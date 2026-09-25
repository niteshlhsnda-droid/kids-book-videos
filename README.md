# 📚🎬 Kids' Book Videos & Stories

A beginner-friendly project template for creating and publishing **original** children's stories and story videos — legally and safely. Everything here is yours to use, remix, and share.

**Who is this for?** Parents, teachers, storytellers, and creators who want to make bedtime stories and kids' videos without worrying about copyright strikes, takedowns, or legal trouble.

**The one golden rule of this project:**

> 🛡️ **Only publish what you created yourself, or what is clearly in the public domain.** If you didn't make it and you can't prove it's free to use — don't use it.

---

## ⭐ Featured story

**[Hoofy the Camel and the Helpful Hump](stories/2026-09-25-hoofy-the-camel-and-the-helpful-hump.md)** — An adapted classic (Rudyard Kipling's *Just So Stories*, public domain): a lazy camel who only says "Humph" gets a hump from the Spirit of the Desert — and discovers that helping others makes every journey lighter. *Moral: When everyone helps, no one's load is heavy.*

🎬 [Watch the narrated video](videos/2026-09-25-hoofy-the-camel-and-the-helpful-hump.mp4) · 📜 [Narration script](narration-scripts/2026-09-25-hoofy-the-camel-and-the-helpful-hump-script.md) · 🎵 [Lullaby](assets/music/2026-09-25-hoofy-the-camel-and-the-helpful-hump.mp3)

A new story + narrated video is published here **every day** — alternating between original tales and lovingly adapted public-domain / Creative Commons classics (always credited). Want to help? See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📚 Daily stories (newest first)

| Date | Story | Moral |
|------|-------|-------|
| 2026-09-25 | [Hoofy the Camel and the Helpful Hump](stories/2026-09-25-hoofy-the-camel-and-the-helpful-hump.md) (adapted — Kipling's *Just So Stories*, public domain) | When everyone helps, no one's load is heavy. |
| 2026-09-24 | [Bram the Badger and the Whispering Woods](stories/2026-09-24-bram-the-badger-and-the-whispering-woods.md) (original) | Saying your fear out loud makes it smaller — and walking beside a friend makes it disappear. |
| 2026-09-23 | [Tilly the Tortoise and the Racing Hare](stories/2026-09-23-tilly-the-tortoise-and-the-racing-hare.md) (adapted — Aesop's Fables, public domain) | Slow and steady, step by step, finishes the race. |
| 2026-09-22 | [Nia and the Sleepy Star](stories/2026-09-22-nia-and-the-sleepy-star.md) (original) | Kindness gives others the strength to shine again. |
| 2026-09-21 | [Willa the Bunny and the Moonflower](stories/2026-09-21-willa-the-bunny-and-the-moonflower.md) (original) | Patience makes sweet surprises even sweeter. |

---

---

## 📁 What's inside

```
kids-book-videos/
├── README.md                  ← you are here (the full guide)
├── LICENSE.md                 ← CC BY 4.0 — what others may do with your work
├── .gitignore                 ← keeps junk files out of the repo
│
├── stories/                   ← story texts in Markdown (easy to read & print)
│   ├── the-brave-little-firefly.md
│   └── pippas-big-rainy-day.md
│
├── narration-scripts/         ← read-aloud scripts with scene & pacing cues
│   └── the-brave-little-firefly-script.md
│
├── videos/                    ← finished MP4s, one per story
│   └── README.md              ← naming + export settings
│
└── assets/
    ├── thumbnails/            ← covers & thumbnails (JPG/PNG)
    └── music/                 ← background music + credit logs
```

**Why this layout?** Text, scripts, videos, and art each live in their own place, so a story can be read as a book, performed from its script, or watched as a video — without files getting mixed up.

---

## 🚀 Quick start (5 minutes)

1. **Read an example story** — open `stories/the-brave-little-firefly.md` to see the style: short sentences, gentle repetition, a kind moral.
2. **Read its narration script** — open `narration-scripts/the-brave-little-firefly-script.md` to see how a story becomes a read-aloud video script (scene cues, pauses, acting notes).
3. **Check the license** — everything original in this repo is shared under [CC BY 4.0](LICENSE.md): anyone may reuse it with credit.

Then follow the guides below to add your own.

---

## ✏️ How to add a new story

1. **Create a new file** in `stories/`, named in lowercase with dashes, e.g. `stories/granny-and-the-talking-drum.md`.
2. **Copy the format** of an example story:
   - A `# Title` at the top
   - An italic line with age range + reading time
   - The story itself: **300–500 words** for ages 4–7
   - A `---` divider, then the moral in italics
3. **Write kid-friendly:**
   - Short sentences. One idea per sentence.
   - Repetition is good ("glow… and glow… and glow") — kids love it.
   - Name feelings out loud ("Flick felt scared") — it teaches emotional words.
   - One clear, kind moral. No lectures.
   - Read it aloud once. If you stumble, simplify that sentence.
4. **Keep it original.** Write your own characters, your own plot. It's fine to be *inspired* by a theme (bravery, sharing), but never copy sentences, rhymes, or characters from published books, cartoons, or movies.
5. **Commit it:** `git add stories/your-story.md && git commit -m "Add story: Your Title" && git push`

---

## 🎙️ How to turn a story into a video

Follow these steps in order — each one has its own folder in this repo.

### Step 1 — Write the narration script
- Create `narration-scripts/your-story-script.md`, following the example script's format:
  - **Bold lines** = read aloud
  - *[Bracketed cues]* = scene changes, pauses, tone
  - *(Parentheses)* = acting notes (never read aloud)
- Mark pauses explicitly (`[Pause 2 seconds]`) — silence helps kids imagine.

### Step 2 — Record the voiceover
- Any phone voice recorder works. Record in a quiet room (a closet full of clothes is a great free sound booth).
- Read slowly, smile while you read, and leave the pauses in.
- Export as WAV or MP3.

### Step 3 — Create the visuals
Use **only** visuals you made or that are free to use:
- ✅ Your own drawings or paintings (photograph/scan them)
- ✅ AI images you generated yourself
- ✅ Public-domain / CC0 images (Pixabay, Unsplash, Pexels — verify each image's license page)
- ❌ Screenshots from cartoons, movies, or other YouTubers
- ❌ "Free" images from a random Google search

### Step 4 — Add music (carefully!)
- See `assets/music/README.md`. Short version: use music **you** made, or tracks from the **YouTube Audio Library** / trusted royalty-free libraries — and save a `-credit.txt` file for every track.
- Keep music quiet under narration (about 10–20% volume).

### Step 5 — Edit and export
- Free editors: **CapCut**, **VN**, **DaVinci Resolve**.
- Vertical `1080×1920` MP4 for Reels / Shorts; horizontal `1920×1080` MP4 for YouTube.
- Save the finished file in `videos/` (see `videos/README.md` for naming).
- Save a thumbnail in `assets/thumbnails/`.

---

## ⚖️ Copyright & safety rules (read this before publishing anything)

Copyright problems come from using **other people's work** without permission. This section tells you exactly what's safe and what isn't.

### ✅ Always safe
| What | Why |
|---|---|
| Stories **you** wrote yourself | You own the copyright automatically |
| Your own voice, drawings, music | Same — your creation, your rights |
| AI images/video **you** generated | Treat as your own creation for this project |
| Public domain works (e.g. Aesop's fables, Grimm's fairy tales as *original texts*) | Copyright expired — free for everyone |
| CC0 / "no rights reserved" assets | Creator gave all rights away |

### ⚠️ Safe only with care
| What | What to check |
|---|---|
| "Royalty-free" music/images | Read the actual license page; save proof (the `-credit.txt` habit) |
| Creative Commons music/images | Note which CC version — some forbid commercial use (NC) or remixes (ND) |
| Public domain *stories* | The original 1812 Cinderella text is fine; **Disney's** Cinderella movie version is NOT |

### ❌ Never use
- Characters from cartoons, movies, or games (a story "starring" a famous mouse or superhero)
- Popular songs, movie soundtracks, cartoon theme tunes — even "just 10 seconds"
- Text copied from published children's books (even with small changes)
- Photos, art, or videos by other creators found via search engines or social media
- "Free download" MP3s/MP4s from untrustworthy sites

### 🧒 Special note: content for children
- On **YouTube**, always mark kids' videos as **"Made for kids"** during upload — it's required by law (COPPA) and changes how comments/ads work.
- Never collect personal data from children (no "comment your name/age" prompts).
- Keep comments moderated or off if you can't monitor them.

### If you're ever unsure
Ask these three questions. If any answer is "no" or "I don't know," **don't publish it**:
1. Did I create this myself, or can I point to the exact page that says it's free to use?
2. Did I save proof (license page, credit file)?
3. Am I avoiding famous characters, songs, and copied text?

---

## 🌍 How to publish online

### Option A — Stories as a website (free, via GitHub Pages)
1. On GitHub, open your repository → **Settings → Pages**.
2. Under "Build and deployment", choose **Deploy from a branch**, select `main` and `/ (root)`, then Save.
3. Add a simple `index.html` at the repo root listing your stories with links to the Markdown files. GitHub will publish it at `https://<your-username>.github.io/kids-book-videos/`.
4. Every `git push` updates the site automatically.

### Option B — Videos on YouTube (free)
1. Create a channel for your stories.
2. Upload from `videos/`, add the thumbnail from `assets/thumbnails/`.
3. In the upload settings: set **Audience → "Yes, it's made for kids"**, add a description with credit lines for any third-party music.
4. Paste your license note in the description, e.g.: *"Story: The Brave Little Firefly — shared under CC BY 4.0."*

### Option C — Short clips on Instagram / YouTube Shorts (free)
- Export the vertical `1080×1920` version and upload as a Reel/Short.
- Put the story title + license in the caption. Link the full story in your bio.

### Option D — Stories as a free ebook
- Copy a story's Markdown into Google Docs → export as PDF/EPUB, or use a free tool like Calibre.
- Include the credit page ("© [Your Name], shared under CC BY 4.0").

---

## 📜 Choosing a license for your kids' content

A license tells the world what they're allowed to do with your work. Without one, others must assume "all rights reserved." Pick one and keep it in `LICENSE.md`.

| License | Others may… | Must they credit you? | Good when… |
|---|---|---|---|
| **CC0** (public domain dedication) | Do anything, no conditions | No | You want maximum spread, e.g. classroom use with zero friction |
| **CC BY 4.0** ⭐ (recommended) | Share & adapt, even commercially | **Yes** | You want sharing + credit. Best balance for kids' content |
| **CC BY-SA 4.0** | Share & adapt, even commercially | Yes, **and** share adaptations under the same license | You want remixes to stay equally open |
| **CC BY-NC 4.0** | Share & adapt, non-commercial only | Yes | You want to block others from selling your work (note: this also blocks some schools/platforms) |

**Our recommendation: CC BY 4.0.** It's the friendliest for teachers, parents, and translators — they can print, translate, and perform your stories freely — while you still get credited everywhere your work travels. (This repo itself uses CC BY 4.0; see [LICENSE.md](LICENSE.md).)

**How to apply it:** keep the `LICENSE.md` file, and add one line wherever you publish: *"© [Your Name], shared under CC BY 4.0 — github.com/<your-username>/kids-book-videos"*.

---

## ✅ Pre-publish checklist

Run through this before every story or video goes public:

- [ ] Story text is 100% my own words (or marked public-domain source)
- [ ] No famous characters, copied rhymes, or borrowed plot lines
- [ ] Every image is mine, AI-generated by me, or verified CC0/public domain
- [ ] Every music track has a `-credit.txt` file in `assets/music/`
- [ ] Voiceover is my own recording
- [ ] License + credit line included wherever I publish
- [ ] YouTube upload marked "Made for kids" (for video)
- [ ] Thumbnail contains no copyrighted characters or logos

---

## 🤝 Contributing

Found a typo? Want to add a story? Contributions are welcome:

1. Fork the repo, add your **original** story or script (same format as the examples).
2. Confirm it passes the pre-publish checklist above.
3. Open a pull request with a short description.

By contributing, you agree your contribution is your own original work shared under the repo's CC BY 4.0 license.

---

*Made with care for little readers everywhere. 🌙📚*
