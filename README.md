# Workshop — a catalog of repos that knew they were dying

**Workshop** is a small, stdlib-only Python CLI plus a hand-curated dataset for exploring "forgotten workshop" repositories: interesting, abandoned, archived open-source projects surfaced from public GitHub research. No dependencies, no network, no setup — clone and run.

Built incrementally by a scheduled autonomous Claude agent under the constraints in `AGENT_RULES.md` (part of a blind multi-agent experiment; see `JUDGING.md`).

## Quickstart

Requires only Python 3 (standard library).

```
python3 workshop.py list              # all 11 entries, one line each
python3 workshop.py show <id|slug>    # one entry by id or owner/name, incl. caveats & sunset evidence
python3 workshop.py search <keyword>  # match against name, repo, description, tags
python3 workshop.py tags              # tag frequency table
python3 workshop.py rank              # entries ordered by interest_score()
python3 workshop.py stats             # censuses: archived, licenses, caveats, sunsets
python3 workshop.py sunsets           # the 6 self-aware sunsets and their successors
```

Two global flags work on every command:

```
--json            # machine-readable output (each entry carries a computed `caveats` array)
--verified-only   # drop any entry with an unresolved data caveat (2 of 11 survive)
```

Run the test suite (40 black-box tests, no network):

```
python3 -m unittest test_workshop
```

## The headline finding

The common intuition is that abandoned repos rot silently. This catalog says otherwise: **6 of the 11 entries (55%) are "self-aware sunsets"** — the maintainers explicitly retired the repo via a deprecation banner, an archive announcement, or a handoff, and 4 of the 6 point users at a successor. First-party abandonment signals turn out to be common and machine-readable, which is a different design premise for any future discovery tool than commit-date heuristics.

The full writeup — including a five-style taxonomy of how maintainers retire repos, a critique of this repo's own ranking heuristic, and the dataset's limitations — is in [`ANALYSIS.md`](ANALYSIS.md). Every number in it reproduces from the CLI.

## The dataset audits itself

`data/candidates.jsonl` (11 entries, JSONL, one object per line) records its own uncertainty in-band: 9 of 11 entries carry at least one `*_note` caveat — most notably five run-1 entries whose `stars:500` value could not be verified with this sandbox's tools and is flagged rather than silently kept. Caveats surface as `[!]` markers in human output, as `caveats` arrays in `--json`, and as a filter via `--verified-only`. Sunset claims must carry an `evidence` string traceable to `RESEARCH_LOG.md`; a test enforces this.

## Repo map

- `workshop.py` — the CLI (single file, stdlib only)
- `data/candidates.jsonl` — the curated dataset
- `test_workshop.py` — 40 black-box tests
- `ANALYSIS.md` — what the dataset shows
- `RESEARCH_LOG.md` — per-entry verification writeups (runs 1–10)
- `MISSION.md`, `SEED.md`, `AGENT_RULES.md`, `JUDGING.md` — the experiment's fixed frame
- `AGENT_STATE.md`, `CHANGELOG.md`, `DECISIONS.md`, `RUNS/` — the agent's memory and audit trail
- `THIRD_PARTY_NOTICES.md` — license/attribution record (no external code was copied)
