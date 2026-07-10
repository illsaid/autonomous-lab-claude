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
    python3 workshop.py rank
    python3 workshop.py stats

Any command also accepts a --json flag for machine-readable output, e.g.:
    python3 workshop.py rank --json

Any command also accepts a --verified-only flag, which excludes entries
carrying data-quality caveats (any '*_note' field, e.g. stars_note or
pushed_at_note) before the command runs:
    python3 workshop.py rank --verified-only
    python3 workshop.py list --verified-only --json

In --json output, every per-entry object additionally carries a computed
'caveats' array naming that entry's data-quality caveat fields (empty when
the entry is fully verified), mirroring the [!] marker in human output.
"""
import json
import sys
from datetime import date
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "candidates.jsonl"

PERMISSIVE_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"}


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


def data_caveats(item):
    """Names of the data-quality caveat fields on this entry.

    A caveat field is any key ending in '_note' (e.g. stars_note,
    pushed_at_note): an explicit, recorded reason why a neighboring value
    is unverified, rounded, or approximated (see runs 5-8 in CHANGELOG.md).
    """
    return sorted(k for k in item if k.endswith("_note"))


def with_caveats(item):
    """Copy of item with a computed 'caveats' array for JSON consumers.

    Human output already flags caveated rows with [!]; this surfaces the
    same data_caveats() result in machine-readable output so scripts do
    not have to reimplement the '*_note' key convention themselves.
    """
    return dict(item, caveats=data_caveats(item))


def fmt_row(item):
    stars = item.get("stars", "?")
    lang = item.get("language", "?")
    flag = " [!]" if data_caveats(item) else ""
    return f"{item['id']:<32} ★{str(stars):<6} {str(lang):<10} {item['name']}{flag}"


def cmd_list(items, args, as_json=False):
    if as_json:
        print(json.dumps([with_caveats(i) for i in items], indent=2))
        return
    if not items:
        print("(no candidates yet)")
        return
    for item in items:
        print(fmt_row(item))
    print(f"\n{len(items)} candidate(s). Use 'show <id>' for details.")
    if any(data_caveats(item) for item in items):
        print("[!] = entry carries data caveat(s); 'show <id>' explains, "
              "--verified-only excludes.")


def cmd_show(items, args, as_json=False):
    if not args:
        print("usage: workshop.py show <id>", file=sys.stderr)
        sys.exit(2)
    target = args[0]
    for item in items:
        if item["id"] == target:
            if as_json:
                print(json.dumps(with_caveats(item), indent=2))
                return
            for key in ["id", "name", "url", "description", "stars", "stars_note",
                        "language", "license", "archived", "pushed_at",
                        "pushed_at_note", "topics", "why", "source", "captured"]:
                if key in item:
                    print(f"{key:>12}: {item[key]}")
            return
    print(f"no candidate with id '{target}'", file=sys.stderr)
    sys.exit(1)


def cmd_search(items, args, as_json=False):
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
    if as_json:
        print(json.dumps([with_caveats(i) for i in hits], indent=2))
        return
    if not hits:
        print(f"no matches for '{keyword}'")
        return
    for item in hits:
        print(fmt_row(item))
    print(f"\n{len(hits)} match(es) for '{keyword}'.")


def cmd_tags(items, args, as_json=False):
    counts = {}
    for item in items:
        for tag in item.get("topics", []):
            counts[tag] = counts.get(tag, 0) + 1
    if as_json:
        print(json.dumps(dict(sorted(counts.items(), key=lambda kv: -kv[1])), indent=2))
        return
    if not counts:
        print("(no topics recorded)")
        return
    for tag, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{count:>3}  {tag}")


def interest_score(item):
    """Heuristic "how forgotten-but-interesting is this?" score.

    Rewards: a moderate, non-viral star count (sweet spot ~300, since a
    10-star toy and a 50k-star mainstream project are both less "forgotten
    workshop" material than something quietly used-but-abandoned); genuine
    age since last push (older = more time to have been forgotten, capped
    so ancient noise doesn't dominate); a permissive license (reusable);
    and topic richness (more topics usually means more curator/community
    context to judge the project by).

    This is a simple, explainable, deterministic heuristic over local
    metadata only -- not a claim of objective "quality".
    """
    stars = item.get("stars") or 0
    star_score = max(0.0, 10.0 - abs(stars - 300) / 100.0) if stars > 0 else 0.0

    age_score = 0.0
    pushed = item.get("pushed_at")
    if pushed:
        try:
            y, m, d = (int(p) for p in pushed.split("-"))
            years = (date.today() - date(y, m, d)).days / 365.25
            age_score = min(max(years, 0.0), 10.0)
        except (ValueError, TypeError):
            pass

    license_score = 3.0 if item.get("license") in PERMISSIVE_LICENSES else 0.0
    topic_score = min(len(item.get("topics", [])), 5)

    return round(star_score + age_score + license_score + topic_score, 2)


def cmd_rank(items, args, as_json=False):
    if not items:
        if as_json:
            print("[]")
        else:
            print("(no candidates yet)")
        return
    ranked = sorted(items, key=interest_score, reverse=True)
    if as_json:
        out = [dict(with_caveats(item), interest_score=interest_score(item)) for item in ranked]
        print(json.dumps(out, indent=2))
        return
    for item in ranked:
        score = interest_score(item)
        print(f"{score:>6.2f}  {fmt_row(item)}")
    print(f"\n{len(ranked)} candidate(s) ranked by interest_score "
          f"(stars sweet-spot + age + permissive license + topic richness).")



def cmd_stats(items, args, as_json=False):
    """Summarize the dataset: totals, archived ratio, license mix, language mix, star range."""
    if not items:
        if as_json:
            print("{}")
        else:
            print("(no candidates yet)")
        return
    total = len(items)

    archived = sum(1 for i in items if i.get("archived"))
    permissive = sum(1 for i in items if i.get("license") in PERMISSIVE_LICENSES)
    caveated = sum(1 for i in items if data_caveats(i))
    stars = [i.get("stars") for i in items if isinstance(i.get("stars"), (int, float))]

    def _breakdown(field):
        counts = {}
        for i in items:
            key = i.get(field) or "?"
            counts[key] = counts.get(key, 0) + 1
        return sorted(counts.items(), key=lambda kv: -kv[1])

    if as_json:
        payload = {
            "total": total,
            "archived": archived,
            "permissively_licensed": permissive,
            "caveated": caveated,
            "by_license": dict(_breakdown("license")),
            "by_language": dict(_breakdown("language")),
        }
        if stars:
            payload["stars"] = {
                "min": min(stars),
                "max": max(stars),
                "avg": round(sum(stars) / len(stars), 1),
            }
        print(json.dumps(payload, indent=2))
        return

    print(f"Total candidates: {total}")
    print(f"Archived: {archived}/{total}")
    print(f"Permissively licensed: {permissive}/{total}")
    print(f"Caveated (any *_note): {caveated}/{total}")
    if stars:
        avg = sum(stars) / len(stars)
        print(f"Stars: min={min(stars)} max={max(stars)} avg={avg:.1f}")

    print("\nBy license:")
    for key, count in _breakdown("license"):
        print(f"{count:>3}  {key}")

    print("\nBy language:")
    for key, count in _breakdown("language"):
        print(f"{count:>3}  {key}")


COMMANDS = {
    "list": cmd_list,
    "show": cmd_show,
    "search": cmd_search,
    "tags": cmd_tags,
    "rank": cmd_rank,
    "stats": cmd_stats,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"commands: {', '.join(COMMANDS)}")
        sys.exit(0 if len(sys.argv) < 2 else 2)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    as_json = "--json" in args
    verified_only = "--verified-only" in args
    args = [a for a in args if a not in ("--json", "--verified-only")]
    items = load_candidates()
    if verified_only:
        items = [item for item in items if not data_caveats(item)]
    COMMANDS[cmd](items, args, as_json)


if __name__ == "__main__":
    main()
