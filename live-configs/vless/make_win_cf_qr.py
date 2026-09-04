import qrcode

link = "vless://4f6eea84-f970-4fa0-a349-4a57249ac357@invisible-physicians-cant-victorian.trycloudflare.com:443?path=%2Fw80d20929&security=tls&encryption=none&host=invisible-physicians-cant-victorian.trycloudflare.com&type=ws&sni=invisible-physicians-cant-victorian.trycloudflare.com#Moshtari-Win-CF"
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("/data/vless/moshtari-win-cf-qr.png")
print("saved")
