$k = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImZiOWI0NWJlLWY4NWUtNGUyMS04ZGVkLWQ4ZWJiYzZiOTI1ZiJ9.eyJpc3MiOiJodHRwczovL3Byb2dyZXNzaXZlLWJhcm5hY2xlLWQ5YThiNDlhNzJmLmFwLXNoYW5naGFpLnRjYi1hcGkudGVuY2VudGNsb3VkYXBpLmNvbSIsInN1YiI6ImFub24iLCJhdWQiOiJwcm9ncmVzc2l2ZS1iYXJuYWNsZS1kOWE4YjQ5YTcyZiIsImV4cCI6NDA5ODIyMzQ3NywiaWF0IjoxNzk0NTQwMjc3LCJub25jZSI6InZRV0owdV8wUW5DdVpOWkRhZnAxOWciLCJhdF9oYXNoIjoidlFXSjB1XzBRbkN1Wk5aRGFmcDE5ZyIsIm5hbWUiOiJBbm9ueW1vdXMiLCJzY29wZSI6ImFub255bW91cyIsInByb2plY3RfaWQiOiJwcm9ncmVzc2l2ZS1iYXJuYWNsZS1kOWE4YjQ5YTcyZiIsIm1ldGEiOnsicGxhdGZvcm0iOiJQdWJsaXNoYWJsZUtleSJ9LCJyb2xlIjoiYW5vbiIsImlzX2Fub255bW91cyI6dHJ1ZSwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiYW5vbnltb3VzIiwicHJvdmlkZXJzIjpbImFub255bW91cyJdfSwidXNlcl9tZXRhZGF0YSI6eyJuYW1lIjoiQW5vbnltb3VzIn0sInVzZXJfdHlwZSI6IiIsImNsaWVudF90eXBlIjoiY2xpZW50X3VzZXIiLCJpc19zeXN0ZW1fYWRtaW4iOmZhbHNlfQ.h3GUB40kySuPOSWGkR5z9ZU4nTarRJtQFmpmyKvhFSGvoGPfGNmTG7ifOGvF88rqd5j8DOEviUPzSxcvHAfUahNrGCi5eouToEN-0Pc2tid5SC5Q9jN-0COjTIuQMaRwHX0XjjTk8NEeMPVhRvP4rDXmIxZDY2WJZw1ecPeqdzzRR56EMWkkKS_F81yX8tSwA50RPWNfl5hbcBeyFm4VlrTCm4wYV9pbvL66sBNUXyI1GAppzabfXKG5FE4ZN_s1ZeLrSkk7kSKHAryrKMMbKpulDBH7rFpRMpkD8WgCGwVe104KoU4ua6y-yhebolYZcOfK7X_doB8ACkg4OSqOvg'
$u = 'https://progressive-barnacle-d9a8b49a72f.api.tcloudbasegateway.com/v1/rdb/rest/responses'
$body = '{"data":{"__test":true,"group":"TEST"}}'
$variants = @(
  @{ Authorization = "Bearer $k"; apikey = $k },
  @{ Authorization = "Bearer $k"; apikey = $k; Prefer = 'return=minimal' },
  @{ apikey = $k }
)
foreach ($v in $variants) {
  $ks = $v.Keys -join '+'
  try {
    $r = Invoke-WebRequest -Method Post -Uri $u -Headers $v -ContentType 'application/json' -Body $body -UseBasicParsing -TimeoutSec 30
    "OK [$ks] " + $r.StatusCode + " " + $r.Content
    break
  } catch {
    $resp = $_.Exception.Response
    $code = try { [int]$resp.StatusCode } catch { '?' }
    $bd = ''
    try { $sr = New-Object IO.StreamReader($resp.GetResponseStream()); $bd = $sr.ReadToEnd() } catch {}
    "FAIL [$ks] $code $bd"
  }
}
