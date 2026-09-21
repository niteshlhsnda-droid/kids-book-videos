#!/usr/bin/env python3
"""Assemble a slideshow story video: Ken Burns images + narration + soft music.

Usage:
    python3 assemble_video.py --images img1.jpg img2.jpg img3.jpg \
        --narration narration.mp3 --music lullaby.mp3 \
        --output story-video.mp4 --thumbnail thumb.jpg
"""
import argparse
import json
import os
import subprocess
import tempfile


def probe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", nargs="+", required=True)
    ap.add_argument("--narration", required=True)
    ap.add_argument("--music", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--thumbnail", required=True)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    args = ap.parse_args()

    total = probe_duration(args.narration)
    per = total / len(args.images)
    frames = max(1, int(per * 30))
    W, H = args.width, args.height

    tmp = tempfile.mkdtemp(prefix="storyvid_")
    segs = []
    for i, img in enumerate(args.images):
        seg = os.path.join(tmp, f"seg{i}.mp4")
        # Slow zoom-in (Ken Burns) so still images feel alive.
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},"
              f"zoompan=z='min(zoom+0.0009,1.18)':d={frames}:"
              f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", img,
             "-vf", vf, "-t", f"{per:.2f}", "-c:v", "libx264",
             "-pix_fmt", "yuv420p", seg], check=True)
        segs.append(seg)

    concat_list = os.path.join(tmp, "list.txt")
    with open(concat_list, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    silent = os.path.join(tmp, "silent.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", concat_list, "-c", "copy", silent], check=True)

    # Mix: narration up front, music tucked quietly underneath.
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", silent, "-i", args.narration, "-i", args.music,
         "-filter_complex",
         "[2:a]volume=0.12,aloop=loop=-1:size=2e9[m];"
         "[1:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
         "-preset", "medium", "-c:a", "aac", "-b:a", "128k",
         "-movflags", "+faststart", "-shortest", args.output], check=True)

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", args.images[0],
         "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                f"crop={W}:{H}", "-frames:v", "1", args.thumbnail],
        check=True)
    print(f"wrote {args.output} ({total:.0f}s, {len(args.images)} scenes)")


if __name__ == "__main__":
    main()
