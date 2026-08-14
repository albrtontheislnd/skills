# APAC Briefing Reports

Output folder for the `apac-econ-tracker` skill.

Each run of the skill writes its briefing report here as a Markdown file named by the date and time it was run:

```
apac-econ-brief_<YYYY-MM-DD>_<HHMM>.md
```

e.g. `apac-econ-brief_2026-08-14_1345.md`.

Any other files the skill produces (raw data-calendar output, RSS pulls, saved source lists) also go here, prefixed with the same date/time so they stay grouped with the run that created them.

Keep the history — do not overwrite or delete older reports, so briefs can be compared over time.