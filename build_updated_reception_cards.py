import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

base_dir = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11'
repo_public = '/Users/ten5/Documents/Github/wedding-planning/public'

t1_path = os.path.join(base_dir, '.user_uploaded/media_1791938866368_e57536af.jpg')
t2_path = os.path.join(base_dir, '.user_uploaded/media_1791938866370_e6460264.jpg')

font_cinzel = '/Users/ten5/Documents/Github/wedding-planning/fonts/Cinzel-Regular.ttf'
font_georgia_b = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
font_outfit = '/System/Library/Fonts/Supplemental/Arial.ttf'

def build_option_1():
    # Option 1: Template 1 (Chandelier & Pastel Pink)
    # Header: "INVITING YOU TO GIVE THEM BLESSINGS \n AT THE WEDDING RECEPTION OF"
    # Time: "5:30 PM onwards"
    # Button: "Check Here for more details" (clickable)
    im1 = Image.open(t1_path).convert('RGB')
    arr1 = np.array(im1, dtype=float)
    w, h = im1.size # 571, 1024

    # 1. Seamless vertical interpolation for time (y: 821..837, x: 185..385)
    y_top, y_bot = 820, 838
    for y in range(821, 838):
        ty = (y - y_top) / (y_bot - y_top)
        for x in range(185, 386):
            col_v = (1 - ty) * arr1[y_top, x] + ty * arr1[y_bot, x]
            arr1[y, x] = col_v

    # 2. Seamless vertical interpolation for button interior (y: 882..914, x: 170..400)
    y_btop, y_bbot = 880, 916
    for y in range(882, 915):
        ty = (y - y_btop) / (y_bbot - y_btop)
        for x in range(170, 401):
            col_v = (1 - ty) * arr1[y_btop, x] + ty * arr1[y_bbot, x]
            arr1[y, x] = col_v

    im1 = Image.fromarray(np.clip(arr1, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(im1)

    # Draw new time: "5:30 PM onwards"
    f_time = ImageFont.truetype(font_georgia_b, 13)
    time_text = "5:30 PM onwards"
    bb = draw.textbbox((0, 0), time_text, font=f_time)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) / 2, 823), time_text, font=f_time, fill=(58, 30, 16))

    # Draw new button text: "Check Here for more details"
    f_btn = ImageFont.truetype(font_cinzel, 11)
    btn_text = "Check Here for more details"
    bb = draw.textbbox((0, 0), btn_text, font=f_btn)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) / 2, 893), btn_text, font=f_btn, fill=(145, 110, 55))

    out_png = os.path.join(base_dir, 'Option1_Chandelier_Reception_Card_preview.png')
    im1.save(out_png, quality=95)

    # Clickable PDF
    out_pdf = os.path.join(base_dir, 'Option1_Chandelier_Wedding_Reception_Card.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(w, h))
    c.drawImage(out_png, 0, 0, width=w, height=h)
    btn_bx0, btn_by0, btn_bx1, btn_by1 = 150, 877, 420, 919
    c.linkURL("https://ten5.github.io/wedding-planning/", (btn_bx0, h - btn_by1, btn_bx1, h - btn_by0), relative=0)
    c.save()

    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option1_Chandelier_Wedding_Reception_Card.pdf'))
    print("Option 1 generated successfully")


def build_option_2():
    # Option 2: Template 2 (Marigold & Gold Mandala / Deep Chocolate)
    # Header: "JOIN US IN CELEBRATING \n THE WEDDING RECEPTION OF"
    # Time: "5:30 PM onwards"
    # Button: "Check Here for more details" (clickable)
    im2 = Image.open(t2_path).convert('RGB')
    arr2 = np.array(im2, dtype=float)
    w, h = im2.size # 571, 1024

    # 1. Seamless vertical interpolation for header (y: 704..755, x: 118..452)
    y_htop, y_hbot = 702, 757
    for y in range(704, 756):
        ty = (y - y_htop) / (y_hbot - y_htop)
        for x in range(118, 453):
            col_v = (1 - ty) * arr2[y_htop, x] + ty * arr2[y_hbot, x]
            arr2[y, x] = col_v

    # 2. Seamless vertical interpolation for time (y: 873..891, x: 180..390)
    y_ttop, y_tbot = 871, 893
    for y in range(873, 892):
        ty = (y - y_ttop) / (y_tbot - y_ttop)
        for x in range(180, 391):
            col_v = (1 - ty) * arr2[y_ttop, x] + ty * arr2[y_tbot, x]
            arr2[y, x] = col_v

    # 3. Seamless vertical interpolation for button interior (y: 934..966, x: 165..405)
    y_btop, y_bbot = 932, 968
    for y in range(934, 967):
        ty = (y - y_btop) / (y_bbot - y_btop)
        for x in range(165, 406):
            col_v = (1 - ty) * arr2[y_btop, x] + ty * arr2[y_bbot, x]
            arr2[y, x] = col_v

    im2 = Image.fromarray(np.clip(arr2, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(im2)

    # Draw updated header:
    # "JOIN US IN CELEBRATING"
    # "THE WEDDING RECEPTION OF"
    f_h1 = ImageFont.truetype(font_cinzel, 12)
    f_h2 = ImageFont.truetype(font_cinzel, 11)
    
    h1_text = "JOIN US IN CELEBRATING"
    h2_text = "THE WEDDING RECEPTION OF"
    
    bb1 = draw.textbbox((0, 0), h1_text, font=f_h1)
    tw1 = bb1[2] - bb1[0]
    x1 = (w - tw1) / 2
    draw.text((x1 + 1, 715), h1_text, font=f_h1, fill=(25, 5, 8))
    draw.text((x1, 714), h1_text, font=f_h1, fill=(235, 192, 120))

    bb2 = draw.textbbox((0, 0), h2_text, font=f_h2)
    tw2 = bb2[2] - bb2[0]
    x2 = (w - tw2) / 2
    draw.text((x2 + 1, 735), h2_text, font=f_h2, fill=(25, 5, 8))
    draw.text((x2, 734), h2_text, font=f_h2, fill=(225, 182, 110))

    # Draw new time: "5:30 PM onwards"
    f_time = ImageFont.truetype(font_georgia_b, 13)
    time_text = "5:30 PM onwards"
    bb = draw.textbbox((0, 0), time_text, font=f_time)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) / 2, 876), time_text, font=f_time, fill=(255, 240, 220))

    # Draw new button text: "Check Here for more details"
    f_btn = ImageFont.truetype(font_cinzel, 11)
    btn_text = "Check Here for more details"
    bb = draw.textbbox((0, 0), btn_text, font=f_btn)
    tw = bb[2] - bb[0]
    bx = (w - tw) / 2
    draw.text((bx + 1, 948), btn_text, font=f_btn, fill=(25, 5, 8))
    draw.text((bx, 947), btn_text, font=f_btn, fill=(235, 192, 120))

    out_png = os.path.join(base_dir, 'Option2_Mandala_Reception_Card_preview.png')
    im2.save(out_png, quality=95)

    # Clickable PDF
    out_pdf = os.path.join(base_dir, 'Option2_Mandala_Wedding_Reception_Card.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(w, h))
    c.drawImage(out_png, 0, 0, width=w, height=h)
    btn_bx0, btn_by0, btn_bx1, btn_by1 = 150, 930, 420, 970
    c.linkURL("https://ten5.github.io/wedding-planning/", (btn_bx0, h - btn_by1, btn_bx1, h - btn_by0), relative=0)
    c.save()

    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option2_Mandala_Wedding_Reception_Card.pdf'))
    print("Option 2 generated successfully")

build_option_1()
build_option_2()
print("Both options completed!")

def build_option_1_join_us():
    im1 = Image.open(t1_path).convert('RGB')
    arr1 = np.array(im1, dtype=float)
    w, h = im1.size

    # Seamless vertical interpolation for header (y: 650..705, x: 120..450)
    y_htop, y_hbot = 648, 707
    for y in range(650, 706):
        ty = (y - y_htop) / (y_hbot - y_htop)
        for x in range(120, 451):
            col_v = (1 - ty) * arr1[y_htop, x] + ty * arr1[y_hbot, x]
            arr1[y, x] = col_v

    # Time patch
    y_top, y_bot = 820, 838
    for y in range(821, 838):
        ty = (y - y_top) / (y_bot - y_top)
        for x in range(185, 386):
            col_v = (1 - ty) * arr1[y_top, x] + ty * arr1[y_bot, x]
            arr1[y, x] = col_v

    # Button patch
    y_btop, y_bbot = 880, 916
    for y in range(882, 915):
        ty = (y - y_btop) / (y_bbot - y_btop)
        for x in range(170, 401):
            col_v = (1 - ty) * arr1[y_btop, x] + ty * arr1[y_bbot, x]
            arr1[y, x] = col_v

    im1 = Image.fromarray(np.clip(arr1, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(im1)

    f_h1 = ImageFont.truetype(font_cinzel, 12)
    f_h2 = ImageFont.truetype(font_cinzel, 11)
    h1_text = "JOIN US IN CELEBRATING"
    h2_text = "THE WEDDING RECEPTION OF"
    bb1 = draw.textbbox((0, 0), h1_text, font=f_h1)
    tw1 = bb1[2] - bb1[0]
    draw.text(((w - tw1) / 2, 668), h1_text, font=f_h1, fill=(142, 105, 50))
    bb2 = draw.textbbox((0, 0), h2_text, font=f_h2)
    tw2 = bb2[2] - bb2[0]
    draw.text(((w - tw2) / 2, 688), h2_text, font=f_h2, fill=(142, 105, 50))

    f_time = ImageFont.truetype(font_georgia_b, 13)
    time_text = "5:30 PM onwards"
    bb = draw.textbbox((0, 0), time_text, font=f_time)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) / 2, 823), time_text, font=f_time, fill=(58, 30, 16))

    f_btn = ImageFont.truetype(font_cinzel, 11)
    btn_text = "Check Here for more details"
    bb = draw.textbbox((0, 0), btn_text, font=f_btn)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) / 2, 893), btn_text, font=f_btn, fill=(145, 110, 55))

    out_png = os.path.join(base_dir, 'Option1B_Chandelier_JoinUs_preview.png')
    im1.save(out_png, quality=95)

    out_pdf = os.path.join(base_dir, 'Option1B_Chandelier_JoinUs_Wedding_Reception_Card.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(w, h))
    c.drawImage(out_png, 0, 0, width=w, height=h)
    btn_bx0, btn_by0, btn_bx1, btn_by1 = 150, 877, 420, 919
    c.linkURL("https://ten5.github.io/wedding-planning/", (btn_bx0, h - btn_by1, btn_bx1, h - btn_by0), relative=0)
    c.save()

    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option1B_Chandelier_JoinUs_Wedding_Reception_Card.pdf'))
    print("Option 1B (Join Us) generated successfully")

build_option_1_join_us()
