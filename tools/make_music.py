#!/usr/bin/env python3
"""Generate an original gentle music-box lullaby.

Every note is synthesized here with numpy — no samples, no loops, no
copyrighted material. Safe to publish anywhere.

Usage:
    python3 make_music.py --duration 240 --output lullaby.mp3 [--seed 7]
"""
import argparse
import math
import random
import subprocess
import tempfile
import wave

import numpy as np

SR = 44100


def music_box_note(freq, dur):
    """A soft music-box tone: bright attack, long gentle decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = np.exp(-3.2 * t)
    y = (np.sin(2 * np.pi * freq * t)
         + 0.30 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-5 * t)
         + 0.12 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-8 * t))
    return y * env


def pad_chord(freqs, dur):
    """A warm, quiet synth pad under the melody."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f in freqs:
        y += np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    y /= max(1, len(freqs))
    swell = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    return y * swell * 0.35


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, required=True,
                    help="total length in seconds")
    ap.add_argument("--output", required=True, help="output .mp3 path")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    # Pick a warm major key and a I–V–vi–IV progression.
    root_midi = rng.choice([48, 50, 53, 55, 57])  # C3 D3 F3 G3 A3
    def mf(semi):
        return 440.0 * 2 ** ((root_midi + semi - 69) / 12)
    chords = [
        [mf(0), mf(4), mf(7)],     # I
        [mf(7), mf(11), mf(14)],   # V
        [mf(9), mf(12), mf(16)],   # vi
        [mf(5), mf(9), mf(12)],    # IV
    ]
    penta = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]  # two octaves, major pentatonic

    total = args.duration
    track = np.zeros(int(total * SR))
    bar = 8.0  # seconds per chord

    # Pads: one chord per bar, cycling the progression.
    t = 0.0
    ci = 0
    while t < total:
        d = min(bar, total - t)
        pad = pad_chord(chords[ci % 4], d)
        s = int(t * SR)
        track[s:s + len(pad)] += pad * 0.5
        t += bar
        ci += 1

    # Melody: a gentle random walk on the pentatonic scale, sparse and dreamy.
    step = 0.55
    idx = 4  # start near the middle
    t = 1.0
    while t < total - 4:
        if rng.random() < 0.45:  # rest — space is part of the music
            t += step
            continue
        idx = max(0, min(len(penta) - 1, idx + rng.choice([-2, -1, -1, 1, 1, 2])))
        freq = mf(penta[idx])
        note = music_box_note(freq, min(3.0, total - t))
        s = int(t * SR)
        track[s:s + len(note)] += note * 0.55
        t += step * rng.choice([1, 1, 2])

    # Gentle fade-out over the last 4 seconds, normalize, write.
    fade = int(4 * SR)
    if fade < len(track):
        track[-fade:] *= np.linspace(1, 0, fade)
    peak = np.max(np.abs(track))
    if peak > 0:
        track *= 0.75 / peak
    pcm = (track * 32767).astype(np.int16)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "128k",
                    args.output], check=True)
    print(f"wrote {args.output} ({total:.0f}s original lullaby)")


if __name__ == "__main__":
    main()
