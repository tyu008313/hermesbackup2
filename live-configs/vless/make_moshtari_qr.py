import base64
import qrcode

b64 = open("/data/vless/sub-moshtari.txt").read().strip()
link = base64.b64decode(b64).decode().strip()
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(link)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("/data/vless/moshtari-qr.png")
print("saved", len(link))
