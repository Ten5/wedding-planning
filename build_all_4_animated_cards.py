import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

artifact_dir = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11'
repo_public = '/Users/ten5/Documents/Github/wedding-planning/public'

font_vibes = '/Users/ten5/Documents/Github/wedding-planning/fonts/GreatVibes-Regular.ttf'
font_cinzel = '/Users/ten5/Documents/Github/wedding-planning/fonts/Cinzel-Regular.ttf'
font_georgia_b = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
font_georgia = '/System/Library/Fonts/Supplemental/Georgia.ttf'

W, H = 1080, 1920

# -------------------------------------------------------------
# CARD 1: Bodhuboron Caricature (Reception)
# Phrasing: "WEDDING RECEPTION INVITATION"
# -------------------------------------------------------------
def build_card_1():
    img_path = os.path.join(artifact_dir, 'bengali_wedding_bodhuboron_caricature_png_1791881107123.jpg')
    raw_img = Image.open(img_path).convert('RGB')
    orig_w, orig_h = raw_img.size
    
    scaled_h = int(orig_h * (W / orig_w))
    scaled_img = raw_img.resize((W, scaled_h), Image.Resampling.LANCZOS)
    
    canvas_img = Image.new('RGB', (W, H))
    canvas_img.paste(scaled_img, (0, 0))
    
    c_start = np.array(scaled_img.getpixel((W // 2, scaled_h - 1)), dtype=float)
    c_end = np.array([178, 142, 106], dtype=float)
    
    arr = np.array(canvas_img)
    for y in range(scaled_h, H):
        t = (y - scaled_h) / max(1, (H - scaled_h))
        col = (1 - t) * c_start + t * c_end
        arr[y, :, :] = col.astype(np.uint8)
    
    canvas_img = Image.fromarray(arr)
    draw = ImageDraw.Draw(canvas_img)
    
    f_title = ImageFont.truetype(font_cinzel, 33)
    f_names = ImageFont.truetype(font_vibes, 112)
    f_date = ImageFont.truetype(font_cinzel, 30)
    f_details = ImageFont.truetype(font_georgia_b, 26)
    f_btn = ImageFont.truetype(font_cinzel, 24)
    
    GOLD_DARK = (118, 72, 20)
    GOLD_MED = (152, 102, 35)
    TEXT_DARK = (52, 32, 18)
    DIVIDER = (185, 145, 95)
    
    def center_text(y, text, font, fill, shadow=None):
        bb = draw.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        x = (W - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bb[3] - bb[1])
    
    y = 1200
    center_text(y, "WEDDING RECEPTION INVITATION", f_title, GOLD_DARK, shadow=(1, 1, (245, 235, 215)))
    y += 56
    center_text(y, "Tarunima & Subhayu", f_names, GOLD_DARK, shadow=(2, 2, (230, 215, 185)))
    
    y += 140
    draw.line([(W/2 - 130, y), (W/2 - 25, y)], fill=DIVIDER, width=2)
    draw.ellipse([(W/2 - 6, y - 6), (W/2 + 6, y + 6)], fill=GOLD_MED)
    draw.line([(W/2 + 25, y), (W/2 + 130, y)], fill=DIVIDER, width=2)
    
    y += 48
    center_text(y, "FRIDAY, NOVEMBER 13, 2026", f_date, GOLD_DARK)
    y += 48
    center_text(y, "5:00 PM onwards", f_details, TEXT_DARK)
    y += 42
    center_text(y, "North Park • San Jose, California", f_details, TEXT_DARK)
    
    y += 65
    btn_w, btn_h = 520, 80
    bx0 = (W - btn_w) / 2
    by0 = y
    bx1 = bx0 + btn_w
    by1 = by0 + btn_h
    
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=40, fill=(255, 252, 245), outline=(168, 122, 65), width=2)
    center_text(by0 + 25, "TIME, LOCATION & MORE", f_btn, GOLD_DARK)
    
    out_png = os.path.join(artifact_dir, 'Option1_Reception_Invitation_preview.png')
    canvas_img.save(out_png, quality=95)
    
    out_pdf = os.path.join(artifact_dir, 'Option1_Wedding_Reception_Invitation.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(W, H))
    c.drawImage(out_png, 0, 0, width=W, height=H)
    c.linkURL("https://ten5.github.io/wedding-planning/", (bx0, H - by1, bx1, H - by0), relative=0)
    c.save()
    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option1_Wedding_Reception_Invitation.pdf'))
    print("Card 1 updated")


# -------------------------------------------------------------
# CARD 2: Sindoor Daan 3D Scene
# Phrasing: "INVITING YOU TO GIVE THEM BLESSINGS"
# -------------------------------------------------------------
def build_card_2():
    img_path = os.path.join(artifact_dir, 'bengali_wedding_sindoor_daan_3d_png_1791881147300.jpg')
    raw_img = Image.open(img_path).convert('RGB')
    orig_w, orig_h = raw_img.size
    
    scaled_h = int(orig_h * (W / orig_w))
    scaled_img = raw_img.resize((W, scaled_h), Image.Resampling.LANCZOS)
    
    canvas_img = Image.new('RGB', (W, H))
    canvas_img.paste(scaled_img, (0, 0))
    
    c_start = np.array(scaled_img.getpixel((W // 2, scaled_h - 1)), dtype=float)
    c_end = np.array([250, 242, 230], dtype=float)
    
    arr = np.array(canvas_img)
    for y in range(scaled_h, H):
        t = (y - scaled_h) / max(1, (H - scaled_h))
        col = (1 - t) * c_start + t * c_end
        arr[y, :, :] = col.astype(np.uint8)
    
    canvas_img = Image.fromarray(arr)
    draw = ImageDraw.Draw(canvas_img)
    
    f_title = ImageFont.truetype(font_cinzel, 26)
    f_sub = ImageFont.truetype(font_cinzel, 20)
    f_names = ImageFont.truetype(font_vibes, 102)
    f_date = ImageFont.truetype(font_cinzel, 29)
    f_details = ImageFont.truetype(font_georgia_b, 25)
    f_btn = ImageFont.truetype(font_cinzel, 24)
    
    GOLD_DEEP = (130, 80, 25)
    GOLD_MED = (165, 115, 45)
    TEXT_DARK = (60, 38, 22)
    DIVIDER = (205, 168, 115)
    
    def center_text(y, text, font, fill, shadow=None):
        bb = draw.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        x = (W - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bb[3] - bb[1])
    
    y = 1250
    center_text(y, "INVITING YOU TO GIVE THEM BLESSINGS", f_title, GOLD_DEEP, shadow=(1, 1, (255, 250, 240)))
    y += 38
    center_text(y, "at the Wedding Celebration of", f_sub, (145, 100, 50))
    y += 38
    center_text(y, "Tarunima & Subhayu", f_names, GOLD_DEEP, shadow=(2, 2, (240, 225, 205)))
    
    y += 125
    draw.line([(W/2 - 130, y), (W/2 - 25, y)], fill=DIVIDER, width=2)
    draw.ellipse([(W/2 - 6, y - 6), (W/2 + 6, y + 6)], fill=GOLD_MED)
    draw.line([(W/2 + 25, y), (W/2 + 130, y)], fill=DIVIDER, width=2)
    
    y += 42
    center_text(y, "FRIDAY, NOVEMBER 13, 2026", f_date, GOLD_DEEP)
    y += 45
    center_text(y, "5:00 PM onwards", f_details, TEXT_DARK)
    y += 40
    center_text(y, "North Park • San Jose, California", f_details, TEXT_DARK)
    
    y += 65
    btn_w, btn_h = 520, 80
    bx0 = (W - btn_w) / 2
    by0 = y
    bx1 = bx0 + btn_w
    by1 = by0 + btn_h
    
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=40, fill=(255, 255, 252), outline=(180, 135, 75), width=2)
    center_text(by0 + 25, "TIME, LOCATION & MORE", f_btn, GOLD_DEEP)
    
    out_png = os.path.join(artifact_dir, 'Option2_Blessings_Invitation_preview.png')
    canvas_img.save(out_png, quality=95)
    
    out_pdf = os.path.join(artifact_dir, 'Option2_Blessings_Wedding_Invitation.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(W, H))
    c.drawImage(out_png, 0, 0, width=W, height=H)
    c.linkURL("https://ten5.github.io/wedding-planning/", (bx0, H - by1, bx1, H - by0), relative=0)
    c.save()
    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option2_Blessings_Wedding_Invitation.pdf'))
    print("Card 2 updated")


# -------------------------------------------------------------
# CARD 3: Festive Regal Bengali Portrait (Royal Chocolate/Gold)
# Phrasing: "JOIN US IN CELEBRATING THE WEDDING INVITATION"
# -------------------------------------------------------------
def build_card_3():
    img_path = os.path.join(artifact_dir, 'bengali_wedding_festive_regal_1791881239310.jpg')
    raw_img = Image.open(img_path).convert('RGB')
    
    canvas_img = raw_img.resize((W, H), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(canvas_img)
    
    f_header1 = ImageFont.truetype(font_cinzel, 25)
    f_header2 = ImageFont.truetype(font_cinzel, 28)
    f_names = ImageFont.truetype(font_vibes, 108)
    f_date = ImageFont.truetype(font_cinzel, 30)
    f_details = ImageFont.truetype(font_georgia_b, 25)
    f_btn = ImageFont.truetype(font_cinzel, 24)
    
    GOLD_LIGHT = (245, 215, 145)
    GOLD_WARM = (225, 185, 105)
    CREAM = (255, 245, 230)
    DIVIDER = (190, 145, 75)
    
    def center_text(y, text, font, fill, shadow=None):
        bb = draw.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        x = (W - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bb[3] - bb[1])
    
    y = 1320
    center_text(y, "JOIN US IN CELEBRATING", f_header1, GOLD_WARM, shadow=(1, 1, (15, 5, 5)))
    y += 38
    center_text(y, "THE WEDDING INVITATION OF", f_header2, GOLD_LIGHT, shadow=(1, 1, (15, 5, 5)))
    y += 52
    center_text(y, "Tarunima & Subhayu", f_names, GOLD_LIGHT, shadow=(2, 2, (20, 5, 5)))
    
    y += 135
    draw.line([(W/2 - 130, y), (W/2 - 25, y)], fill=DIVIDER, width=2)
    draw.ellipse([(W/2 - 6, y - 6), (W/2 + 6, y + 6)], fill=GOLD_WARM)
    draw.line([(W/2 + 25, y), (W/2 + 130, y)], fill=DIVIDER, width=2)
    
    y += 45
    center_text(y, "FRIDAY, NOVEMBER 13, 2026", f_date, GOLD_LIGHT, shadow=(1, 1, (15, 5, 5)))
    y += 46
    center_text(y, "5:00 PM onwards", f_details, CREAM, shadow=(1, 1, (15, 5, 5)))
    y += 40
    center_text(y, "North Park • San Jose, California", f_details, CREAM, shadow=(1, 1, (15, 5, 5)))
    
    y += 65
    btn_w, btn_h = 520, 80
    bx0 = (W - btn_w) / 2
    by0 = y
    bx1 = bx0 + btn_w
    by1 = by0 + btn_h
    
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=40, fill=(35, 10, 10), outline=(215, 175, 95), width=2)
    center_text(by0 + 25, "TIME, LOCATION & MORE", f_btn, GOLD_LIGHT)
    
    out_png = os.path.join(artifact_dir, 'Option3_Regal_Celebration_preview.png')
    canvas_img.save(out_png, quality=95)
    
    out_pdf = os.path.join(artifact_dir, 'Option3_Regal_Wedding_Invitation.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(W, H))
    c.drawImage(out_png, 0, 0, width=W, height=H)
    c.linkURL("https://ten5.github.io/wedding-planning/", (bx0, H - by1, bx1, H - by0), relative=0)
    c.save()
    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option3_Regal_Wedding_Invitation.pdf'))
    print("Card 3 updated")


# -------------------------------------------------------------
# CARD 4: Anime / Ghibli Watercolor Warm Glow
# Phrasing: Minimal Wording
# -------------------------------------------------------------
def build_card_4():
    img_path = os.path.join(artifact_dir, 'bengali_wedding_anime_ghibli_1791881261748.jpg')
    raw_img = Image.open(img_path).convert('RGB')
    
    canvas_img = raw_img.resize((W, H), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(canvas_img)
    
    f_sub = ImageFont.truetype(font_cinzel, 24)
    f_names = ImageFont.truetype(font_vibes, 114)
    f_date = ImageFont.truetype(font_cinzel, 28)
    f_btn = ImageFont.truetype(font_cinzel, 24)
    
    BROWN_DARK = (95, 48, 18)
    BROWN_MED = (135, 82, 38)
    DIVIDER = (205, 160, 110)
    
    def center_text(y, text, font, fill, shadow=None):
        bb = draw.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        x = (W - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bb[3] - bb[1])
    
    # Position in the clean ivory watercolor wash at y=1520
    y = 1515
    center_text(y, "WEDDING RECEPTION", f_sub, BROWN_MED, shadow=(1, 1, (255, 250, 240)))
    y += 40
    center_text(y, "Tarunima & Subhayu", f_names, BROWN_DARK, shadow=(2, 2, (245, 230, 210)))
    
    y += 130
    draw.line([(W/2 - 120, y), (W/2 - 20, y)], fill=DIVIDER, width=2)
    draw.ellipse([(W/2 - 5, y - 5), (W/2 + 5, y + 5)], fill=BROWN_MED)
    draw.line([(W/2 + 20, y), (W/2 + 120, y)], fill=DIVIDER, width=2)
    
    y += 38
    center_text(y, "NOVEMBER 13, 2026 • SAN JOSE, CA", f_date, BROWN_DARK)
    
    y += 58
    btn_w, btn_h = 520, 80
    bx0 = (W - btn_w) / 2
    by0 = y
    bx1 = bx0 + btn_w
    by1 = by0 + btn_h
    
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=40, fill=(255, 252, 246), outline=(180, 130, 80), width=2)
    center_text(by0 + 25, "TIME, LOCATION & MORE", f_btn, BROWN_DARK)
    
    out_png = os.path.join(artifact_dir, 'Option4_Anime_Minimal_preview.png')
    canvas_img.save(out_png, quality=95)
    
    out_pdf = os.path.join(artifact_dir, 'Option4_Anime_Minimal_Wedding_Invitation.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(W, H))
    c.drawImage(out_png, 0, 0, width=W, height=H)
    c.linkURL("https://ten5.github.io/wedding-planning/", (bx0, H - by1, bx1, H - by0), relative=0)
    c.save()
    shutil.copyfile(out_pdf, os.path.join(repo_public, 'Option4_Anime_Minimal_Wedding_Invitation.pdf'))
    print("Card 4 updated")

build_card_1()
build_card_2()
build_card_3()
build_card_4()
print("All 4 cards completed perfectly!")
