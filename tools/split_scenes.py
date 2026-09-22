#!/usr/bin/env python3
"""Split each story in stories/*.md into illustration scenes.

A scene = 1+ consecutive paragraphs, roughly 40-75 words, so each
illustration depicts a real story beat (dialogue one-liners merge into
their surrounding scene instead of getting pointless solo pictures).

Output: book/scene-plans/<slug>.json per story:
  {"slug":..., "title":..., "age":..., "moral":...,
   "scenes": [{"paragraphs": ["...", ...]}, ...]}

Re-runnable: overwrites the JSON plans.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "book"))
# reuse the parser from the big-book builder
import importlib.util

spec = importlib.util.spec_from_file_location(
    "build_pdf", os.path.join(BASE, "..", "book", "build_pdf.py"))
build_pdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_pdf)

STORIES_DIR = os.path.join(BASE, "..", "stories")
OUT_DIR = os.path.join(BASE, "..", "book", "scene-plans")

TARGET_MIN, TARGET_MAX = 40, 80


def split_scenes(paragraphs):
    """Group paragraph texts into scenes of ~TARGET_MIN-TARGET_MAX words."""
    scenes, cur, words = [], [], 0
    for p in paragraphs:
        pw = len(p.split())
        if cur and words >= TARGET_MIN and words + pw > TARGET_MAX:
            scenes.append(cur)
            cur, words = [], 0
        cur.append(p)
        words += pw
    if cur:
        scenes.append(cur)
    # merge a tiny trailing scene into the previous one
    if len(scenes) > 1:
        last_words = sum(len(p.split()) for p in scenes[-1])
        if last_words < 20:
            scenes[-2].extend(scenes[-1])
            scenes.pop()
    # merge a tiny leading scene into the next one
    if len(scenes) > 1:
        first_words = sum(len(p.split()) for p in scenes[0])
        if first_words < 20:
            scenes[1] = scenes[0] + scenes[1]
            scenes.pop(0)
    return scenes


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted(f for f in os.listdir(STORIES_DIR) if f.endswith(".md"))
    total_scenes = 0
    for fname in files:
        slug = fname[:-3]
        title, age, body, moral = build_pdf.parse_story(
            os.path.join(STORIES_DIR, fname))
        paras = [t for kind, t in body]  # keep reading order
        scenes = split_scenes(paras)
        total_scenes += len(scenes)
        plan = {
            "slug": slug,
            "title": title,
            "age": age,
            "moral": moral,
            "scenes": [{"paragraphs": s} for s in scenes],
        }
        with open(os.path.join(OUT_DIR, slug + ".json"), "w",
                  encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        print(f"{slug}: {len(scenes)} scenes")
    print(f"\n{len(files)} stories, {total_scenes} scenes total")


if __name__ == "__main__":
    main()
