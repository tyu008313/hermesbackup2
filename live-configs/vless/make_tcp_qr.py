import qrcode

link = "vless://1e423f99-2136-4af4-870f-62428403d088@altaria.proxy.rlwy.net:59085?security=none&encryption=none&type=ws&path=%2Freza-tcp-59#Reza-TCP59085"
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("/data/vless/reza-tcp-qr.png")
print("saved")
