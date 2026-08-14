# Hermes Agent Skills

A personal collection of reusable skills for [Hermes Agent](https://github.com/NousResearch/hermes-agent). Each skill packages domain-specific instructions, optional reference material, and helper scripts in a self-contained directory.

The collection covers development workflows, finance and economics, Chinese-language learning, reading research, and Vietnam policy tracking.

## Repository layout

```text
.
├── chinese-learning/
│   ├── hanzi-analyzer/
│   ├── zh-vn-translate/
│   └── zh-vn-vocab/
├── dev/
│   ├── dev-memory-bank/
│   └── dev-update-docs/
├── finance/
│   ├── apac-econ-tracker/
│   ├── gold-market-summary/
│   └── vcbf-analysis/
├── reading/
│   └── economics-book-finder/
├── vietnam/
│   └── vn-policy-tracker/
├── apac-briefing-reports/       # Generated APAC briefing output
├── .docs/                       # Skill-authoring documentation
└── skills.code-workspace       # VS Code workspace
```

Most skill directories contain:

- `SKILL.md` — required metadata and instructions for the agent.
- `references/` — curated source lists, templates, and supporting documentation where needed.
- `scripts/` — optional deterministic helper programs.

## Skills

### Chinese learning

| Skill | Version | Description |
|---|---:|---|
| [`hanzi-analyzer`](chinese-learning/hanzi-analyzer/) | 1.2.0 | Analyzes Chinese characters, including radicals, Sino-Vietnamese pronunciation, mnemonics, and stroke order; can generate an interactive `hanzi-writer` visualization. |
| [`zh-vn-translate`](chinese-learning/zh-vn-translate/) | 1.0.0 | Translates Chinese into Vietnamese and explains meaning, grammar, sentence structure, and important vocabulary. |
| [`zh-vn-vocab`](chinese-learning/zh-vn-vocab/) | 1.0.0 | Helps Vietnamese learners understand Mandarin vocabulary, grammar, idioms, usage, and natural examples. |

### Development

| Skill | Version | Description |
|---|---:|---|
| [`dev-memory-bank`](dev/dev-memory-bank/) | 1.0.0 | Persists project context across sessions through a structured `.docs/memory-bank/` directory. |
| [`dev-update-docs`](dev/dev-update-docs/) | 1.1.0 | Reviews repository changes and keeps documentation under `.docs/` aligned with the codebase. |

### Finance and economics

| Skill | Version | Description |
|---|---:|---|
| [`apac-econ-tracker`](finance/apac-econ-tracker/) | 1.0.0 | Builds periodic briefings on Asia-Pacific economics, markets, trade, labor, central banks, and Vietnam-specific developments. |
| [`gold-market-summary`](finance/gold-market-summary/) | 1.0.0 | Produces a live, data-driven summary of global gold price movements over the previous 14 calendar days. |
| [`vcbf-analysis`](finance/vcbf-analysis/) | — | Directory reserved for a VCBF analysis skill; its current `SKILL.md` is an empty stub. |

### Reading

| Skill | Version | Description |
|---|---:|---|
| [`economics-book-finder`](reading/economics-book-finder/) | 1.2.0 | Finds and ranks prominent economics books for a target year using curated sources, cross-source scoring, and generated Markdown reports. |

### Vietnam

| Skill | Version | Description |
|---|---:|---|
| [`vn-policy-tracker`](vietnam/vn-policy-tracker/) | 1.0.0 | Collects and ranks Vietnamese government policies, laws, decrees, circulars, and drafts published during the previous 14 days. |

## Skill format

Skills use a `SKILL.md` file with YAML frontmatter followed by Markdown instructions. The frontmatter commonly defines:

- Skill name, description, version, author, and license.
- Hermes categories and search tags.
- Related skills and required or fallback tools.
- Optional platform, environment-variable, and automation configuration.

See [`.docs/creating-skills.md`](.docs/creating-skills.md) for the full authoring guide and metadata format.

## Generated reports and data

Skills that create reports are expected to write generated data to the workspace output directories described by their instructions, rather than to their source directories. For example:

- `apac-briefing-reports/` stores timestamped APAC economic briefings and related run artifacts.
- `economics-book-finder` writes reports to an `economics-book-reports/` directory in the runtime workspace.
- `vn-policy-tracker` writes reports to a `vn-policy-briefings/` directory in the runtime workspace.

Generated report history should be preserved; recurring skills should not overwrite earlier reports.

## Development

This repository is primarily documentation and lightweight Python tooling. There is no project-wide package manager or test runner. Individual scripts document their own command-line usage and dependencies; Python standard-library scripts can generally be run directly with Python 3.

When adding a skill:

1. Create a directory under the appropriate category.
2. Add a `SKILL.md` with valid Hermes metadata and clear trigger conditions.
3. Add references and scripts only when they support the skill's workflow.
4. Keep generated user output outside the skill source directory.
5. Validate the skill's commands and update this README when the collection changes.

## License

Individual skills currently declare the MIT license in their metadata unless otherwise noted.