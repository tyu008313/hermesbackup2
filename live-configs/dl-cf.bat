@echo off
powershell -c "Invoke-WebRequest -Uri https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -OutFile C:/xray/cf.exe"
echo DL_EXIT=%ERRORLEVEL%
