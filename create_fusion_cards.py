import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

base_dir = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11'
repo_public = '/Users/ten5/Documents/Github/wedding-planning/public'

art_fusion_path = os.path.join(base_dir, 'wedding_invitation_card_1791942221896.jpg')
t1_path = os.path.join(base_dir, '.user_uploaded/media_1791938866368_e57536af.jpg')
t2_path = os.path.join(base_dir, '.user_uploaded/media_1791938866370_e6460264.jpg')

font_cinzel = '/Users/ten5/Documents/Github/wedding-planning/fonts/Cinzel-Regular.ttf'
font_vibes = '/Users/ten5/Documents/Github/wedding-planning/fonts/GreatVibes-Regular.ttf'
font_georgia_b = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'

W, H = 1080, 1920

# --------------------------------------------------------------------------
# DESIGN 1: THE FUSION (2D Couple from Opt 2 + Pastel Chandelier Stage from Opt 1)
# --------------------------------------------------------------------------
def make_card_fusion(header_text_type="join_us"):
    raw_img = Image.open(art_fusion_path).convert('RGB')
    orig_w, orig_h = raw_img.size
    
    scaled_h = int(orig_h * (W / orig_w))
    img = raw_img.resize((W, scaled_h), Image.Resampling.LANCZOS)
    
    if scaled_h > H:
        img = img.crop((0, 0, W, H))
    elif scaled_h < H:
        canvas_bg = Image.new('RGB', (W, H), (255, 253, 248))
        canvas_bg.paste(img, (0, 0))
        img = canvas_bg

    draw = ImageDraw.Draw(img)

    f_h1 = ImageFont.truetype(font_cinzel, 24)
    f_h2 = ImageFont.truetype(font_cinzel, 22)
    f_names = ImageFont.truetype(font_vibes, 96)
    f_date = ImageFont.truetype(font_cinzel, 27)
    f_time = ImageFont.truetype(font_georgia_b, 25)
    f_venue = ImageFont.truetype(font_georgia_b, 25)
    f_btn = ImageFont.truetype(font_cinzel, 24)

    GOLD_DARK = (128, 85, 30)
    GOLD_MED = (165, 115, 45)
    TEXT_DARK = (52, 28, 14)
    DEEP_BTN_TEXT = (45, 20, 8)  # Rich, deep espresso brown for maximum visibility!
    DIVIDER = (195, 155, 100)

    def center_text(y, text, font, fill, shadow=None):
        bb = draw.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        x = (W - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bb[3] - bb[1])

    # Ornamental gold drop ends around y=1420. We start text cleanly at y=1450.
    y = 1450
    if header_text_type == "join_us":
        center_text(y, "JOIN US IN CELEBRATING", f_h1, GOLD_DARK, shadow=(1, 1, (255, 250, 242)))
        y += 32
        center_text(y, "THE WEDDING RECEPTION OF", f_h2, GOLD_DARK, shadow=(1, 1, (255, 250, 242)))
    else:
        center_text(y, "INVITING YOU TO GIVE THEM BLESSINGS", f_h1, GOLD_DARK, shadow=(1, 1, (255, 250, 242)))
        y += 32
        center_text(y, "AT THE WEDDING RECEPTION OF", f_h2, GOLD_DARK, shadow=(1, 1, (255, 250, 242)))

    # Names: Subhayu & Tarunima
    y += 40
    center_text(y, "Subhayu & Tarunima", f_names, GOLD_DARK, shadow=(2, 2, (240, 225, 205)))

    # Elegant divider
    y += 105
    draw.line([(W/2 - 120, y), (W/2 - 20, y)], fill=DIVIDER, width=2)
    draw.ellipse([(W/2 - 5, y - 5), (W/2 + 5, y + 5)], fill=GOLD_MED)
    draw.line([(W/2 + 20, y), (W/2 + 120, y)], fill=DIVIDER, width=2)

    # Date, Time, Venue
    y += 32
    center_text(y, "FRIDAY, NOVEMBER 13, 2026", f_date, GOLD_DARK)
    y += 36
    center_text(y, "5:30 PM onwards", f_time, TEXT_DARK)
    y += 34
    center_text(y, "North Park • San Jose, California", f_venue, TEXT_DARK)

    # Clickable Button with DEEP, bold high-contrast font and comfortable margins
    y += 45
    btn_w, btn_h = 580, 72
    bx0 = (W - btn_w) / 2
    by0 = y
    bx1 = bx0 + btn_w
    by1 = by0 + btn_h

    # Rounded pill outline
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=36, fill=(255, 252, 246), outline=(150, 105, 45), width=2)
    
    # Use bold font with deep mahogany/espresso brown for maximum legibility
    f_btn_bold = ImageFont.truetype(font_georgia_b, 25)
    DEEP_BTN_COLOR = (32, 12, 5)
    bb = draw.textbbox((0, 0), "Check Here for more details", font=f_btn_bold)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text(((W - tw) / 2, by0 + (btn_h - th) / 2 - 2), "Check Here for more details", font=f_btn_bold, fill=DEEP_BTN_COLOR)

    prefix = "OptionA_Fusion_JoinUs" if header_text_type == "join_us" else "OptionA_Fusion_Blessings"
    out_png = os.path.join(base_dir, f'{prefix}_preview.png')
    img.save(out_png, quality=95)

    out_pdf = os.path.join(base_dir, f'{prefix}_Wedding_Reception_Card.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(W, H))
    c.drawImage(out_png, 0, 0, width=W, height=H)
    c.linkURL("https://ten5.github.io/wedding-planning/", (bx0, H - by1, bx1, H - by0), relative=0)
    c.save()

    shutil.copyfile(out_pdf, os.path.join(repo_public, f'{prefix}_Wedding_Reception_Card.pdf'))
    print(f"{prefix} generated successfully: button at y=({by0}, {by1})")


# --------------------------------------------------------------------------
# DESIGN 2: OPTION 1 ORIGINAL with Deep High-Visibility Button Font
# --------------------------------------------------------------------------
def make_card_t1_deep(header_text_type="blessings"):
    im1 = Image.open(t1_path).convert('RGB')
    arr1 = np.array(im1, dtype=float)
    w, h = im1.size

    # Patch time
    y_top, y_bot = 820, 838
    for y in range(821, 838):
        ty = (y - y_top) / (y_bot - y_top)
        for x in range(185, 386):
            col_v = (1 - ty) * arr1[y_top, x] + ty * arr1[y_bot, x]
            arr1[y, x] = col_v

    # Patch button
    y_btop, y_bbot = 880, 916
    for y in range(882, 915):
        ty = (y - y_btop) / (y_bbot - y_btop)
        for x in range(165, 406):
            col_v = (1 - ty) * arr1[y_btop, x] + ty * arr1[y_bbot, x]
            arr1[y, x] = col_v

    # If join_us header requested, patch the header area
    if header_text_type == "join_us":
        y_htop, y_hbot = 662, 706
        for y in range(665, 704):
            ty = (y - y_htop) / (y_hbot - y_htop)
            for x in range(130, 442):
                col_v = (1 - ty) * arr1[y_htop, x] + ty * arr1[y_hbot, x]
                arr1[y, x] = col_v

    im1 = Image.fromarray(np.clip(arr1, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(im1)

    if header_text_type == "join_us":
        f_h1 = ImageFont.truetype(font_cinzel, 12)
        f_h2 = ImageFont.truetype(font_cinzel, 11)
        h1_text = "JOIN US IN CELEBRATING"
        h2_text = "THE WEDDING RECEPTION OF"
        bb1 = draw.textbbox((0, 0), h1_text, font=f_h1)
        tw1 = bb1[2] - bb1[0]
        draw.text(((w - tw1) / 2, 668), h1_text, font=f_h1, fill=(135, 95, 42))
        bb2 = draw.textbbox((0, 0), h2_text, font=f_h2)
        tw2 = bb2[2] - bb2[0]
        draw.text(((w - tw2) / 2, 688), h2_text, font=f_h2, fill=(135, 95, 42))

    f_time = ImageFont.truetype(font_georgia_b, 13)
    time_text = "5:30 PM onwards"
    bb = draw.textbbox((0, 0), time_text, font=f_time)
    tw = bb[2] - bb[0]
    draw.text(((w - tw) / 2, 823), time_text, font=f_time, fill=(58, 30, 16))

    # Deeper, bolder font for high visibility: Georgia Bold, rich dark espresso (28, 10, 4)
    f_btn = ImageFont.truetype(font_georgia_b, 13)
    btn_text = "Check Here for more details"
    bb = draw.textbbox((0, 0), btn_text, font=f_btn)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text(((w - tw) / 2, 885 + (32 - th) / 2), btn_text, font=f_btn, fill=(28, 10, 4))

    prefix = "Option1_Chandelier_DeeperFont" if header_text_type == "blessings" else "Option1B_Chandelier_JoinUs_DeeperFont"
    pdf_name = "Option1_Chandelier_Wedding_Reception_Card" if header_text_type == "blessings" else "Option1B_Chandelier_JoinUs_Wedding_Reception_Card"

    out_png = os.path.join(base_dir, f'{prefix}_preview.png')
    im1.save(out_png, quality=95)

    out_pdf = os.path.join(base_dir, f'{pdf_name}.pdf')
    c = canvas.Canvas(out_pdf, pagesize=(w, h))
    c.drawImage(out_png, 0, 0, width=w, height=h)
    btn_bx0, btn_by0, btn_bx1, btn_by1 = 150, 877, 420, 919
    c.linkURL("https://ten5.github.io/wedding-planning/", (btn_bx0, h - btn_by1, btn_bx1, h - btn_by0), relative=0)
    c.save()

    shutil.copyfile(out_pdf, os.path.join(repo_public, f'{pdf_name}.pdf'))
    print(f"{pdf_name} generated successfully")

make_card_fusion("join_us")
make_card_fusion("blessings")
make_card_t1_deep("blessings")
make_card_t1_deep("join_us")
