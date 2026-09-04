import qrcode

link = "vless://1e423f99-2136-4af4-870f-62428403d088@hermes-railway-template-production-685f.up.railway.app:443?encryption=none&security=tls&sni=hermes-railway-template-production-685f.up.railway.app&type=ws&host=hermes-railway-template-production-685f.up.railway.app&path=%2Freza-rail-ws#Reza-Rail"

qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("/data/vless/reza-rail-qr.png")
print("saved")
