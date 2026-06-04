# narrative-style-editor

A Claude skill that reviews and rewrites a Google Doc against 38 rules for
structure, clarity, data-driven precision, and editorial integrity. It flags gaps
where the author must supply missing data rather than guessing, and runs a bounded
drift-verification pass so the rewrite does not introduce urgency, spin,
attribution distortion, technical oversimplification, or hallucinated data.

## Invocation

`/narrative-style-editor <Google Doc URL>` with an optional mode and `--audience`:

| Mode | Effect |
| :--- | :--- |
| (default) | New doc: clean rewrite + changes table |
| `--show-changes` | New doc with inline ✍️ / 🗑️ / 📊 / ⚠️ markers |
| `--in-place` | **Overwrites** the original (a pre-update revision is pinned for rollback) |
| `--dry-run` | Previews the plan in the conversation; no document is created or changed |

Add `--audience leadership|peers|xfn` to prioritize rules for the reader.

## Layout

- `SKILL.md` — skill definition and workflow.
- `references/PRINCIPLES.md` — the 38 writing rules (numbered 1-38).
- `references/OUTPUT_FORMAT.md` — title, pre-publish zone, changes table, violation summary.
- `references/VERIFICATION.md` — the bounded drift-verification protocol.
- `references/EXAMPLE.md` — a worked end-to-end example.
- `scripts/` — deterministic helpers (Python 3.9+, stdlib only): output assembly,
  acronym scan, URL validation. See `scripts/README.md`.
- `.claude/commands/narrative-style-editor.md` — the slash-command wrapper.

## Development

See `CHANGELOG.md` for the running history and `REMEDIATION_PLAN.md` for the
roadmap derived from the architecture review.