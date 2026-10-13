import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

bgs = {
    'Option 1': {
        'path': '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11/bengali_card_bg1_1790904744639.jpg',
        'out_pdf': 'Reception_Invitation_Option1.pdf',
        'out_png': 'reception_card_option1_preview.png',
        'y_start': 695,
        'name_size': 80
    },
    'Option 3': {
        'path': '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11/bengali_card_bg3_1790904838923.jpg',
        'out_pdf': 'Reception_Invitation_Option3.pdf',
        'out_png': 'reception_card_option3_preview.png',
        'y_start': 710,
        'name_size': 84
    }
}

font_vibes_path = '/Users/ten5/Documents/Github/wedding-planning/fonts/GreatVibes-Regular.ttf'
font_cinzel_path = '/Users/ten5/Documents/Github/wedding-planning/fonts/Cinzel-Regular.ttf'
font_georgia_b_path = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'

def build_reception_card(cfg):
    img = Image.open(cfg['path']).convert('RGB')
    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)
    w, h = 1080, 1920

    GOLD_DARK = (136, 90, 32)
    GOLD_MED = (162, 116, 45)
    TEXT_DARK = (58, 38, 28)
    TEXT_VENUE = (82, 50, 32)
    DIVIDER = (205, 168, 112)

    f_header1 = ImageFont.truetype(font_cinzel_path, 26)
    f_header2 = ImageFont.truetype(font_cinzel_path, 26)
    f_names = ImageFont.truetype(font_vibes_path, cfg['name_size'])
    f_date = ImageFont.truetype(font_cinzel_path, 29)
    f_time = ImageFont.truetype(font_georgia_b_path, 26)
    f_venue = ImageFont.truetype(font_georgia_b_path, 28)
    f_rsvp = ImageFont.truetype(font_cinzel_path, 23)

    def draw_centered(y, text, font, fill, shadow=None):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bbox[3] - bbox[1])

    y = cfg['y_start']

    # 1. Header: JOIN US IN CELEBRATING THE WEDDING RECEPTION OF
    draw_centered(y, "JOIN US IN CELEBRATING", f_header1, GOLD_DARK, shadow=(1, 1, (230, 215, 195)))
    y += 42
    draw_centered(y, "THE WEDDING RECEPTION OF", f_header2, GOLD_DARK, shadow=(1, 1, (230, 215, 195)))

    # 2. Couple Names: Tarunima & Subhayu
    y += 62
    draw_centered(y, "Tarunima & Subhayu", f_names, GOLD_DARK, shadow=(2, 2, (215, 195, 165)))

    # 3. Divider Ornament 1
    y += 125
    draw.line([(w/2 - 110, y), (w/2 - 22, y)], fill=DIVIDER, width=2)
    draw.ellipse([(w/2 - 5, y - 5), (w/2 + 5, y + 5)], fill=GOLD_MED)
    draw.line([(w/2 + 22, y), (w/2 + 110, y)], fill=DIVIDER, width=2)

    # 4. Friday Reception Details ONLY
    y += 55
    draw_centered(y, "FRIDAY, NOVEMBER 13, 2026", f_date, GOLD_DARK)
    y += 48
    draw_centered(y, "5:00 PM onwards", f_time, TEXT_DARK)
    y += 44
    draw_centered(y, "North Park • San Jose, California", f_venue, TEXT_VENUE)

    # 5. Divider Ornament 2
    y += 65
    draw.line([(w/2 - 110, y), (w/2 - 22, y)], fill=DIVIDER, width=2)
    draw.ellipse([(w/2 - 5, y - 5), (w/2 + 5, y + 5)], fill=GOLD_MED)
    draw.line([(w/2 + 22, y), (w/2 + 110, y)], fill=DIVIDER, width=2)

    # 6. Clickable RSVP & Wedding Details Badge
    y += 55
    pill_w = 500
    pill_h = 80
    pill_x0 = (w - pill_w) / 2
    pill_y0 = y
    pill_x1 = pill_x0 + pill_w
    pill_y1 = pill_y0 + pill_h

    draw.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=40, fill=(255, 253, 248), outline=(195, 155, 95), width=2)
    draw_centered(pill_y0 + 25, "RSVP & WEDDING DETAILS", f_rsvp, GOLD_DARK)

    # Save preview PNG
    artifact_dir = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11'
    out_png = os.path.join(artifact_dir, cfg['out_png'])
    img.save(out_png, quality=95)

    # Save Clickable PDF
    out_pdf = os.path.join(artifact_dir, cfg['out_pdf'])
    repo_pdf = os.path.join('/Users/ten5/Documents/Github/wedding-planning/public', cfg['out_pdf'])

    c = canvas.Canvas(out_pdf, pagesize=(w, h))
    c.drawImage(out_png, 0, 0, width=w, height=h)

    # Embed clickable link directly over the RSVP & Wedding Details pill
    pdf_x0 = pill_x0
    pdf_y0 = h - pill_y1
    pdf_x1 = pill_x1
    pdf_y1 = h - pill_y0
    c.linkURL("https://ten5.github.io/wedding-planning/", (pdf_x0, pdf_y0, pdf_x1, pdf_y1), relative=0)
    c.save()

    import shutil
    shutil.copyfile(out_pdf, repo_pdf)
    print(f"Created PDF: {out_pdf}")

for k, cfg in bgs.items():
    build_reception_card(cfg)
