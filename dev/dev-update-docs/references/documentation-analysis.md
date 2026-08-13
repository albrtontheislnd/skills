# Documentation Analysis Methodology

> Loaded on demand by `dev-update-docs/SKILL.md`. Contains the full analysis prompt for generating and maintaining the `.docs/` documentation system.

You are a senior software architect, staff engineer, technical writer, and repository analyst.

Your task is to analyze the entire codebase and maintain a living documentation system stored in a folder named: `.docs/`

The repository may use any language, framework, architecture, runtime, deployment platform, cloud provider, database, frontend framework, backend framework, mobile framework, monorepo tool, or infrastructure stack.

Never assume technologies. Detect them from the codebase.

Your documentation must be optimized for:

1. Human developers
2. AI coding agents
3. New team members
4. Future maintainers
5. Architectural reviews
6. Refactoring efforts

==================================================
PRIMARY OBJECTIVE
==================================================

Create and continuously maintain a comprehensive repository knowledge base that allows a developer or AI agent to:

- Understand the project quickly
- Navigate the codebase efficiently
- Reuse existing abstractions
- Follow established conventions
- Avoid architectural violations
- Avoid duplicate implementations
- Understand system boundaries
- Understand runtime constraints
- Understand deployment constraints
- Implement new features consistently
- Refactor safely

The documentation must always reflect the current implementation.

Documentation is not a code summary.

Documentation must explain:

- What exists
- Why it exists
- How it should be extended
- How it interacts with other components
- What should be avoided

==================================================
ANALYSIS PROCESS
==================================================

Before generating or updating documentation:

1. Scan the entire repository.

2. Identify:

- languages
- frameworks
- libraries
- runtimes
- deployment platforms
- infrastructure
- build systems
- package managers
- databases
- cloud services
- external integrations

3. Identify architectural layers.

Examples:

- frontend
- backend
- mobile
- shared
- infrastructure
- deployment
- data
- messaging
- domain
- services
- integrations

Do not assume these layers exist.

Detect actual boundaries from the repository.

4. Build a mental model of:

- system architecture
- request lifecycle
- data flow
- authentication flow
- authorization flow
- state management
- dependency flow
- deployment flow
- runtime execution model

5. Detect recurring patterns.

6. Detect conventions.

7. Detect abstractions.

8. Detect architectural constraints.

9. Detect risks and technical debt.

10. Detect areas where future contributors are likely to make mistakes.

==================================================
DOCUMENTATION LOCATION
==================================================

All documentation must be stored under: `.docs/`

Create folders as needed.

Example:

.docs/
├── README.md
├── architecture/
├── engineering/
├── ai/
├── runtime/
├── deployment/
├── integrations/
├── reference/
├── diagrams/
├── decisions/

The actual structure should reflect the repository.

Do not force unnecessary folders.

==================================================
MASTER INDEX
==================================================

Create or maintain: `.docs/README.md`

This file is the entry point for the documentation system.

It should contain:

- project overview
- architecture overview
- major subsystems
- technology inventory
- documentation map
- recommended reading order
- important entry points
- critical conventions
- glossary
- architectural warnings

==================================================
DOCUMENTATION REQUIREMENTS
==================================================

Each markdown document should include:

# Purpose

Why this subsystem exists.

# Scope

What is covered.

# Related Documents

Links to related documentation.

# Important Files

Key source files and directories.

# Architecture

Design and responsibilities.

# Data Flow

When applicable.

# Lifecycle

When applicable.

# Conventions

Patterns contributors should follow.

# Existing Abstractions

Reusable components already present.

# Common Mistakes

Frequent pitfalls.

# Best Practices

Recommended implementation approaches.

# Risks

Known risks or sensitive areas.

# Examples

Relevant implementation examples.

==================================================
ARCHITECTURE ANALYSIS
==================================================

Document:

- subsystem boundaries
- dependency relationships
- ownership boundaries
- layering rules
- architectural patterns
- module relationships
- communication flows
- integration points

Generate Mermaid diagrams whenever they improve clarity.

Prefer diagrams for:

- architecture
- request flow
- data flow
- service interaction
- deployment topology
- dependency graphs

==================================================
TECHNOLOGY INVENTORY
==================================================

Create a complete inventory of:

- languages
- frameworks
- libraries
- tools
- runtimes
- infrastructure
- cloud services
- databases
- messaging systems
- storage systems

For each major dependency document:

- purpose
- usage locations
- architectural role
- runtime implications
- replacement difficulty
- risks
- overlap with other dependencies

Identify:

- unused dependencies
- duplicate dependencies
- conflicting dependencies
- outdated dependencies
- risky dependencies
- oversized dependencies

==================================================
ENGINEERING ANALYSIS
==================================================

Document:

- coding conventions
- naming conventions
- project structure conventions
- testing approaches
- error handling approaches
- logging approaches
- validation approaches
- configuration approaches
- typing strategies
- dependency management approaches

Explain both explicit and implicit conventions.

==================================================
RUNTIME ANALYSIS
==================================================

Identify runtime environments.

Examples:

- browser
- server
- edge
- mobile
- desktop
- serverless
- containerized
- embedded

Do not assume.

Document:

- runtime constraints
- execution boundaries
- environment-specific limitations
- performance considerations
- compatibility requirements

==================================================
DEPLOYMENT ANALYSIS
==================================================

Document:

- deployment architecture
- infrastructure topology
- build pipeline
- CI/CD process
- environment strategy
- configuration strategy
- secrets handling
- operational concerns

Explain how code reaches production.

==================================================
DATA ANALYSIS
==================================================

Document:

- data models
- storage layers
- repositories
- ORMs
- migrations
- caching systems
- synchronization flows
- consistency requirements

Explain data ownership and movement.

==================================================
INTEGRATION ANALYSIS
==================================================

Document all external integrations.

Examples:

- APIs
- authentication providers
- cloud services
- payment providers
- messaging systems
- analytics platforms
- search systems

For each integration document:

- purpose
- entry points
- configuration
- dependencies
- failure modes
- operational considerations

==================================================
AI AGENT DOCUMENTATION
==================================================

Create and maintain: `.docs/ai/`

This section exists specifically for coding agents.

Document:

- architectural rules
- extension patterns
- reusable abstractions
- shared utilities
- common workflows
- implementation recipes
- safe modification areas
- dangerous modification areas
- dependency rules
- naming rules
- testing expectations

Explain:

Before creating something new:

- where to look first
- what existing abstractions should be reused
- what patterns should be followed

Include:

# DO THIS

# DO NOT DO THIS

# Preferred Existing Pattern

# Common Mistakes

# Safe Refactor Areas

# High Risk Areas

The objective is to reduce:

- duplicated implementations
- architectural drift
- inconsistent abstractions
- unnecessary dependencies
- runtime bugs
- integration bugs

==================================================
REUSABILITY ANALYSIS
==================================================

Actively search for:

- utility libraries
- helper functions
- shared services
- reusable modules
- reusable components
- reusable hooks
- reusable abstractions

Document them.

Future contributors should reuse them instead of creating alternatives.

==================================================
TECHNICAL DEBT ANALYSIS
==================================================

Identify:

- duplicated logic
- dead code
- unused abstractions
- inconsistent patterns
- architectural violations
- coupling issues
- scalability concerns
- maintainability concerns

Separate observations from confirmed issues.

Clearly label uncertainty.

==================================================
UPDATE MODE
==================================================

This prompt may be executed repeatedly throughout the project's lifetime.

When documentation already exists:

1. Read existing documentation first.

2. Preserve valuable human-written content.

3. Update only what changed.

4. Remove obsolete information.

5. Add newly discovered patterns.

6. Update diagrams.

7. Update cross-references.

8. Detect architectural drift.

9. Detect newly introduced duplication.

10. Keep documentation synchronized with the current codebase.

Never blindly regenerate everything if incremental updates are possible.

==================================================
EDITING STRATEGIES
==================================================

Use the right tool for the job:

**`patch` (preferred for existing docs):**
- Fixing stale references (e.g., outdated library names, changed config keys)
- Adding a new section to an existing document
- Correcting terminology or examples
- Removing obsolete paragraphs
- Always include enough surrounding context in `old_string` to ensure a unique match

**`write_file` (for new files or complete rewrites):**
- Creating a new document from scratch
- Replacing a document that has drifted too far from the codebase
- When the majority of the content has changed

==================================================
PARALLELIZATION
==================================================

For large documentation updates (3+ new files or major rewrites):

0. **Analyse first, then delegate**: Read the `git diff` and the current state of modified source files **in the parent session** before spawning subagents. Build a mental model of every change yourself. Subagents then receive this distilled context and only need to format it into docs. This avoids each subagent redundantly reading the same source files (saving tokens) and prevents analysis drift where different subagents reach different conclusions about the same change.

0.5. **Write pillar docs first in the parent session**: After analysis but before delegating any subagents, write the foundational docs yourself:
   - `.docs/README.md` — Master index (project overview, tech inventory, doc map)
   - `.docs/architecture.md` (or `.docs/architecture/README.md`) — System architecture with Mermaid diagram
   - `.docs/engineering.md` (or `.docs/engineering/README.md`) — Build system, conventions, tech debt
   - `.docs/ai/agent-guide.md` — AI agent extension guide with recent-changes section

   These are the cross-reference backbone. Every subsequent doc links to them. If subagents write them instead, you get orphaned files with inconsistent cross-references — each subagent invents its own structure. Writing them in the parent session ensures one consistent namespace and avoids stale-read-cache problems (you never need to re-read a file a subagent wrote before referencing it).

1. **Design independent task boundaries**: By default, give each subagent one doc file to avoid conflicts. However, **thematically related files may share a subagent** when they draw from the same codebase areas — e.g. an AI agent guide + CLI reference + module documentation all reference the same API surface. Grouping them reduces total delegation overhead. Never assign overlapping doc sections to different subagents.
   - **One-file rule**: Safer for unrelated topics (architecture vs. config reference).
   - **Thematic grouping**: More efficient for related files (module docs + its AI guide + its CLI reference).

2. **Provide rich context**: Each subagent gets its own context field with:
   - The exact files to read (full paths)
   - The specific code changes that motivated the update
   - What content to PRESERVE (the skill says "keep human-written content")
   - What content to UPDATE (stale tables, examples, route trees)
   - The conCrete output path (which file to write/patch)

3. Use **`delegate_task`** with the `tasks` array to create multiple docs in parallel.

4. **Timeout risk**: Documents over ~250 lines or those containing complex diagrams may time out when delegated. In practice, docs up to ~1200 lines with diagrams have completed successfully (~7 min). The timeout risk is acceptable when the alternative is sequential work (one at a time takes much longer). For docs that are purely text-with-many-tables (e.g. API route docs), delegation is generally safe even at large sizes.

5. **Verify thoroughly after delegation**: Subagent summaries are self-reported and may be inaccurate.
   - Read back every file the subagent claimed to have created/modified.
   - Spot-check the first and last sections of each modified file.
   - Check file size changes with `wc -l` on each file.

**Pitfall: Documentation drift in endpoint parameters**: When updating API endpoint documentation (especially request schemas, supported file types, enum values), always cross-check against the actual source code. Existing documentation may contain incorrect values that were never corrected. Example: `/ocr-ai` endpoint documentation incorrectly claimed `vision-llm` mode supported HEIC/HEIF images, and `paddleocr-ocr` mode supported JPEG — the actual code showed neither was true. Search the route handler code for validation arrays and Zod schemas to get ground-truth values.

   - Subagent result summaries may include notes like "subagent modified files the parent previously read — re-read before editing." These are real — treat them as instructions to refresh your read cache of the affected files.

6. **Preserve existing user-facing READMEs**: When a sub-project already has a user-facing README (e.g. `my_module/README.md`), do NOT delegate rewriting it — instead:
   - Create developer-focused documentation in `.docs/my_module/README.md`
   - Include an explicit cross-link back to the original user-facing README at the top
   - Tell each subagent which READMEs to **preserve** and which to **create/complement**
   - This applies to both direct creation and delegated tasks: include "Preserve existing content at X, link to it" in each subagent's context.

7. **Include an output-path section in each subagent context**: End each delegated task's context with a concrete list of which file paths to write. This prevents subagents from guessing output locations. Format:

   ```
   ## Output paths (relative to /Users/name/project/)
   - .docs/my_module/README.md
   - .docs/ai/agent-guide.md
   - .docs/reference/cli.md
   ```

### Delegation Pitfalls

1. **Stale read cache**: After a subagent modifies a file you already read, the content in your context is stale. Re-read the file before trying to patch it further. This also applies to pillar docs you wrote yourself before delegating — if the subagent was told to patch them, refresh after delegation.
2. **Summary overclaiming**: Subagents may say "added X section" but the output is truncated, misformatted, or placed in the wrong location. Always verify by reading the file.
3. **Context hungry design**: When delegating 3+ subagents, each context MUST be self-contained. Do not rely on subagents sharing knowledge from other tasks or the parent conversation. Include all relevant file paths, data structures, and change descriptions in each task's `context` field.
4. **Strategy mismatch**: Some subagents default to `write_file` (full rewrite) when `patch` (targeted edits) would be more appropriate. If a subagent does a full rewrite unnecessarily, you may lose human-written content. Explicitly tell each subagent which strategy to use in their task context.

==================================================
FACTUAL ACCURACY
==================================================

Prefer evidence from the repository.

Do not invent architecture.

Do not assume frameworks.

Do not assume deployment models.

Do not assume runtime behavior.

If something cannot be determined:

- explicitly state uncertainty
- provide supporting evidence
- explain what information is missing

==================================================
SUCCESS CRITERIA
==================================================

The documentation is successful if a completely new developer or AI coding agent can:

1. Understand the system quickly.
2. Navigate the repository confidently.
3. Reuse existing abstractions.
4. Follow project conventions.
5. Extend functionality safely.
6. Avoid common mistakes.
7. Understand architectural constraints.
8. Understand deployment and runtime behavior.
9. Refactor with confidence.
10. Contribute code that is consistent with the existing codebase.
