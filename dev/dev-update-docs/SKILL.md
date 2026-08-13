---
name: dev-update-docs
description: Analyzes repository code changes, updates the '.docs/' directory, and checks '.docs/memory-bank/' (owned by the dev-memory-bank skill) for consistency against the main docs and codebase — reporting findings without modifying the memory bank.
version: 1.1.0
author: Albert
license: MIT
metadata:
  hermes:
    tags: [Documentation, DevOps, Markdown]
    category: dev
    related_skills: [dev-memory-bank]
    requires_tools: [read_file, write_file, terminal, patch, delegate_task]
    model:
      provider: openrouter
      model: openai/gpt-oss-120b:free
---

# Update Docs Skill

This skill guides the agent to systematically scan a repository for missing or outdated documentation and update its Markdown files inside the `.docs/` folder. It also verifies that `.docs/memory-bank/` (a directory owned and written exclusively by the `dev-memory-bank` skill) stays consistent with the main `.docs/` documentation and the actual codebase, writing a report when they drift apart.

## When to Use

- After source code changes are committed or staged, so `.docs/` reflects the current implementation.
- When the user requests "update docs", "refresh documentation", or similar.
- Periodically, to keep architecture, API, instructions, and feature docs in sync with the code.
- Whenever a `.docs/memory-bank/` directory exists, to check it for consistency against the main docs and codebase (read-only — never edit it).

## Procedure

Execute the following steps precisely. The detailed analysis methodology lives in `references/documentation-analysis.md`, and the memory-bank consistency sub-workflow in `references/memory-bank-consistency.md` — load those as needed.

### 1. Context Assessment

- Check the contents of the current workspace root.
- Run `git status` or inspect recently modified source files to see what changed.
- Check for deleted files (e.g. `git diff --diff-filter=D --name-only`) and note any docs that may need references removed.
- Read the diff of modified source files to understand what changed vs the existing docs. For committed changes (post-refactor), use `git diff HEAD~N..HEAD --name-only` then `git diff HEAD~N..HEAD` for the cumulative diff. For unstaged changes, use `git diff --no-color`.
- **Establish directory structure**: if `.docs/` does not exist, create it with standard subdirectories (`mkdir -p .docs/{modules,reference,ai}`). Let the actual repository structure guide the folders — don't force folders that don't map to real subsystems.

### 2. Documentation Alignment

- Locate `.docs/` in the repository root.
- Inspect existing `.md` files to see if architecture, API, instructions, or features have fallen out of sync with the implementation.
- Build a mapping of which docs need updates and what kind (minor patch vs major rewrite).

### 3. Memory Bank Consistency Check

- **Boundary rule**: `.docs/memory-bank/` is owned and written exclusively by the `dev-memory-bank` skill. Never create, edit, or delete files under it. Treat it as read-only input.
- Check whether `.docs/memory-bank/` exists. If it does not, skip this step entirely (generate no report).
- If it exists, follow `references/memory-bank-consistency.md` to cross-check it (read-only) against the main `.docs/` files and the current source code, and write findings to `.docs/reports/memory-bank-consistency.md`.
- This step runs independently of steps 1–2: even if the main docs need no changes, the memory-bank check must still run and report when `.docs/memory-bank/` exists.

### 4. Execution

- If updates or new files are required, write or edit the markdown directly inside `.docs/` (excluding `.docs/memory-bank/`).
- Use `patch` for targeted updates to existing docs (fixing stale references, adding sections). Use `write_file` for new files or complete rewrites.
- For large updates spanning multiple topics, use `delegate_task` to parallelize creation across subagents (one per doc topic).
- **CAUTION**: very large documents (250+ lines, especially with diagrams) may time out when delegated. In practice docs up to ~1200 lines have completed (~7 min); the risk is acceptable vs sequential work. Prefer delegation for complex multi-topic updates but design independent task boundaries.
- Before ANY write or patch, verify the target path does not resolve inside `.docs/memory-bank/`. If a correction would touch the memory bank, abort that write and record it in the consistency report instead.
- Ensure clear, concise markdown formatting.

### 5. Verification

See the `## Verification` checklist below.

## Pitfalls

- **Forgetting to check for deleted files**: removed source files leave stale doc references. Always check `git diff --diff-filter=D --name-only` during context assessment and plan to remove/update references to deleted files, classes, functions, or APIs.
- **Assuming directory structure**: don't impose a predefined doc structure that doesn't match the codebase. Let actual modules and components guide the `.docs/` layout.
- **Over-relying on git diff alone**: `git diff` shows what changed but not always the full impact — a utility change may affect multiple modules. Consider broader implications.
- **Writing into `.docs/memory-bank/`**: this skill must never modify the memory bank, not even a "helpful" correction. That directory is the `dev-memory-bank` skill's exclusive domain. Always write findings to `.docs/reports/memory-bank-consistency.md` instead.
- **Stale references after renames/removals**: after renaming/removing packages, scripts, config keys, APIs, or directory paths, grep the whole `.docs/` tree for the old names (see Verification).
- **Endpoint parameter drift**: when updating endpoint docs, cross-check supported file types, enum values, and validation rules against actual route handlers (Zod schemas, validation arrays) — existing docs may already be wrong.
- **Broken markdown tables after patch edits**: `patch` can introduce/drop leading pipes, creating `|||` rows or broken separators. Verify and fix after any table edit (see Verification).
- **Trusting subagent summaries**: delegate summaries are self-reported and may overclaim. Always `read_file` the actual output before accepting it.

## Verification

- List all `.md` files in `.docs/` (excluding `.docs/memory-bank/`) to confirm the expected set exists.
- Check file sizes with `wc -l` to catch empty or truncated files.
- Spot-check the first 10–20 lines of each new file to verify content quality.
- **Catch-all stale reference sweep**: after changes that rename/remove packages, scripts, config keys, APIs, or directory paths, run `search_files(pattern='old-package-name|old-script-name|old-api-route|old-directory-path', path='.docs/')` for the old names across the entire docs directory. Subagents only update files assigned to them — this grep catches references in files they didn't know about.
- Concrete patterns to search when applicable: **class/interface names**, **method/function names**, **command IDs**, **config keys**, **endpoint URLs**, **file paths**, **dependency package names**, **directory path renames** (e.g. after moving `src/components/` to `src/services/`, grep for `src/components/`).
- **Markdown table formatting after patch operations**: after any table edit, (1) `read_file` and visually confirm each data row starts with `|| ` (two pipes + space) and separator rows with `|` + dashes + `|`; (2) if display is ambiguous, verify with `od -c` — e.g. `sed -n '18p' .docs/reference/configuration.md | od -c`; (3) fix artifacts with further `patch` calls targeting the exact wrong prefix.
- **Verify API endpoint parameters against source code**: cross-check supported file types, enum values, and validation rules against actual route handlers in `src/routes/`. Search for Zod schemas and validation arrays. (See `references/ocr-endpoint-verification.md` in the target repo for a worked example.)
- If using `delegate_task`, verify the subagent's summary claims by reading back the files it created — do NOT trust the summary alone.
- **Memory-bank safety**: confirm no file under `.docs/memory-bank/` was created, edited, or deleted during this run.
- **Consistency report**: if the memory-bank check found issues, confirm `.docs/reports/memory-bank-consistency.md` exists and spot-check its content.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Docs already up to date, and no memory-bank issues | Respond exactly `[SILENT]` |
| `.docs/memory-bank/` does not exist | Skip the consistency check entirely |
| Memory-bank drift found | Write `.docs/reports/memory-bank-consistency.md`; never touch the memory bank |
| Large multi-topic update | `delegate_task` with independent task boundaries, then verify by reading back |

## Related

- `references/documentation-analysis.md` — the full analysis methodology (languages, architecture, technology inventory, engineering/runtime/deployment/data/integration analysis, AI-agent docs, reusability, tech debt, update mode, editing strategies, parallelization, factual accuracy, success criteria).
- `references/memory-bank-consistency.md` — the memory-bank consistency check sub-workflow.
