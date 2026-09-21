#!/usr/bin/env python3
"""Upload staged files to the kids-book-videos GitHub repo via the API.

Usage:
    python3 publish.py --repo niteshlhsnda-droid/kids-book-videos \
        --map manifest.json
manifest.json: {"local/path/file.md": "stories/file.md", ...}

Calls the github skill's authenticated request helper directly (in-process),
so large files like videos are not limited by OS command-line length caps.
Existing files are updated (their current sha is fetched first).
"""
import argparse
import base64
import importlib.util
import json

GH_PY = "/home/hatch/workspace/skills/github/bin/gh.py"


def load_gh():
    spec = importlib.util.spec_from_file_location("gh_skill", GH_PY)
    gh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gh)
    return gh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--map", required=True,
                    help="JSON mapping local paths to repo paths")
    ap.add_argument("--message", default="Add daily story")
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()

    gh = load_gh()

    with open(args.map) as f:
        mapping = json.load(f)

    for local, repo_path in mapping.items():
        with open(local, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        path = f"/repos/{args.repo}/contents/{repo_path}"
        url = gh.build_url(path, None)
        data = {"message": f"{args.message}: {repo_path}",
                "content": content, "branch": args.branch}
        # Updating an existing file requires its current sha.
        status, payload, _ = gh.do_request("GET", url, None)
        if status == 200 and isinstance(payload, dict) and payload.get("sha"):
            data["sha"] = payload["sha"]
        status, payload, _ = gh.do_request("PUT", url, data)
        if status >= 400:
            raise SystemExit(
                f"upload failed for {repo_path}: HTTP {status} "
                f"{json.dumps(payload)[:300]}")
        sha = payload["commit"]["sha"][:8]
        print(f"ok: {repo_path} ({sha})", flush=True)


if __name__ == "__main__":
    main()
