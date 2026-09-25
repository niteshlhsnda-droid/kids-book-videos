#!/usr/bin/env python3
"""Generate the playful storybook homepage (index.md) from the final plans.

Reads book/colorful-plans/<slug>.json for every story, groups cards into
categories, and writes a fully static index.md (HTML + client-side search).
Idempotent: re-running produces the same file; new stories appear on rerun.

Usage: build_homepage.py --lang en|hi --repo ~/workspace/kids-book-videos
"""
import argparse
import html
import json
import os

NIGHT_SLUGS = [
    "2026-09-21-willa-the-bunny-and-the-moonflower", "a-blanket-of-stars",
    "counting-stars-to-sleep", "faye-the-deer-fawns-firefly-dance",
    "hoots-sleepy-rounds", "koda-the-koala-and-the-sleepy-leaf",
    "marnie-the-mole-hears-the-stars", "moonbeam-mail", "mossys-moon-blanket",
    "night-sounds-lullaby", "sun-and-moon-take-turns", "sunny-says-goodnight",
    "teddys-midnight-picnic", "the-brave-little-firefly", "the-dream-boat",
    "the-dream-collectors-pillow", "the-dream-garden", "the-firefly-dance",
    "the-goodnight-zoo", "the-lullaby-river", "the-moon-shares-its-light",
    "the-night-bakery", "the-night-train", "the-sleepy-lighthouse",
    "the-winds-bedtime-song", "where-do-birds-sleep",
]

EMOJI_MAP = [
    ("moon", "🌙"), ("star", "⭐"), ("firefly", "✨"), ("lullaby", "🎵"),
    ("bear", "🐻"), ("bunny", "🐰"), ("rabbit", "🐰"), ("kitten", "🐱"),
    ("cat", "🐱"), ("puppy", "🐶"), ("dog", "🐶"), ("duck", "🦆"),
    ("frog", "🐸"), ("owl", "🦉"), ("hoot", "🦉"), ("koala", "🐨"),
    ("penguin", "🐧"), ("butterfly", "🦋"), ("bee", "🐝"), ("ant", "🐜"),
    ("snail", "🐌"), ("train", "🚂"), ("boat", "⛵"), ("balloon", "🎈"),
    ("kite", "🪁"), ("snow", "❄️"), ("rain", "🌧️"), ("cloud", "☁️"),
    ("garden", "🌸"), ("flower", "🌸"), ("tree", "🌳"), ("zoo", "🦁"),
    ("lion", "🦁"), ("mouse", "🐭"), ("crow", "🐦"), ("bird", "🐦"),
    ("hare", "🐇"), ("tortoise", "🐢"), ("turtle", "🐢"), ("crab", "🦀"),
    ("otter", "🦦"), ("squirrel", "🐿️"), ("mole", "🦔"), ("hedgehog", "🦔"),
    ("pig", "🐷"), ("lamb", "🐑"), ("pumpkin", "🎃"), ("parade", "🎉"),
    ("bakery", "🍞"), ("picnic", "🧺"), ("dream", "💭"), ("sleep", "😴"),
    ("wind", "🍃"), ("wave", "🌊"), ("puddle", "💧"),
]

STRINGS = {
    "en": {
        "html_lang": "en",
        "site_title": "The Big Bedtime Storybook",
        "tagline": "109 bedtime stories for ages 4–7 — 103 original tales plus 6 timeless classics.",
        "search_ph": "🔍 Search stories…",
        "stats": "📚 109 stories &nbsp;·&nbsp; 📕 free illustrated PDFs &nbsp;·&nbsp; 🌙 new stories daily",
        "whole_book": "📖 Read the whole book in one page",
        "banner_flag": "✨ FEATURED BOOK",
        "banner_title": "🌙 The Night-Time Storybook",
        "banner_text": "26 dreamy bedtime stories in one beautiful book — perfect for lights-out reading.",
        "banner_pdf": "book/night-time-stories.pdf",
        "no_results": "😴 No stories found — try another word!",
        "read": "📖 Read",
        "pdf": "📕 PDF",
        "sections": [
            ("night", "🌙 Night-Time Stories",
             "Gentle tales of moons, stars, fireflies and sleepy friends."),
            ("bedtime", "📚 Bedtime Tales",
             "Original cozy stories for ages 4–7."),
            ("classic", "🏛️ Classic Tales",
             "Timeless tales from Aesop's fables and classic fairy tales, retold for bedtime."),
        ],
        "daily": "New stories added daily.",
    },
    "hi": {
        "html_lang": "hi",
        "site_title": "मीठे सपनों की कहानियाँ",
        "tagline": "4–7 साल के बच्चों के लिए 109 हिंदी सुलाने वाली कहानियाँ — 103 मूल कहानियाँ और 6 कालजयी क्लासिक कहानियाँ।",
        "search_ph": "🔍 कहानी खोजें…",
        "stats": "📚 109 कहानियाँ &nbsp;·&nbsp; 📕 मुफ़्त सचित्र PDF &nbsp;·&nbsp; 🌙 रोज़ नई कहानियाँ",
        "whole_book": "",
        "banner_flag": "✨ ख़ास किताब",
        "banner_title": "🌙 रात की कहानियों की किताब",
        "banner_text": "एक ही खूबसूरत किताब में 26 सपनीली सुलाने वाली कहानियाँ — बत्ती बुझाकर पढ़ने के लिए बिल्कुल सही।",
        "banner_pdf": "book/night-time-stories.pdf",
        "no_results": "😴 कोई कहानी नहीं मिली — कोई और शब्द आज़माएँ!",
        "read": "📖 पढ़ें",
        "pdf": "📕 PDF",
        "sections": [
            ("night", "🌙 रात की कहानियाँ",
             "चाँद, तारों, जुगनुओं और निंदिया के दोस्तों की प्यारी कहानियाँ।"),
            ("bedtime", "📚 सोने की कहानियाँ",
             "4–7 साल के बच्चों के लिए मूल प्यारी कहानियाँ।"),
            ("classic", "🏛️ क्लासिक कहानियाँ",
             "पंचतंत्र और लोककथाओं की कालजयी कहानियाँ — सुलाने के अंदाज़ में।"),
        ],
        "daily": "रोज़ नई कहानियाँ जुड़ती हैं।",
    },
}

SERIES_KEY = {"en": {"Bedtime Tales": "bedtime", "Classic Tales": "classic"},
              "hi": {"सोने की कहानियाँ": "bedtime", "क्लासिक कहानियाँ": "classic"}}


def card_emoji(slug):
    for kw, em in EMOJI_MAP:
        if kw in slug:
            return em
    return "🌙"


def card_html(slug, title, s):
    t = html.escape(title)
    em = card_emoji(slug)
    search = html.escape((title + " " + slug).lower())
    art = f"book/colorful-illustrations/{slug}/scene-01-cover.webp"
    return f"""<article class="story-card" data-search="{search}">
  <a class="card-art" href="stories/{slug}.html" aria-label="{t}">
    <span class="fallback" aria-hidden="true">{em}</span>
    <img src="{art}" alt="{t} — cover art" loading="lazy" onerror="this.style.display='none'">
  </a>
  <div class="card-body">
    <h3><a href="stories/{slug}.html">{t}</a></h3>
    <div class="card-actions">
      <a class="btn btn-read" href="stories/{slug}.html">{s['read']}</a>
      <a class="btn btn-pdf" href="book/stories/{slug}.pdf">{s['pdf']}</a>
    </div>
  </div>
</article>"""


SEARCH_JS = """<script>
(function () {
  var input = document.getElementById("story-search");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".story-card"));
  var sections = Array.prototype.slice.call(document.querySelectorAll("section.category"));
  var empty = document.getElementById("no-results");
  var count = document.getElementById("result-count");
  input.addEventListener("input", function () {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {
      var hit = !q || c.getAttribute("data-search").indexOf(q) !== -1;
      c.style.display = hit ? "" : "none";
      if (hit) shown++;
    });
    sections.forEach(function (sec) {
      var any = Array.prototype.some.call(
        sec.querySelectorAll(".story-card"),
        function (c) { return c.style.display !== "none"; });
      sec.style.display = any ? "" : "none";
    });
    empty.style.display = shown ? "none" : "block";
    count.textContent = q ? (" — " + shown + " found") : "";
  });
})();
</script>"""


def build(lang, repo):
    s = STRINGS[lang]
    plans_dir = os.path.join(repo, "book", "colorful-plans")
    plans = {}
    for fn in os.listdir(plans_dir):
        if fn.endswith(".json"):
            p = json.load(open(os.path.join(plans_dir, fn), encoding="utf-8"))
            plans[p["slug"]] = p
    key = SERIES_KEY[lang]
    groups = {"night": [], "bedtime": [], "classic": []}
    for slug in NIGHT_SLUGS:
        if slug in plans:
            groups["night"].append(slug)
    for slug, p in plans.items():
        g = key.get(p.get("series", ""), "bedtime")
        groups[g].append(slug)
    for g in groups:
        groups[g] = sorted(set(groups[g]), key=lambda sl: plans[sl]["title"].lower())

    whole = (f'<p style="margin-top:22px"><a class="btn btn-read" style="flex:none;padding:13px 34px" '
             f'href="book/bedtime-storybook.html">{s["whole_book"]}</a></p>') if s["whole_book"] else ""

    parts = [f"""---
layout: default
title: {s['site_title']}
---

<div class="hero">
  <span class="moon">🌙</span>
  <h1>{html.escape(s['site_title'])}</h1>
  <p class="tagline">{html.escape(s['tagline'])}</p>
  <div class="search-wrap">
    <input id="story-search" type="search" placeholder="{html.escape(s['search_ph'])}" aria-label="search">
    <span class="mag">🔍</span>
  </div>
  <p class="stats">{s['stats']}<span id="result-count"></span></p>
  {whole}
</div>

<div class="book-banner">
  <a href="{s['banner_pdf']}">
    <span class="cover-emoji">🌙</span>
    <span>
      <span class="flag">{s['banner_flag']}</span>
      <h2>{s['banner_title']}</h2>
      <p>{s['banner_text']}</p>
    </span>
    <span class="go">→</span>
  </a>
</div>

<main class="shelf">
<div class="no-results" id="no-results">{s['no_results']}</div>
"""]
    for gid, heading, desc in s["sections"]:
        cards = "\n".join(card_html(sl, plans[sl]["title"], s) for sl in groups[gid])
        parts.append(f"""<section class="category cat-{gid}" id="cat-{gid}">
  <h2>{heading}</h2>
  <p class="desc">{html.escape(desc)}</p>
  <div class="cards">
{cards}
  </div>
</section>
""")
    parts.append("</main>\n" + SEARCH_JS + "\n")
    out = os.path.join(repo, "index.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    total = sum(len(v) for v in groups.values())
    print(f"[{lang}] index.md written: {len(plans)} stories, "
          f"night={len(groups['night'])} bedtime={len(groups['bedtime'])} classic={len(groups['classic'])}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True, choices=["en", "hi"])
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    build(a.lang, a.repo)
