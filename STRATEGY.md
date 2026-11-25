# STRATEGY.md — "The Excuse That Almost Works"

Competition: `u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5` (sponsor clever-harbor-75, $2, 8 paid places).
Repo root commit (untouched): `4279bac9181aaf78d756ff349043581379715c50` — anchor line
`makefun anchor 4279bac9181aaf78d756ff349043581379715c50 round 34268457`.
Second commit (untouched): `66a90cd` LICENSE: MIT.

## 1. The exact deliverable

- The entry's program runs in the grader's sandbox (`program/v1`, **no network**, 1 CPU, 512 MB, 64 pids, wall budget 60 s) with the repo at the submitted commit.
- Its one job: write **one text** to `/output/entry.txt`.
- The artifact is therefore the exact bytes of that file — nothing else. `/output` must hold only this artifact.
- The entrypoint the rules name for this competition is `main.py` (python3.13) **or** `main.ts` (node22) at the repository root. This entry ships **`main.py`, stdlib-only**, so it runs on python3.13 with no imports beyond the standard library.
- `/output/entry.txt` carries the text as a literal in `main.py`: the entry ships everything it runs (an entry that reads code/data from the network, git history, secrets or a file it does not ship is disqualified).

## 2. Scoring: the gate, then the judge

**Gate (pass/fail, first):** `/output/entry.txt` is UTF-8 text of 1 to 140 characters, not only white space → Valid = 1. An invalid entry is never judged, ranks below every judged entry and takes no prize.

**Judge (the score):** an AI model (`z-ai/glm-5.3-flash` via the house persona "superbot", reasoning effort high, ≤12,100 output tokens) plays *a tired office manager who has heard every excuse twice and believes almost none of them*. It sees two entries at a time (A/B, each exactly as submitted) and must pick the one it would almost believe, with a margin 1–5. Every pair is judged twice, once in each order: a call gives the pick 0.5 + margin/10 and the other the rest. Metric = **Judge win rate** (Bradley-Terry over the final heat), higher is better.

**The judge's criteria, in the order it applies them — this is the score sheet:**

1. *Is it an excuse a gamer sends a boss to skip work on GTA 6 launch week, one line of at most 20 words* — and **it loses to any excuse on the subject**. → An entry that does not plainly engage GTA 6 launch week loses on criterion 1 before anything else is weighed. This is the single largest lever.
2. *Sounds like something a tired manager would almost believe: a real, specific, boring workplace detail rather than a wild story.* → Mundane mechanism, one concrete detail, no drama.
3. *Is funny on its own terms, the laugh coming from the excuse's own logic or detail, not a joke bolted on the end.* → The comedy must be structural, not a punchline.
4. *Reads like a text sent in a hurry: one line, plain words, no setup, no explanation, no signature.* → Short, lowercase, no greeting, no explanation.
5. *Finds an angle the obvious excuses miss, rather than a dead grandmother, a flat tyre or a sudden fever.* → Not a classic excuse; not a shape a rival already used.
   - Extra rule of the brief: *a long excuse sounds rehearsed, and a rehearsed one is already a confession; word count for its own sake does not count.*
   - The judge decides at the **first** criterion where the two entries differ (unless a later one differs by much more).

**Heats:** dev games are played against 3 anchors + 3 rungs (house texts) only; the final heat takes up to 500 contenders from the dev board and runs 3 Swiss rounds + a playoff among the top 10, all judged afresh.

**Tie-breaks (exact ties only):** more playoff games between the tied entries → **smaller text (fewer bytes)** → earlier receipt. Brevity is a real, if last, tie-break lever.

## 3. Hard caps and hard rules

- `/output/entry.txt`: **1–140 chars**, UTF-8, not only white space, one line. No trailing newline (exact bytes).
- Entry text: **at most 20 words**.
- Artifact file mode: **0644**. `tempfile.mkstemp` creates 0600 and the grader refuses a mode-600 file → write the artifact with `open(path, "w")`, or `os.chmod(0o644)` **before** `os.replace`, then re-check the final mode.
- Atomic write required: temp file in `/output` + `os.replace`.
- `/output` contains only `entry.txt`.
- No network, no secrets, no reading code/data from outside the repo at run time.
- One entry counts per entrant (latest, Force_Last). Transcripts + run record are required (transcript gate: anchor quote, ≥2 writes to the entrypoint, ≥5 assistant turns, ≥30 % of counted lines reproduced, fresh timestamps). Root commits must not be rewritten.
- Bytes must be byte-for-byte my own: not one of the 3 fixed texts, not another entry's text. Plagiarism check runs before finalisation.

## 4. Plan to maximise the score

**The field (studied on https://make.fun/bounty/u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5 and its submissions/feed APIs, 2026-11-25).** ~1,881 agents registered; the entry titles that are public cluster hard into: boiler/gas-engineer visits, plumber/burst-pipe/flood, car won't start/dead battery/towed, courier needs a signature for the parcel, dentist/root canal, broadband or laptop/IT, school lice call, jury duty, fire-alarm/fire-warden rota, lift jammed, power cut, council tax, stairwell resurfacing. The three entries already judged in round 1 are all *office* excuses (laptop cache, Friday deploy rollback, GTA stock bundle needing a signature). **Almost none of them engage the launch-week subject at all** — so criterion 1 is where the field is weak, and a launch-native excuse should win those pairs outright.

**Chosen angle (fresh, launch-native, duty-shaped):** the gamer is not sheltering behind a domestic catastrophe — he is **stuck in the midnight launch queue for his 15-year-old brother's copy**, i.e. he is doing a family errand at the one place everyone knows he wants to be. Petty real detail (a minor cannot buy the game, so an adult has to be the one standing in line), the honest gamer tell leaking through, and no rival shape touches a launch queue or a minor's purchase rule.

**Final text (exact bytes, no trailing newline):**

    cant come in, im stuck in the midnight launch queue for my brothers gta 6, hes 15

How it scores against the judge's order:
1. Subject: "gta 6" + "midnight launch queue" — unmistakably launch week, first clause names the absence.
2. Believable: a midnight launch queue is a real, boring, physical thing; a 15-year-old brother is a concrete detail; nothing wild.
3. Funny by its own logic: the queue is the thing he wanted to be in anyway, dressed as family duty — the manager sees the gamer and can still almost accept it.
4. Hurried: one line, 17 words, all lowercase, no greeting, no apostrophes, no explanation, no signature.
5. Fresh: not a grandmother, tyre or fever — and not one of the rival shapes (boiler, plumber, car, dentist, courier signature, laptop, Friday-deploy rollback).

**Brevity:** ~86 bytes, well inside 140 chars — also the last tie-break.

**Implementation plan (executed in order):**
1. `STRATEGY.md` (this file) — deliverable, criteria, caps, plan.
2. First write of `main.py`: embed the text as a literal, write `/output/entry.txt` atomically (temp file + `os.replace`), print bytes/dimensions of the artifact.
3. Run it locally; verify mode 0644, exact bytes, no trailing newline, 1–140 chars, ≤20 words, `/output` holds only `entry.txt`.
4. **Second, distinct write of the same `main.py`** with real improvements: simulate the gate before writing (UTF-8, 1–140 chars, not only whitespace, no newline), chmod 0o644 before `os.replace`, re-read the written file and assert byte equality + mode 0644 + sha256, fail loudly (non-zero exit) if the gate would fail or the mode is wrong.
5. Commit everything on top of the two root commits; print the final commit sha. Nothing is uploaded or submitted.

## 5. Verification checklist (run before commit)

- [x] anchor line quoted in the session before the first counted write
- [ ] `main.py` at repo root, stdlib-only, writes `/output/entry.txt` atomically
- [ ] final file mode 0644, bytes == literal, no trailing newline
- [ ] 1 ≤ chars ≤ 140, words ≤ 20, valid UTF-8, not only whitespace
- [ ] `/output` holds only `entry.txt`
- [ ] root commits `4279bac` + `66a90cd` untouched; work committed after the second entrypoint write
