from PIL import Image, ImageDraw

W, H = 800, 800
img = Image.new("RGB", (W, H), (18, 18, 30))
d = ImageDraw.Draw(img)

# background glow
for r in range(380, 0, -1):
    c = int(18 + (60 - 18) * (1 - r / 380))
    d.ellipse([400 - r, 400 - r, 400 + r, 400 + r], fill=(c, c // 2, 70))

# ears
d.polygon([(230, 330), (200, 130), (360, 250)], fill=(255, 150, 60))
d.polygon([(570, 330), (600, 130), (440, 250)], fill=(255, 150, 60))
d.polygon([(250, 300), (230, 170), (340, 255)], fill=(255, 180, 200))
d.polygon([(550, 300), (570, 170), (460, 255)], fill=(255, 180, 200))

# head
d.ellipse([180, 220, 620, 620], fill=(255, 165, 70))
# stripes
for x in (300, 360, 440, 500):
    d.polygon([(x, 225), (x + 25, 225), (x + 12, 300)], fill=(230, 120, 40))

# eyes
d.ellipse([(280, 380), (370, 470)], fill=(255, 255, 255))
d.ellipse([(430, 380), (520, 470)], fill=(255, 255, 255))
d.ellipse([(305, 400), (350, 455)], fill=(30, 200, 120))
d.ellipse([(450, 400), (495, 455)], fill=(30, 200, 120))
d.ellipse([(318, 412), (338, 442)], fill=(10, 10, 10))
d.ellipse([(463, 412), (483, 442)], fill=(10, 10, 10))
d.ellipse([(312, 406), (322, 418)], fill=(255, 255, 255))
d.ellipse([(457, 406), (467, 418)], fill=(255, 255, 255))

# nose + mouth
d.polygon([(385, 500), (415, 500), (400, 518)], fill=(255, 100, 150))
d.arc([(360, 515), (400, 550)], start=0, end=180, fill=(90, 40, 20), width=5)
d.arc([(400, 515), (440, 550)], start=0, end=180, fill=(90, 40, 20), width=5)

# whiskers
for y in (490, 510, 530):
    d.line([(150, y), (270, y + 10)], fill=(255, 255, 255), width=4)
    d.line([(530, y + 10), (650, y)], fill=(255, 255, 255), width=4)

# blush
d.ellipse([(250, 500), (300, 540)], fill=(255, 120, 140))
d.ellipse([(500, 500), (550, 540)], fill=(255, 120, 140))

img.save("/data/vless/my-cat.png")
print("saved")
