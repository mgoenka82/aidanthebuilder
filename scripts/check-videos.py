#!/usr/bin/env python3
"""Check that every YouTube video embedded in index.html is still playable.

Reads the video ids straight out of index.html so the list can never drift,
then asks YouTube's oembed endpoint about each one. A video that has been
deleted, made private, or had embedding turned off gives a non-200 response.

Exits non-zero if anything is broken, so a scheduled CI run fails loudly.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "index.html"
OEMBED = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={}&format=json"


def video_ids(html: str) -> list[str]:
    # Matches the `{ id:"XXXXXXXXXXX", label:...}` entries in the THEMES table.
    return re.findall(r'\{\s*id:\s*"([\w-]{11})"', html)


def check(vid: str) -> tuple[bool, str]:
    req = urllib.request.Request(OEMBED.format(vid), headers={"User-Agent": "legosforaidan-linkcheck"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
        return True, f"{data.get('title', '?')} — {data.get('author_name', '?')}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} (deleted, private, or embedding disabled)"
    except Exception as e:  # network hiccup, DNS, timeout
        return False, f"{type(e).__name__}: {e}"


def main() -> int:
    ids = video_ids(HTML.read_text())
    if not ids:
        print("No video ids found in index.html — did the file format change?")
        return 2

    broken = []
    for vid in ids:
        ok, detail = check(vid)
        print(f"{'ok  ' if ok else 'DEAD'}  {vid}  {detail}")
        if not ok:
            broken.append((vid, detail))

    print(f"\n{len(ids) - len(broken)}/{len(ids)} videos playable")
    if broken:
        print("\nBroken videos — replace these in index.html:")
        for vid, detail in broken:
            print(f"  https://www.youtube.com/watch?v={vid}  →  {detail}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
