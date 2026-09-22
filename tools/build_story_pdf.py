#!/usr/bin/env python3
"""Build one illustrated PDF per story: each scene's paragraphs paired
with the illustration depicting that scene.

Usage:
    python3 build_story_pdf.py <slug>          # build one story
    python3 build_story_pdf.py --all           # build every story

Inputs:
    book/scene-plans/<slug>.json               (from split_scenes.py)
    book/scene-illustrations/<slug>/scene-NN.jpg  (one per scene, 1-based)
    book/illustrations/<slug>.jpg              (title-page art, optional)

Output:
    book/stories/<slug>.pdf

Scene images are downscaled to max 1000px wide (JPEG q68) so each PDF
stays small enough for GitHub Pages downloads.
Re-runnable: overwrites the output PDF.
"""
import glob
import json
import os
import sys
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, Image, KeepTogether,
)

BASE = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.normpath(os.path.join(BASE, "..", "book"))
PLANS_DIR = os.path.join(BOOK_DIR, "scene-plans")
SCENE_IMG_DIR = os.path.join(BOOK_DIR, "scene-illustrations")
TITLE_IMG_DIR = os.path.join(BOOK_DIR, "illustrations")
OUT_DIR = os.path.join(BOOK_DIR, "stories")
BUILD_IMG_DIR = os.path.join(BOOK_DIR, "stories", ".build-img")

PAGE_W, PAGE_H = 6 * inch, 9 * inch
MARGIN_LR = 0.85 * inch
MARGIN_TB = 0.75 * inch
USABLE_W = PAGE_W - 2 * MARGIN_LR

MIDNIGHT = HexColor("#141B34")
GOLD = HexColor("#E8B64C")
DIMGOLD = HexColor("#8F7132")
INK = HexColor("#26221C")
WARMGRAY = HexColor("#6E665C")
MORALGRAY = HexColor("#4A443C")
CREAM = HexColor("#F7F2E7")
HAIRLINE = HexColor("#D8D2C4")

FONT_DIR = "/usr/share/fonts/truetype/noto"
for _name, _file in [("NotoSerif", "NotoSerif-Regular.ttf"),
                     ("NotoSerif-Bold", "NotoSerif-Bold.ttf"),
                     ("NotoSerif-Italic", "NotoSerif-Italic.ttf"),
                     ("NotoSerif-BoldItalic", "NotoSerif-BoldItalic.ttf")]:
    try:
        pdfmetrics.registerFont(TTFont(_name, os.path.join(FONT_DIR, _file)))
    except Exception:
        pass

sTitle = ParagraphStyle("T", fontName="NotoSerif-Bold", fontSize=24,
                        leading=30, textColor=MIDNIGHT, alignment=TA_CENTER,
                        spaceAfter=6)
sAge = ParagraphStyle("A", fontName="NotoSerif-Italic", fontSize=10,
                      leading=14, textColor=WARMGRAY, alignment=TA_CENTER,
                      spaceAfter=12)
sBody = ParagraphStyle("B", fontName="NotoSerif", fontSize=11.5,
                       leading=17.5, textColor=INK, alignment=TA_JUSTIFY,
                       firstLineIndent=18, spaceAfter=7)
sBodyFirst = ParagraphStyle("B1", parent=sBody, firstLineIndent=0)
sMoral = ParagraphStyle("M", fontName="NotoSerif-Italic", fontSize=11,
                        leading=16, textColor=MORALGRAY, alignment=TA_CENTER,
                        spaceBefore=10, spaceAfter=4)
sEnd = ParagraphStyle("E", fontName="NotoSerif-Bold", fontSize=12,
                      leading=16, textColor=MIDNIGHT, alignment=TA_CENTER,
                      spaceBefore=14)
sBrand = ParagraphStyle("Br", fontName="NotoSerif", fontSize=9,
                        leading=12, textColor=WARMGRAY, alignment=TA_CENTER)


def prep_image(src, dst, max_w=1000):
    """Downscale to a web-friendly JPEG for the PDF."""
    im = PILImage.open(src).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)),
                       PILImage.LANCZOS)
    im.save(dst, "JPEG", quality=68, optimize=True)
    return dst


def scene_image_path(slug, idx):
    """1-based scene index -> illustration path (jpg/png/webp)."""
    d = os.path.join(SCENE_IMG_DIR, slug)
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = os.path.join(d, f"scene-{idx:02d}.{ext}")
        if os.path.exists(p):
            return p
    return None


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("NotoSerif-Italic", 8)
    canvas.setFillColor(WARMGRAY)
    canvas.drawCentredString(PAGE_W / 2, 0.55 * inch,
                             f"{doc.story_title}  ·  {doc.page}")
    # hairline
    canvas.setStrokeColor(HAIRLINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_LR, 0.72 * inch, PAGE_W - MARGIN_LR, 0.72 * inch)
    canvas.restoreState()


def title_page_art(slug):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = os.path.join(TITLE_IMG_DIR, slug + "." + ext)
        if os.path.exists(p):
            return p
    return None


def build_one(slug):
    plan_path = os.path.join(PLANS_DIR, slug + ".json")
    if not os.path.exists(plan_path):
        return f"{slug}: no scene plan"
    plan = json.load(open(plan_path, encoding="utf-8"))
    scenes = plan["scenes"]

    missing = [i + 1 for i in range(len(scenes))
               if scene_image_path(slug, i + 1) is None]
    if missing:
        return f"{slug}: MISSING illustrations for scenes {missing}"

    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(BUILD_IMG_DIR, exist_ok=True)
    out_pdf = os.path.join(OUT_DIR, slug + ".pdf")

    doc = BaseDocTemplate(out_pdf, pagesize=(PAGE_W, PAGE_H),
                          leftMargin=MARGIN_LR, rightMargin=MARGIN_LR,
                          topMargin=MARGIN_TB, bottomMargin=MARGIN_TB,
                          title=plan["title"],
                          author="Kids Book Videos")
    doc.story_title = plan["title"]
    frame = Frame(MARGIN_LR, MARGIN_TB, USABLE_W,
                  PAGE_H - 2 * MARGIN_TB, id="main")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=footer)])
    story = []

    # ---- title page ----
    story.append(Spacer(1, 0.9 * inch))
    story.append(Paragraph(escape(plan["title"]), sTitle))
    story.append(Spacer(1, 0.12 * inch))
    # gold rule
    story.append(Paragraph('<font color="#E8B64C">◆</font>', sBrand))
    if plan.get("age"):
        story.append(Paragraph(escape(plan["age"]), sAge))
    art = title_page_art(slug)
    if art:
        dst = os.path.join(BUILD_IMG_DIR, slug + "-title.jpg")
        prep_image(art, dst, max_w=1000)
        im = PILImage.open(dst)
        w = USABLE_W
        h = w * im.height / im.width
        max_h = 4.2 * inch
        if h > max_h:
            h = max_h
            w = h * im.width / im.height
        story.append(Image(dst, width=w, height=h))
        story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Kids Book Videos", sBrand))
    story.append(PageBreak())

    # ---- scenes: picture + the paragraphs it depicts ----
    for idx, scene in enumerate(scenes, start=1):
        img_src = scene_image_path(slug, idx)
        dst = os.path.join(BUILD_IMG_DIR, f"{slug}-scene-{idx:02d}.jpg")
        prep_image(img_src, dst, max_w=1000)
        im = PILImage.open(dst)
        w = USABLE_W
        h = w * im.height / im.width
        max_h = 3.4 * inch
        if h > max_h:
            h = max_h
            w = h * im.width / im.height
        parts = [Image(dst, width=w, height=h), Spacer(1, 0.14 * inch)]
        for j, para in enumerate(scene["paragraphs"]):
            st = sBodyFirst if (idx == 1 and j == 0) else sBody
            parts.append(Paragraph(escape(para), st))
        story.append(KeepTogether(parts))

    # ---- moral + end ----
    if plan.get("moral"):
        moral = plan["moral"]
        rest = moral[6:].strip() if moral.lower().startswith("moral:") \
            else moral
        story.append(Paragraph(
            '<font name="NotoSerif-BoldItalic">Moral:</font> ' + escape(rest),
            sMoral))
    story.append(Paragraph("The End", sEnd))

    doc.build(story)
    size = os.path.getsize(out_pdf)
    return f"{slug}: OK ({size:,} bytes, {len(scenes)} scenes)"


def main():
    if len(sys.argv) < 2:
        print("usage: build_story_pdf.py <slug> | --all")
        sys.exit(1)
    if sys.argv[1] == "--all":
        plans = sorted(glob.glob(os.path.join(PLANS_DIR, "*.json")))
        fails = []
        for p in plans:
            slug = os.path.basename(p)[:-5]
            try:
                res = build_one(slug)
            except Exception as e:  # noqa: BLE001
                res = f"{slug}: ERROR {e}"
            print(res)
            if "OK" not in res:
                fails.append(slug)
        print(f"\nbuilt {len(plans) - len(fails)}/{len(plans)}")
        if fails:
            print("FAILED:", ", ".join(fails))
            sys.exit(2)
    else:
        print(build_one(sys.argv[1]))


if __name__ == "__main__":
    main()
