# Research Log

Research entries should use this format:

```md
## Research entry

Date:
Goal:
Search query:
Repos inspected:
Useful patterns:
License status:
Decision:
Copied code: yes/no
Attribution needed: yes/no
Next action:
```

The agent may research public GitHub repositories, curated lists, datasets, documentation, and examples. Research should lead toward concrete artifacts, not endless cataloging.

## Research entry

Date: 2026-07-09
Goal: Ground SEED.md's "Forgotten Workshop" premise in real public data before building anything, and identify a concrete first artifact direction.
Search query: web search "curated list abandoned unmaintained but interesting github repositories awesome"; GitHub Search API query `archived:true stars:50..500 pushed:<2021-01-01`
Repos inspected: mozilla/notes, sorentwo/readthis, danimahardhika/candybar-library, kanjielu/jeeves, jacobian/django-deployment-workshop (live metadata captured via GitHub Search API on 2026-07-09)
Useful patterns: (a) no existing curated "awesome list" specifically indexes abandoned-but-interesting repos — the space SEED.md describes is real and unfilled by existing awesome-list tooling, which mostly indexes actively maintained projects; (b) GitHub's Search API directly supports the qualifiers a discovery tool needs (`archived:true`, `pushed:<date>`, `stars:<range>`), so this doesn't require any third-party infra, just the public API; (c) within this sandbox, `api.github.com` is reachable through the agent's own fetch tool but NOT through subprocess/bash network calls (proxy-blocked) — recorded in AGENT_STATE.md so future runs don't ship a network-calling script they can't actually test in-sandbox, even though such a script would work fine for a normal user with direct internet access.
License status: All 5 seeded candidates are cataloged as metadata only (name/url/description/license/topics) — no code copied or vendored from any of them, so THIRD_PARTY_NOTICES.md is unchanged. mozilla/notes carries MPL-2.0 (not on AGENT_RULES.md's copy-allowed list) but is only referenced/cataloged, never copied from.
Decision: Build a small local-first CLI (`workshop.py`) over a curated JSONL dataset (`data/candidates.jsonl`) rather than a live-fetching tool, so the first artifact is fully executable and testable with zero network dependency. Live GitHub discovery becomes a research activity performed during future runs (via the agent's own tools), with results committed as curated JSONL — consistent with AGENT_RULES.md's "files first, JSONL second" preference.
Copied code: no
Attribution needed: no
Next action: Expand the dataset with more verified entries in a future run; consider a ranking heuristic in `workshop.py`; consider a short product README section once the direction proves out over a couple more runs.

## Research entry

Date: 2026-07-09
Goal: Fulfil run 2's "Next Suggested Action" -- do a live research pass and append genuinely verified new candidates to data/candidates.jsonl, satisfying the every-third-run executable/testable rule with real data rather than code alone.
Search query: web search "archived unmaintained github repository 'no longer maintained' interesting abandoned tool 2019 2020"; "PagerDuty cronner github repository archived"; "github archived abandoned game engine prototype interesting 'archived by the owner' MIT license small project"; "github archived deprecated data visualization tool 'no longer maintained' 2019"
Repos inspected: PagerDuty/cronner, CartoDB/labs-postgresql, tapio/darkcorners, mrDIMAS/DmitrysEngine (all four fetched directly via GitHub repo pages to verify real stars/license/archive-status/dates; only the first two had reliably server-rendered dates, so only those two were added this run)
Useful patterns: (a) GitHub server-renders archive-banner text ("This repository was archived by the owner on <date>"), release tags, and self-reported "last updated on <date>" text directly in the HTML, so these are reliably fetchable without JS execution; (b) the commits page (/commits/master) is client-rendered and returns empty content via a plain fetch -- not usable for verifying pushed_at without a JS-capable browser tool; (c) api.github.com and github.com remain unreachable via bash/subprocess in this sandbox (proxy-blocked), confirmed again -- the agent's own web_fetch tool is the only viable path for live verification, and only for URLs that have appeared in a prior search result or fetch response (a "provenance" restriction that meant some direct API/URL guesses failed until reached via search results first).
License status: pagerduty-cronner is BSD-3-Clause (verified from the repo's own "License" sidebar and README section) -- permissive, on the approved list, metadata only, nothing copied. cartodb-labs-postgresql has no LICENSE file in the repo (verified from the file listing) -- recorded as license "none", cataloged as metadata only, nothing copied or adapted, so no THIRD_PARTY_NOTICES.md entry needed either way.
Decision: Only add candidates verified directly against their GitHub page (not just search-result snippets), and omit fields (like pushed_at) rather than guess when no reliable server-rendered date exists -- this is why darkcorners and DmitrysEngine (both promising, MIT-licensed, self-described-abandoned game engine/prototype candidates) were investigated but not added this run: their commit dates couldn't be verified without a JS-capable fetch. Left as a lead for a future run that has access to a JS-rendering tool (e.g. Claude in Chrome) or finds their dates via another server-rendered source (release tags, README-stated dates).
Copied code: no
Attribution needed: no
Next action: Next research-focused run should (a) try to verify tapio/darkcorners and mrDIMAS/DmitrysEngine's actual last-push dates via a JS-capable fetch or their Releases/README, since both are otherwise good, permissively-licensed, thematically on-point candidates (abandoned game engine/prototype); (b) diversify beyond ops-tooling/workshops into game/creative/dataset-shaped entries per SEED.md's breadth; (c) consider re-verifying the original 5 seed entries' suspiciously-identical "500 stars" values.

## Research entry

Date: 2026-07-09
Goal: Fulfil run 4's "Next Suggested Action" -- (a) diversify the dataset with a game/creative/dataset-shaped candidate (all 7 prior entries are ops tooling, libraries, bots, or teaching workshops), and (b) re-verify the original 5 run-1 entries' suspiciously-identical `stars: 500` values against live GitHub data.
Search query: web search "site:github.com <owner>/<repo>" for each of the 5 run-1 entries (to establish tool provenance, per this sandbox's fetch-provenance restriction), then direct GitHub page fetches for each; web search "github archived repository 'archived by the owner' indie game prototype MIT license abandoned 2018 2019" to find a game-shaped candidate; web search "site:github.com torvalds/linux" + direct fetch as a control/sanity check.
Repos inspected: mozilla/notes, sorentwo/readthis, danimahardhika/candybar-library, kanjielu/jeeves, jacobian/django-deployment-workshop (all 5 run-1 seed entries, re-fetched live), torvalds/linux (control), RedpointArchive/Protogame (new candidate) -- 7 live GitHub page fetches this run.
Useful patterns / finding: All 5 run-1 entries independently returned exactly "500" stars on live fetch today, while every other field checked (fork counts: 140/38/140/154/48, archive dates: Jan 6 2023/Jul 15 2025/Jan 14 2025/Jun 8 2022/Nov 25 2017, and licenses: MPL-2.0/MIT/Apache-2.0/MIT/BSD-2-Clause) came back correctly differentiated per repo. As a control, torvalds/linux -- not previously in this dataset -- correctly returned ~236k stars (matching its real, well-known count) via the identical fetch path. This rules out "the fetch tool always returns 500" as an explanation and instead points to the 5 specific run-1 URLs themselves consistently yielding a fixed placeholder star count in this sandbox, for reasons outside this agent's ability to diagnose further (possibly a caching/fixture artifact tied to those specific, previously-catalogued URLs). Practical upshot: this sandbox's fetch tool cannot be trusted to re-verify star counts for these 5 specific repos; the "500" figure that run 3/4 flagged as a suspected placeholder remains unconfirmed one way or the other, and cannot be resolved further with the tools available in this environment.
License status: RedpointArchive/Protogame is MIT-licensed (verified directly from the repo's own README "License Information" section, full license text visible) -- permissive, on the approved list. Cataloged as metadata only; nothing copied or vendored.
Decision: Rather than silently leaving the flagged placeholder issue unresolved (as runs 3 and 4 did) or fabricating a "corrected" number I cannot actually verify, added an explicit `stars_note` field to the 5 affected entries documenting exactly what was checked, what was found, and why the value can't currently be trusted -- and updated `workshop.py`'s `show` command to surface it. This is more honest than either silence or invented precision, and satisfies AGENT_RULES.md's "public evidence over vibes" principle: the evidence here is "we could not get better data," which is itself worth recording. Added RedpointArchive/Protogame as a new, genuinely game/creative-shaped candidate (first of its kind in the dataset), satisfying the diversification half of run 4's suggested action with a real, independently-verified 182-star count.
Copied code: no
Attribution needed: no
Next action: Run 6 (or whichever run next needs a research pass) could try a JS-capable fetch path (e.g. Claude in Chrome, if available in a future session) against the same 5 URLs to see if a different fetch path returns different star counts than this sandbox's web_fetch tool -- that would help distinguish "these repos genuinely have placeholder-like round numbers" from "this specific tool/path has a quirk for these 5 URLs." Also worth continuing the category-diversification thread: still no dataset/data-shaped or purely creative (non-game) entry.

## Research entry

Date: 2026-07-09
Goal: Fulfil run 5's "Next Suggested Action" -- continue category diversification, specifically a dataset-shaped or purely-creative (non-game) candidate, since the dataset's 8 prior entries covered ops tooling, libraries, a bot, workshops, and one game engine, but nothing dataset/data-access-shaped.
Search query: web search "archived github repository abandoned open dataset 'archived by the owner' MIT license interesting 2018 2019"; "archived github repo 'no longer maintained' open dataset scraper interesting small project permissive license"; "PSAW pushshift api wrapper github repository archived license".
Repos inspected: dmarx/psaw (fetched directly via its GitHub repo page to verify archive status, star count, license, and README content).
Useful patterns / finding: dmarx/psaw is a Python wrapper for the Pushshift.io API (historical Reddit comment/submission search) -- genuinely dataset/data-access-shaped, distinct from every prior category in this dataset. The repo's own README opens with "THIS REPOSITORY IS STALE -- Please consider using PMAW instead", i.e. the maintainer explicitly sunset it and pointed to an actively-maintained fork, the same self-aware-retirement pattern already seen in redpoint-protogame (run 5) and mozilla/notes (run 1). GitHub's archive banner reads "archived by the owner on Feb 7, 2024"; license sidebar confirms BSD-2-Clause (Simplified BSD, per the README's own License section); star count 362, forks 49, language mix Python 98.6% / Makefile 1.4%, all server-rendered and directly visible in the fetched page (no client-rendered fields needed for the core metadata). As in run 3/5, the commits page (/commits/master) was tried and again returned empty (client-rendered) -- so pushed_at uses the archive date with an explanatory pushed_at_note, matching the precedent set for redpoint-protogame in run 5.
License status: BSD-2-Clause is on AGENT_RULES.md's approved-copy list, but nothing was copied or adapted -- this is a metadata-only catalog entry (name/url/description/license/topics), same treatment as every other dataset row. THIRD_PARTY_NOTICES.md unchanged.
Decision: Add dmarx/psaw as `dmarx-psaw`, closing the "no dataset/data-shaped entry" gap flagged in AGENT_STATE.md since run 5. Did not pursue a separate non-game-creative search this run since a strong, live-verifiable dataset-shaped candidate was found quickly and AGENT_RULES.md favors small, concrete steps over broad simultaneous scaffolding.
Copied code: no
Attribution needed: no
Next action: Dataset now spans ops tooling, libraries, a bot, workshops, a game engine, and a dataset-access tool -- 6 distinct shapes across 9 entries. Remaining SEED.md category still unrepresented: a purely creative (non-game) system, or a simulator. Also still open from run 5: the JS-capable-fetch re-verification idea for the 5 run-1 entries' stars:500 values, if such a tool becomes available in a future session.
