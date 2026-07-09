#!/usr/bin/env python3
"""
Workshop: a small CLI for browsing curated "forgotten workshop" repositories --
interesting, abandoned, or historically notable open-source projects surfaced
from public GitHub research.

Data lives in data/candidates.jsonl (one JSON object per line). This script
has no external dependencies and does not require network access; it only
reads the local curated dataset.

Usage:
    python3 workshop.py list
    python3 workshop.py show <id>
    python3 workshop.py search <keyword>
    python3 workshop.py tags
"""
import json
import sys
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "candidates.jsonl"


def load_candidates():
    if not DATA_PATH.exists():
        print(f"error: data file not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    items = []
    with DATA_PATH.open() as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"warning: skipping malformed line {line_no}: {e}", file=sys.stderr)
    return items


def fmt_row(item):
    stars = item.get("stars", "?")
    lang = item.get("language", "?")
    return f"{item['id']:<32} ★{str(stars):<6} {str(lang):<10} {item['name']}"


def cmd_list(items, args):
    if not items:
        print("(no candidates yet)")
        return
    for item in items:
        print(fmt_row(item))
    print(f"\n{len(items)} candidate(s). Use 'show <id>' for details.")


def cmd_show(items, args):
    if not args:
        print("usage: workshop.py show <id>", file=sys.stderr)
        sys.exit(2)
    target = args[0]
    for item in items:
        if item["id"] == target:
            for key in ["id", "name", "url", "description", "stars", "language",
                        "license", "archived", "pushed_at", "topics", "why",
                        "source", "captured"]:
                if key in item:
                    print(f"{key:>12}: {item[key]}")
            return
    print(f"no candidate with id '{target}'", file=sys.stderr)
    sys.exit(1)


def cmd_search(items, args):
    if not args:
        print("usage: workshop.py search <keyword>", file=sys.stderr)
        sys.exit(2)
    keyword = args[0].lower()
    hits = []
    for item in items:
        haystack = " ".join(str(item.get(k, "")) for k in
                             ["name", "description", "why", "language"])
        haystack += " " + " ".join(item.get("topics", []))
        if keyword in haystack.lower():
            hits.append(item)
    if not hits:
        print(f"no matches for '{keyword}'")
        return
    for item in hits:
        print(fmt_row(item))
    print(f"\n{len(hits)} match(es) for '{keyword}'.")


def cmd_tags(items, args):
    counts = {}
    for item in items:
        for tag in item.get("topics", []):
            counts[tag] = counts.get(tag, 0) + 1
    if not counts:
        print("(no topics recorded)")
        return
    for tag, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{count:>3}  {tag}")


COMMANDS = {
    "list": cmd_list,
    "show": cmd_show,
    "search": cmd_search,
    "tags": cmd_tags,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"commands: {', '.join(COMMANDS)}")
        sys.exit(0 if len(sys.argv) < 2 else 2)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    items = load_candidates()
    COMMANDS[cmd](items, args)


if __name__ == "__main__":
    main()
