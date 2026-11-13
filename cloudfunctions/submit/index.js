/**
 * 问卷写入云函数（HTTP 访问）
 *   POST /submit   提交问卷 → 写入云数据库 responses 集合
 *   GET  /results?key=xxx  读取全部回答（key 与管理密码一致）
 * 说明：云函数使用环境管理员权限，前端无需登录即可写入。
 */
const tcb = require('@cloudbase/node-sdk');

const ENV_ID = process.env.TCB_ENV || 'progressive-barnacle-d9a8b49a72f';
const ADMIN_KEY = process.env.ADMIN_KEY || 'admin123';
const COLLECTION = 'responses';

const app = tcb.init({ env: ENV_ID });
const db = app.database();

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Max-Age': '86400',
};

function reply(statusCode, obj) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS },
    body: JSON.stringify(obj),
  };
}

function parseBody(event) {
  let raw = event.body || '';
  if (event.isBase64Encoded) raw = Buffer.from(raw, 'base64').toString('utf8');
  if (!raw) return {};
  if (typeof raw === 'object') return raw;
  try { return JSON.parse(raw); } catch { return {}; }
}

async function ensureCollection() {
  try { await db.createCollection(COLLECTION); } catch (e) { /* 已存在则忽略 */ }
}

exports.main = async (event) => {
  const path = String(event.path || event.requestContext?.path || '/');
  const method = String(event.httpMethod || event.requestContext?.httpMethod || 'GET').toUpperCase();

  if (method === 'OPTIONS') return { statusCode: 204, headers: CORS, body: '' };

  // 提交
  if (path.indexOf('submit') >= 0 && method === 'POST') {
    try {
      const body = parseBody(event);
      if (!body || !Object.keys(body).length) return reply(400, { ok: false, error: 'empty body' });
      await ensureCollection();
      const res = await db.collection(COLLECTION).add({
        ...body,
        submittedAt: body.submittedAt || new Date().toISOString(),
        _ip: (event.headers && (event.headers['x-forwarded-for'] || event.headers['x-real-ip'])) || '',
        _ua: (event.headers && event.headers['user-agent']) || '',
      });
      console.log('[submit] ok', res.id);
      return reply(200, { ok: true, id: res.id });
    } catch (e) {
      console.error('[submit] fail', e);
      return reply(500, { ok: false, error: String(e.message || e) });
    }
  }

  // 读取结果
  if (path.indexOf('results') >= 0 && method === 'GET') {
    const q = event.queryStringParameters || {};
    if (q.key !== ADMIN_KEY) return reply(401, { ok: false, error: '密码错误' });
    try {
      let all = [];
      for (let skip = 0; ; skip += 100) {
        const r = await db.collection(COLLECTION).orderBy('submittedAt', 'desc').skip(skip).limit(100).get();
        const docs = r.data || [];
        all = all.concat(docs);
        if (docs.length < 100) break;
      }
      return reply(200, { ok: true, total: all.length, responses: all });
    } catch (e) {
      return reply(500, { ok: false, error: String(e.message || e) });
    }
  }

  return reply(404, { ok: false, error: 'not found', path, method });
};
