#!/usr/bin/env python3
"""Generate beautiful static story pages (stories/<slug>.html) from plans.

Story .md files have no front matter, so Jekyll serves them as raw text.
This generator renders each plan into a fully styled standalone HTML page
instead — without touching the .md files. Idempotent: rerun any time.

Usage: build_story_pages.py --lang en|hi --repo ~/workspace/kids-book-videos
"""
import argparse
import html
import json
import os

SITE = {
    "en": {
        "base": "/kids-book-videos",
        "title": "The Big Bedtime Storybook",
        "home_emoji": "🌙",
        "moral_label": "Tonight's gentle lesson",
        "pdf_cta": "Download this story as an illustrated PDF",
        "back": "← Back to all stories",
        "foot": "The Big Bedtime Storybook — cozy tales for ages 4–7.",
        "desc": "a cozy bedtime story",
    },
    "hi": {
        "base": "/kids-book-videos-hindi",
        "title": "मीठे सपनों की कहानियाँ",
        "home_emoji": "🌙",
        "moral_label": "आज की प्यारी सीख",
        "pdf_cta": "इस कहानी की सचित्र PDF डाउनलोड करें",
        "back": "← सभी कहानियों पर वापस जाएँ",
        "foot": "मीठे सपनों की कहानियाँ — 4–7 साल के बच्चों के लिए।",
        "desc": "एक प्यारी सुलाने वाली कहानी",
    },
}

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site}</title>
<meta name="description" content="{title} — {desc}.">
<script src="{base}/auth.js"></script>
<link rel="stylesheet" href="../assets/css/storybook.css">
</head>
<body class="storybook">
<nav class="story-topbar">
  <a class="home-link" href="../">{emoji} {site}</a>
</nav>
<article class="story">
  <h1>{title}</h1>
  <p class="age"><em>{age}</em></p>
  <hr>
{paras}
  <hr>
  <p class="moral">💛 <strong>{moral_label}:</strong> {moral}</p>
  <div class="story-pdf-cta">
    <a href="../book/stories/{slug}.pdf">📕 {pdf_cta}</a>
  </div>
</article>
<footer class="site-foot">
  <div class="hearts">🌙 📚 ✨</div>
  <p><a href="../" style="color:#8a7bb8">{back}</a><br>{foot}</p>
</footer>
</body>
</html>
"""


def build(lang, repo):
    s = SITE[lang]
    plans_dir = os.path.join(repo, "book", "colorful-plans")
    stories_dir = os.path.join(repo, "stories")
    n = 0
    for fn in sorted(os.listdir(plans_dir)):
        if not fn.endswith(".json"):
            continue
        p = json.load(open(os.path.join(plans_dir, fn), encoding="utf-8"))
        slug = p["slug"]
        paras = "\n".join(
            "  <p>" + html.escape(x) + "</p>"
            for sc in p["scenes"] for x in sc["paragraphs"]
        )
        page = PAGE.format(
            lang=lang, base=s["base"], emoji=s["home_emoji"], site=html.escape(s["title"]),
            title=html.escape(p["title"]), age=html.escape(p.get("age", "")),
            paras=paras, moral_label=s["moral_label"], moral=html.escape(p["moral"]),
            slug=slug, pdf_cta=s["pdf_cta"], back=s["back"], foot=s["foot"],
            desc=s["desc"],
        )
        with open(os.path.join(stories_dir, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
        n += 1
    print(f"[{lang}] story pages written: {n}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True, choices=["en", "hi"])
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    build(a.lang, a.repo)
