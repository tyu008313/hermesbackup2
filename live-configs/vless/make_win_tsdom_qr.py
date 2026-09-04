import qrcode

link = "vless://4f6eea84-f970-4fa0-a349-4a57249ac357@github-rdp-server-1.tail6c7748.ts.net:2080?security=none&encryption=none&type=ws&path=%2Fw80d20929#Moshtari-Win-TSdom"
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("/data/vless/moshtari-win-tsdom-qr.png")
print("saved")
