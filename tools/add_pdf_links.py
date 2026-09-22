#!/usr/bin/env python3
"""Append an illustrated-PDF download link to every story page source.

For each stories/<slug>.md without an existing PDF link, appends:

    ---

    📥 [Download this story as an illustrated PDF](../book/stories/<slug>.pdf)

The rendered story pages (stories/<slug>.html) then carry the download.
Re-runnable: skips stories that already have the link.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
STORIES_DIR = os.path.normpath(os.path.join(BASE, "..", "stories"))


def main():
    files = sorted(f for f in os.listdir(STORIES_DIR) if f.endswith(".md"))
    added, skipped = 0, 0
    for fname in files:
        slug = fname[:-3]
        path = os.path.join(STORIES_DIR, fname)
        text = open(path, encoding="utf-8").read()
        marker = f"book/stories/{slug}.pdf"
        if marker in text:
            skipped += 1
            continue
        if not text.endswith("\n"):
            text += "\n"
        text += ("\n---\n\n"
                 f"📥 [Download this story as an illustrated PDF]"
                 f"(../book/stories/{slug}.pdf)\n")
        open(path, "w", encoding="utf-8").write(text)
        added += 1
        print(f"{slug}: link added")
    print(f"\nadded {added}, skipped {skipped} (of {len(files)})")


if __name__ == "__main__":
    main()
