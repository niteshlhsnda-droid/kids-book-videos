# 🤝 Contributing

Welcome! This is an **open repository** — anyone can contribute stories, art,
music, translations, or improvements. Everything original here is shared under
[CC BY 4.0](LICENSE.md), so your contributions will be too.

## What you can contribute

- **Stories** — original bedtime tales for ages 4–7 (300–500 words, gentle tone,
  one clear moral). See `stories/` for the format.
- **Adaptations** — retellings of public-domain or CC BY / CC BY-SA tales.
  Pick from [`sources/adaptation-queue.md`](sources/adaptation-queue.md) or
  suggest new entries (with source URL + license).
- **Narration scripts** — read-aloud versions with pacing cues (`narration-scripts/`).
- **Illustrations** — cozy, kid-safe art to accompany stories (`assets/`).
- **Music** — original lullabies and background pieces (`assets/music/`).
- **Translations** — stories in more languages are always welcome.

## The rules

1. **Only contribute what is free to share.** Your own original work, or works
   verifiably in the public domain / under CC BY / CC BY-SA. Never submit
   copyrighted text, art, or music you don't own. No NC or ND material.
2. **Credit everything.** Adaptations must include a credits block: original
   title, author, illustrator, source URL, and license.
3. **Keep it kid-safe.** Ages 4–7: gentle language, no scary or violent content,
   kind morals.
4. **One story per pull request**, named in lowercase with dashes
   (e.g. `stories/granny-and-the-talking-drum.md`).

## How the daily pipeline works

A scheduled job publishes one story + narrated video every day, alternating
between **original** tales and **adapted** classics from the adaptation queue.
Every video is verified (picture, sound, length) before it goes live, and every
adaptation ships with a credits file. See `tools/` for the pipeline scripts.

## Questions?

Open an issue — we're friendly. 🌙
