# -*- coding: utf-8 -*-
"""Consent form PDF — bilingual (EN template + CN translation), full structure."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialB', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('MSYH', r'C:\Windows\Fonts\msyh.ttc'))
pdfmetrics.registerFont(TTFont('MSYHB', r'C:\Windows\Fonts\msyhbd.ttc'))

OUT = r'e:\question\interview-survey\consent.pdf'

title_s  = ParagraphStyle('title', fontName='ArialB', fontSize=15, leading=22, alignment=TA_CENTER, spaceAfter=2)
cnsub_s  = ParagraphStyle('cnsub', fontName='MSYH',  fontSize=12, leading=18, alignment=TA_CENTER, spaceAfter=14)
h_s      = ParagraphStyle('h',    fontName='ArialB', fontSize=12, leading=17, spaceBefore=12, spaceAfter=4)
hcn_s    = ParagraphStyle('hcn',  fontName='MSYHB',  fontSize=11, leading=16, spaceAfter=4)
body_s   = ParagraphStyle('body', fontName='Arial',  fontSize=11, leading=18, alignment=TA_JUSTIFY)
cn_s     = ParagraphStyle('cn',   fontName='MSYH',   fontSize=10.5, leading=17, alignment=TA_JUSTIFY,
                          textColor='#444444', spaceBefore=3, firstLineIndent=21)
item_s   = ParagraphStyle('item', fontName='Arial',  fontSize=11, leading=18, alignment=TA_JUSTIFY,
                          leftIndent=6*mm, spaceBefore=4)
cnitem_s = ParagraphStyle('cnit', fontName='MSYH',   fontSize=10.5, leading=17, alignment=TA_JUSTIFY,
                          leftIndent=6*mm, spaceBefore=2, textColor='#444444')
plain_s  = ParagraphStyle('plain',fontName='Arial',  fontSize=11, leading=18, spaceBefore=8)
sign_s   = ParagraphStyle('sign', fontName='Arial',  fontSize=11, leading=26, spaceBefore=14)

story = []

# ---------- Page 1: Data Usage Consent Form ----------
story.append(Paragraph('Data Usage Consent Form', title_s))
story.append(Paragraph('用户研究知情同意书', cnsub_s))

story.append(Paragraph('Research Purpose and Procedures', h_s))
story.append(Paragraph('研究目的与流程', hcn_s))
story.append(Paragraph(
    'This research investigates methods that generate 3D scene videos from artistic paintings '
    '(e.g., traditional Chinese paintings). You will be asked to complete an online questionnaire '
    'to evaluate the generated videos. The questionnaire takes approximately 10-15 minutes.', body_s))
story.append(Paragraph(
    '本研究旨在探讨由艺术图像（如中国画）自动生成三维场景视频的相关方法。您将被邀请完成一份在线问卷，'
    '对生成的视频进行评价，整个过程约需 10–15 分钟。', cn_s))

story.append(Paragraph('Data Collection and Usage', h_s))
story.append(Paragraph('数据收集与使用', hcn_s))
story.append(Paragraph(
    'We will collect the following data: your background information (gender, age, major, and '
    'relevant experience), your ratings and preference choices, and your answers to open-ended '
    'questions. The collected data will be used <b>solely for the purpose of this research</b> and '
    'will be presented in an anonymized, aggregated form. The data will not be linked to any '
    'information that could identify you personally, and will not be disclosed to any third party '
    'or used for any other purpose.', body_s))
story.append(Paragraph(
    '我们将收集以下数据：您的背景信息（性别、年龄、专业及相关经验）、您的评分与偏好选择，'
    '以及开放性问题的回答。所收集的数据<b>仅用于本研究</b>，并以匿名、汇总的形式呈现；'
    '数据不会与任何可识别您个人身份的信息相关联，不会披露给任何第三方，也不会用于本研究以外的任何用途。', cn_s))

story.append(Paragraph('Participant Rights', h_s))
story.append(Paragraph('参与者权益', hcn_s))
story.append(Paragraph(
    'Your participation is entirely voluntary. You may stop and withdraw from this study at any '
    'time, and you may skip any question you prefer not to answer. Withdrawal will not result in '
    'any penalty or loss of benefits to you. If you have any questions about this study, please '
    'feel free to contact the researchers.', body_s))
story.append(Paragraph(
    '您的参与完全自愿。您可以随时中止并退出本研究，也可以跳过任何您不愿回答的题目，退出不会带来任何不利影响。'
    '如对本研究有任何疑问，请随时联系研究人员。', cn_s))

story.append(Paragraph('Consent', h_s))
story.append(Paragraph('同意声明', hcn_s))
story.append(Paragraph(
    'I have read and understood the information above. I agree to participate in this research '
    'and allow my data to be used for research purposes.', plain_s))
story.append(Paragraph(
    '我已阅读并理解上述内容，自愿同意参与本研究，并允许我的回答数据用于研究目的。', cn_s))
story.append(Paragraph('Signature 签名: _____________________________', sign_s))
story.append(Paragraph('Date 日期: _____________________________', sign_s))

story.append(Paragraph('Compensation Notice', h_s))
story.append(Paragraph('报酬领取须知', hcn_s))
story.append(Paragraph(
    'For your participation in this study, you will receive a compensation, which will be issued '
    'within one month after the experiment is completed.', plain_s))
story.append(Paragraph(
    '参与本研究您将获得相应报酬，报酬将于实验结束后一个月内发放，请知悉。', cn_s))
story.append(Paragraph('Signature 签名: _____________________________', sign_s))
story.append(Paragraph('Date 日期: _____________________________', sign_s))

# ---------- (Study Procedure removed per user request) ----------
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=25*mm, rightMargin=25*mm, topMargin=24*mm, bottomMargin=24*mm,
                        title='用户研究知情同意书 Data Usage Consent Form', author='Research Team')
doc.build(story)
print('PDF_OK')
