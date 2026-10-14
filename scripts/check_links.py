"""Fail if any page in dist/ links to a page on this site that doesn't exist.

Run after `npm run build`. Catches links to lessons that aren't written yet.
"""

import pathlib
import posixpath
import re
import sys

BASE = "/vibedsa"
dist = pathlib.Path("dist")
broken = set()

for page in dist.rglob("index.html"):
    rel_dir = page.parent.relative_to(dist).as_posix()
    url = f"{BASE}/" if rel_dir == "." else f"{BASE}/{rel_dir}/"
    for href in re.findall(r'href="([^"#?]+)', page.read_text(encoding="utf-8")):
        if href.startswith(("http:", "https:", "mailto:", "//")):
            continue
        full = posixpath.normpath(posixpath.join(url, href))
        if not full.startswith(BASE):
            continue
        target = dist / full[len(BASE):].strip("/")
        if not ((target / "index.html").exists() or target.is_file()):
            broken.add(f"{url} -> {href}")

if broken:
    print("Broken internal links:", *sorted(broken), sep="\n  ")
    sys.exit(1)
print("No broken internal links.")
