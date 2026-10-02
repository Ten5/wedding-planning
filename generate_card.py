import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def create_card():
    base_path = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11/page1_pure_invitation_artwork_1785366164192.jpg'
    img = Image.open(base_path).convert('RGB')
    w, h = img.size # 768 x 1376

    # Clean the center area from y=260 to y=1080
    arr = np.array(img)
    clean_box_top = 260
    clean_box_bottom = 1085
    
    bg_mean = np.array([250.6, 247.5, 236.8])
    noise = np.random.normal(0, 1.5, (clean_box_bottom - clean_box_top, w, 3))
    clean_bg = np.clip(bg_mean + noise, 0, 255).astype(np.uint8)
    arr[clean_box_top:clean_box_bottom, :] = clean_bg

    img_clean = Image.fromarray(arr)
    mask = Image.new('L', (w, h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rectangle([0, clean_box_top + 10, w, clean_box_bottom - 10], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(8))

    img_result = Image.composite(img_clean, Image.open(base_path).convert('RGB'), mask)
    draw = ImageDraw.Draw(img_result)

    # Fonts
    font_vibes_path = '/Users/ten5/Documents/Github/wedding-planning/fonts/GreatVibes-Regular.ttf'
    font_cinzel_path = '/Users/ten5/Documents/Github/wedding-planning/fonts/Cinzel-Regular.ttf'
    font_georgia_path = '/System/Library/Fonts/Supplemental/Georgia.ttf'
    font_georgia_b_path = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
    font_georgia_i_path = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'

    font_modern_header = ImageFont.truetype(font_cinzel_path, 25)
    font_names = ImageFont.truetype(font_vibes_path, 76)
    font_hashtag = ImageFont.truetype(font_georgia_b_path, 26)
    font_date = ImageFont.truetype(font_cinzel_path, 23)
    font_event_title = ImageFont.truetype(font_georgia_b_path, 21)
    font_event_time = ImageFont.truetype(font_georgia_i_path, 19)
    font_venue = ImageFont.truetype(font_georgia_b_path, 21)
    font_rsvp_btn = ImageFont.truetype(font_cinzel_path, 19)
    font_rsvp_url = ImageFont.truetype(font_georgia_path, 18)

    # Colors
    GOLD_DARK = (136, 92, 36)
    GOLD_MED = (156, 114, 48)
    TEXT_DARK = (60, 42, 32)
    DIVIDER_COLOR = (200, 168, 122)

    def draw_centered_text(y, text, font, fill, shadow=None):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (w - tw) / 2
        if shadow:
            draw.text((x + shadow[0], y + shadow[1]), text, font=font, fill=shadow[2])
        draw.text((x, y), text, font=font, fill=fill)
        return y + (bbox[3] - bbox[1])

    # 1. Header: ARE GETTING MARRIED!
    y = 300
    draw_centered_text(y, "ARE GETTING MARRIED!", font_modern_header, GOLD_DARK, shadow=(1, 1, (230, 215, 195)))

    # 2. Couple Names: Tarunima & Subhayu
    y = 356
    draw_centered_text(y, "Tarunima & Subhayu", font_names, GOLD_DARK, shadow=(1, 2, (215, 195, 170)))

    # 3. Hashtag: #DoRiTales (mixed case preserved)
    y = 458
    draw_centered_text(y, "#DoRiTales", font_hashtag, GOLD_MED, shadow=(1, 1, (230, 215, 195)))

    # Divider ornament 1
    y = 510
    draw.line([(w/2 - 90, y), (w/2 - 20, y)], fill=DIVIDER_COLOR, width=1)
    draw.ellipse([(w/2 - 4, y - 4), (w/2 + 4, y + 4)], fill=GOLD_MED)
    draw.line([(w/2 + 20, y), (w/2 + 90, y)], fill=DIVIDER_COLOR, width=1)

    # 4. EVENT 1: WEDDING CEREMONY
    y = 548
    draw_centered_text(y, "THURSDAY, NOVEMBER 12, 2026", font_date, GOLD_DARK)
    y = 584
    draw_centered_text(y, "Wedding Ceremony • 2:00 PM onwards", font_event_title, TEXT_DARK)
    y = 616
    draw_centered_text(y, "Amber India • Los Altos, California", font_venue, (85, 55, 35))

    # Divider ornament 2
    y = 672
    draw.line([(w/2 - 60, y), (w/2 + 60, y)], fill=DIVIDER_COLOR, width=1)

    # 5. EVENT 2: GRAND RECEPTION
    y = 705
    draw_centered_text(y, "FRIDAY, NOVEMBER 13, 2026", font_date, GOLD_DARK)
    y = 741
    draw_centered_text(y, "Grand Reception • 5:00 PM onwards", font_event_title, TEXT_DARK)
    y = 773
    draw_centered_text(y, "North Park • San Jose, California", font_venue, (85, 55, 35))

    # Divider ornament 3
    y = 828
    draw.line([(w/2 - 90, y), (w/2 - 20, y)], fill=DIVIDER_COLOR, width=1)
    draw.ellipse([(w/2 - 4, y - 4), (w/2 + 4, y + 4)], fill=GOLD_MED)
    draw.line([(w/2 + 20, y), (w/2 + 90, y)], fill=DIVIDER_COLOR, width=1)

    # 6. RSVP Pill & URL Link
    y_pill = 865
    pill_w = 480
    pill_h = 76
    pill_x0 = (w - pill_w) / 2
    pill_y0 = y_pill
    pill_x1 = pill_x0 + pill_w
    pill_y1 = pill_y0 + pill_h

    # Draw luxury rounded pill badge with soft gold border
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=38, fill=(255, 253, 248), outline=(195, 155, 95), width=2)
    
    # Text inside pill
    draw_centered_text(y_pill + 13, "RSVP & WEDDING DETAILS", font_rsvp_btn, GOLD_DARK)
    draw_centered_text(y_pill + 42, "ten5.github.io/wedding-planning", font_rsvp_url, (90, 75, 65))

    # Footer note
    y = 964
    draw_centered_text(y, "Formal Invitation to Follow", ImageFont.truetype(font_georgia_i_path, 18), (140, 115, 95))

    # Save output PNG
    out_png = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11/wedding_invitation_card_1page.png'
    img_result.save(out_png, quality=95)
    
    repo_png = '/Users/ten5/Documents/Github/wedding-planning/public/images/wedding_invitation_card_1page.png'
    img_result.save(repo_png, quality=95)
    print("PNG SAVED:", out_png)

    # -------------------------------------------------------------
    # GENERATE 1-PAGE PDF WITH ACTIVE CLICKABLE HYPERLINK
    # -------------------------------------------------------------
    pdf_out = '/Users/ten5/.gemini/antigravity/brain/f720da55-5f20-4c92-ab02-95ebeeae0f11/Tarunima_Subhayu_Wedding_Invitation.pdf'
    repo_pdf = '/Users/ten5/Documents/Github/wedding-planning/public/Tarunima_Subhayu_Wedding_Invitation.pdf'

    # PDF page dimensions: 768 x 1376 points (exact 1:1 match)
    c = canvas.Canvas(pdf_out, pagesize=(w, h))
    c.drawImage(out_png, 0, 0, width=w, height=h)

    # Clickable link box over the RSVP Pill badge
    # Note: Reportlab coordinates origin (0, 0) is at bottom-left!
    # pill_y0 from top is y_pill, so in PDF coords: y_bottom = h - pill_y1, y_top = h - pill_y0
    pdf_x0 = pill_x0
    pdf_y0 = h - pill_y1
    pdf_x1 = pill_x1
    pdf_y1 = h - pill_y0

    target_url = "https://ten5.github.io/wedding-planning/"
    c.linkURL(target_url, (pdf_x0, pdf_y0, pdf_x1, pdf_y1), relative=0)

    c.save()
    
    # Copy to repo public
    import shutil
    shutil.copyfile(pdf_out, repo_pdf)
    print("PDF SAVED WITH CLICKABLE LINK:", pdf_out)

if __name__ == '__main__':
    create_card()
