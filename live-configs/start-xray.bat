@echo off
schtasks /create /tn XrayVLESS /tr "C:\xray\xray.exe run -config C:\xray\config.json" /sc onstart /ru SYSTEM /rl highest /f
schtasks /run /tn XrayVLESS
timeout /t 5 /nobreak >NUL
netstat -an | findstr 2080
