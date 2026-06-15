# narrative-style-editor

A Claude skill that reviews and rewrites pasted text (markdown or plain) against 38
rules for structure, clarity, data-driven precision, and editorial integrity. It
flags gaps where the author must supply missing data rather than guessing, and runs
a bounded drift-verification pass so the rewrite does not introduce urgency, spin,
attribution distortion, technical oversimplification, or hallucinated data.

## Invocation

`/narrative-style-editor` — paste the text to review, with an optional mode and `--audience`:

| Mode | Effect |
| :--- | :--- |
| (default) | Console response: clean rewrite + changes table + summary + checklist |
| `--show-changes` | Same, plus inline ✍️ / 🗑️ / 📊 / ⚠️ markers at every change site |
| `--dry-run` | Analysis only: changes table, summary, gap list, verification — no rewrite block |

Add `--audience leadership|peers|xfn` to prioritize rules for the reader. If the
input is markdown, the rewrite preserves its formatting.

## Layout

- `SKILL.md` — skill definition and workflow.
- `references/PRINCIPLES.md` — the 38 writing rules (numbered 1-38).
- `references/OUTPUT_FORMAT.md` — console response, changes table, violation summary.
- `references/VERIFICATION.md` — the bounded drift-verification protocol.
- `references/EXAMPLE.md` — a worked end-to-end example.
- `scripts/` — deterministic helpers (Python 3.9+, stdlib only): output assembly,
  acronym scan, false-profundity scan. See `scripts/README.md`.
- `.claude/commands/narrative-style-editor.md` — the slash-command wrapper.

## Development

See `CHANGELOG.md` for the running history and `REMEDIATION_PLAN.md` for the
roadmap derived from the architecture review.
