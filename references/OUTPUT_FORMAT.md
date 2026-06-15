# Output Format

This is the single source of truth for the narrative-style-editor output: the
console response, the changes table, and the violation summary. `SKILL.md` points
here rather than restating them.

The skill takes pasted text (markdown or plain) and returns everything in one
console response. Nothing is written to a file or an external document, so there is
no document title, banner, or "delete before publishing" zone — the user copies the
clean rewrite out of the response; the review material below it is for reference.

## Console response

Emit these parts in order, in the conversation:

1. **Clean rewrite** — the rewritten text as a copyable markdown block. If the input
   was markdown, preserve its formatting (headings, lists, emphasis, links, code,
   tables). Only ⚠️ gap markers appear in the body; no other inline markers (except
   in `--show-changes`).
2. **Changes Made table** — the markdown pipe table from `scripts/render_output.py`
   (`changes_table_md`), under a `## Changes Made` heading.
3. **Violation summary** — the exact format under "Violation summary" below.
4. **Verification evidence checklist** — the final drift-verification pass's
   checklist (Parts A and B, per `references/VERIFICATION.md`).

Mode differences:

- **Default** — all four parts; clean rewrite body (⚠️ gap markers only).
- **`--show-changes`** — same four parts, but the rewrite block carries inline
  ✍️ rewritten / 🗑️ removed / 📊 data / ⚠️ gap markers at every change site so the
  author can see where edits were made.
- **`--dry-run`** — omit part 1 (no rewrite block). Emit the changes table, the
  violation summary, the gap list, and the drift-verification result (including the
  evidence checklist).

## Changes table

Use document order. Assign sequential IDs starting at 1. The table is rendered as a
GitHub-style markdown pipe table by `scripts/render_output.py`.

- **Location** uses `§[Original Section], ¶[N]`, where `¶N` counts paragraphs from
  the start of that section in the ORIGINAL text, excluding headings and tables. Pin
  `§Section` to the original heading text; if a header was rewritten (Rule 28), still
  cite the original header so the row stays resolvable. When the input has no
  headings, use `¶N` alone (paragraphs from the start of the input).
- **Original** must be a verbatim substring of the source text. **Reasoning** must
  cite a real rule number in the range 1-38.
- A **Data** row must additionally cite the original span the value is derived from.
  A value that does not trace to the source is fabricated data (drift), not a `Data`
  change.
- The changes table is an edit log, not a claim-provenance log: it records changed,
  added, or removed spans, not every preserved factual claim. Preserved text is not
  independently re-verified; when data integrity must be inspectable, use
  `--show-changes`.

### Without `--audience`

| ID | Type | Location | Original | Revised | Reasoning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Rewritten | §[Section], ¶[N] | "[text]" | "[rewritten]" | Rule N - why |
| 2 | Removed | §[Section], ¶[N] | "[text]" | "" | Rule N - why |
| 3 | Data | §[Section], ¶[N] | "[text]" | "[corrected]" | Rule N - why |
| 4 | Gap | §[Section], ¶[N] | "[text]" | "[⚠️ NEEDS: what]" | Rule N - author needs [what] |
| 5 | Drift | §[Section], ¶[N] | "[original]" | "[corrected rewrite]" | Verification caught Rule N violation |
| 6 | Unresolved Drift | §[Section], ¶[N] | "[original]" | "[remaining issue]" | Rule N - unresolved after bounded verification |

### With `--audience`

Add a Priority column (P0/P1) after ID.

| ID | Priority | Type | Location | Original | Revised | Reasoning |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | P0 | Rewritten | §[Section], ¶[N] | "[text]" | "[rewritten]" | Rule N - why |
| 2 | P1 | Removed | §[Section], ¶[N] | "[text]" | "" | Rule N - why |
| 3 | P1 | Data | §[Section], ¶[N] | "[text]" | "[corrected]" | Rule N - why |
| 4 | P0 | Gap | §[Section], ¶[N] | "[text]" | "[⚠️ NEEDS: what]" | Rule N - author needs [what] |
| 5 | P1 | Drift | §[Section], ¶[N] | "[original]" | "[corrected rewrite]" | Verification caught Rule N violation |
| 6 | P1 | Unresolved Drift | §[Section], ¶[N] | "[original]" | "[remaining issue]" | Rule N - unresolved after bounded verification |

## Violation summary

Emit this exact format as a plain-text paragraph after the changes table, in every mode:

```text
Rules: X of 38 applicable.
Violations fixed: Y.
Gaps flagged: Z.
Verification: A drift violations caught and fixed. B unresolved drift violations remain.
Top categories: [list].
```

Derive every number by tallying the change-log rows (do not estimate):

- `Y` = count of `Rewritten` + `Removed` + `Data` rows.
- `Z` = count of `Gap` rows.
- `A` = count of `Drift` rows.
- `B` = count of `Unresolved Drift` rows.
- `X` = number of the 38 rules judged applicable to this document.
- `Top categories` = the rule categories with the most violations, most first.

The counts must reconcile with the changes table before output. `scripts/render_output.py`
computes them (and the row ordering, IDs, audience priority, and the markdown changes
table) from the change records; use it rather than hand-counting.
