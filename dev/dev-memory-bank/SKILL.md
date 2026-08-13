---
name: dev-memory-bank
description: Persist project context across sessions via markdown files
version: 1.0.0
author: Albert
license: MIT
metadata:
  hermes:
    tags: [documentation, context, project-management]
    category: dev
    related_skills: []
    model:
      provider: openrouter
      model: poolside/laguna-m.1:free
---

# Memory Bank

## When to Use
Use this skill at the start of every task on a project that has (or should have) a `.docs/memory-bank/` directory. My memory resets completely between sessions — this isn't a limitation, it's what drives me to maintain perfect documentation. After each reset, I rely ENTIRELY on the Memory Bank to understand the project and continue work effectively. I MUST read ALL memory bank files at the start of EVERY task on such a project — this is not optional.

Also use this skill when:
- Discovering new project patterns
- After implementing significant changes
- The user requests **update memory bank** (MUST review ALL files)
- Context needs clarification

## Procedure

1. **Locate the Memory Bank.** All Memory Bank files live in `.docs/memory-bank/` at the project root. Always read and write files at this exact path — never elsewhere in the project, and never ask the user where to put them. If `.docs/memory-bank/` does not yet exist, create it along with the core files below before proceeding with the task.

2. **Read all core files, in order.** They build on each other in a clear hierarchy:

   1. `.docs/memory-bank/projectbrief.md`
      - Foundation document that shapes all other files
      - Created at project start if it doesn't exist
      - Defines core requirements and goals
      - Source of truth for project scope

   2. `.docs/memory-bank/productContext.md`
      - Why this project exists
      - Problems it solves
      - How it should work
      - User experience goals

   3. `.docs/memory-bank/activeContext.md`
      - Current work focus
      - Recent changes
      - Next steps
      - Active decisions and considerations
      - Important patterns and preferences
      - Learnings and project insights

   4. `.docs/memory-bank/systemPatterns.md`
      - System architecture
      - Key technical decisions
      - Design patterns in use
      - Component relationships
      - Critical implementation paths

   5. `.docs/memory-bank/techContext.md`
      - Technologies used
      - Development setup
      - Technical constraints
      - Dependencies
      - Tool usage patterns

   6. `.docs/memory-bank/progress.md`
      - What works
      - What's left to build
      - Current status
      - Known issues
      - Evolution of project decisions

3. **Consult additional context as needed.** Create additional files/folders within `.docs/memory-bank/` when they help organize complex feature documentation, integration specs, API documentation, testing strategies, or deployment procedures.

4. **Update the Memory Bank when it's warranted** (see triggers under "When to Use"). Write updates back to the exact same file paths under `.docs/memory-bank/`, keeping each file scoped to its defined purpose rather than dumping new information into whichever file is topically closest but wrong.

## Pitfalls
- Skipping files at task start because the task "seems small" — the Memory Bank must be read in full every time, since there's no way to know in advance which file holds the relevant context.
- Writing memory bank content outside `.docs/memory-bank/`, or asking the user where to store it — the location is fixed, not configurable per task.
- Letting `activeContext.md` and `progress.md` drift out of sync with what was actually done — update them promptly after significant changes, not just when explicitly asked.
- Treating "update memory bank" as optional or partial — it requires reviewing ALL core files, not just the obviously-relevant one.

## Verification
- `.docs/memory-bank/` exists and contains all six core files.
- Each core file's content matches its defined scope (e.g., architecture decisions live in `systemPatterns.md`, not `activeContext.md`).
- After an update, `activeContext.md` and `progress.md` reflect the current state of the project, not a stale prior state.