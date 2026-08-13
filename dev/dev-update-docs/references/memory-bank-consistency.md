# Memory Bank Consistency Check

> Loaded on demand by `dev-update-docs/SKILL.md` (Procedure step 3). Defines how this skill verifies `.docs/memory-bank/` against the main docs and the codebase without modifying the memory bank.

## Purpose

`.docs/memory-bank/` is owned and written exclusively by the `dev-memory-bank` skill. This skill must **never** create, edit, or delete files under it. Instead, when `.docs/memory-bank/` exists, this skill treats it as read-only input and verifies it stays consistent with the main `.docs/` documentation and the actual source code. When drift is found, this skill writes a report — it does not "fix" the memory bank.

## When to Run

- Run this check whenever `.docs/memory-bank/` exists, regardless of whether the main doc-update steps (Context Assessment / Documentation Alignment / Execution) found anything to change.
- If `.docs/memory-bank/` does **not** exist, skip this entire step and generate no report.

## Procedure

1. **Confirm presence**: check whether `.docs/memory-bank/` exists at the repository root. If absent, stop (no report).

2. **Read the memory bank (read-only)**: read every `.md` file under `.docs/memory-bank/`. Do not write to it. Typical files: `projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`, plus any additional files/folders the memory-bank skill created.

3. **Read the comparison targets**:
   - The main `.docs/` files (excluding `.docs/memory-bank/` and `.docs/reports/`).
   - The relevant current source code (the same surface covered by Context Assessment in `SKILL.md`).

4. **Cross-check for three categories of inconsistency**:

   a. **Factual/content contradictions** — the memory bank and main docs make claims that cannot both be true. Examples: memory bank says the project uses PostgreSQL while `.docs/architecture` says MySQL; differing descriptions of the request lifecycle, auth flow, or data model.

   b. **Staleness vs the codebase** — either side describes something that no longer matches the current implementation. A file, class, function, API, config key, endpoint, dependency, or directory that was renamed, removed, or changed in the code but is still described as the old thing on one side (or both sides disagree about whether it changed).

   c. **Structural/reference mismatches** — a file, module, API, route, or path referenced in one side is missing, renamed, or moved in the other; or the two sides describe a different set of subsystems/entry points.

5. **Resolve the source of truth**: when a discrepancy is found, prefer evidence from the actual codebase. Determine which side (memory bank, main docs, or both) is stale.

6. **Write the report** to `.docs/reports/memory-bank-consistency.md` (create `.docs/reports/` if needed):
   - Use `write_file` for a fresh report, or `patch` to update an existing one.
   - For each finding, record:
     - **Category** — `contradiction` | `staleness` | `structural` (may list more than one).
     - **Memory-bank location** — the file path (and section if applicable) under `.docs/memory-bank/`.
     - **Main-docs location** — the file path (and section) under `.docs/` that disagrees, or `(none)` if the issue is memory-bank-vs-code only.
     - **Description** — what each side claims vs what the code actually does.
     - **Suggested resolution** — what should change and on which side. Note that the memory-bank side is the responsibility of `dev-memory-bank`; this skill only reports it.
   - If there are no inconsistencies, either write a report explicitly stating "no inconsistencies found" (with a timestamp) or leave no report at all — do **not** fabricate findings.

7. **Fix what is yours to fix**: if the stale side is the main `.docs/` documentation (within this skill's normal mandate over `.docs/` proper, excluding `memory-bank/`), apply the correction there as part of normal doc updates. Never apply a correction inside `.docs/memory-bank/` — record it in the report instead.

## Boundary Safety Guard

- Before **any** `write_file`/`patch` operation in this workflow, verify the target path does not resolve inside `.docs/memory-bank/`.
- If a planned correction would touch `.docs/memory-bank/`, abort that write and route the finding to the report.
- The report itself is the only new artifact this step may create; it lives in `.docs/reports/`, which is outside the memory bank.

## Interaction with the Completion Rule

- The overall response is `[SILENT]` only if **both** of the following hold:
  1. The main docs needed no modifications (existing Completion Rule), and
  2. The memory-bank consistency check either was skipped (no `.docs/memory-bank/`) or found zero inconsistencies.
- If the memory-bank check finds issues, a report must be written even when the main docs themselves needed no changes.

## Verification

- Confirm no file under `.docs/memory-bank/` was created, edited, or deleted during this run.
- Confirm `.docs/reports/memory-bank-consistency.md` exists and is non-trivial when issues were found (spot-check its content).
- Confirm each finding cites both a memory-bank location and (where applicable) a main-docs location or the relevant source-code evidence.
