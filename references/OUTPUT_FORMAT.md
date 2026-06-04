# Output Format

This is the single source of truth for the narrative-style-editor output formats:
the document title, the pre-publish zone, the changes table, and the violation
summary. `SKILL.md` points here rather than restating them.

## Document title

For modes that create a new document, title it:

`[Claude] [/narrative-style-editor] YYYY-MM-DD HH:MM - (Original Title)`

The timestamp is the date and time in the author's timezone.

## Pre-Publish Zone (default, show-changes, and in-place modes)

Insert a "Changes Made" section at the top of the document, wrapped in yellow pre-publish banners (header + footer) instructing the author to delete everything between the banners before publishing.

- Banners: single-cell `<table>` with `background-color: #FFF9C4`, plain bold text (no headings, no font-size overrides).
- "Changes Made" label: `<p><b>`, not a heading.
- Changes table (without `--audience`):
  `<table data-col-widths="25, 75, 75, 120, 110, 120">` (Google Docs does not auto-size columns; these proportional widths keep # and Type narrow, Original/Revised/Reasoning wide).
- Changes table (with `--audience`):
  `<table data-col-widths="25, 30, 75, 75, 120, 110, 120">` (adds a Priority column after #).
- Verification evidence checklist: below the changes table, include the final verification pass's checklist (the per-rule drift rows plus the citation and `Data`-source checks, per `references/VERIFICATION.md`). It lives inside the pre-publish zone so the author can audit the drift conclusion, then delete it with the rest of the zone before publishing.

This output assumes the `gdocs` MCP accepts HTML input and honours `background-color` and `data-col-widths`. If a host's MCP does not, adapt to the structured request form it consumes.

## Changes table

Use document order. Assign sequential IDs starting at 1.

- **Location** uses `§[Original Section], ¶[N]`, where `¶N` counts paragraphs from the start of that section in the ORIGINAL document, excluding headings, tables, and the pre-publish zone. Pin `§Section` to the original heading text; if a header was rewritten (Rule 28), still cite the original header so the row stays resolvable.
- **Original** must be a verbatim substring of the source document. **Reasoning** must cite a real rule number in the range 1-38.
- A **Data** row must additionally cite the original span the value is derived from. A value that does not trace to the source is fabricated data (drift), not a `Data` change.
- The changes table is an edit log, not a claim-provenance log: it records changed, added, or removed spans, not every preserved factual claim. Preserved text is not independently re-verified; when data integrity must be inspectable, use `--show-changes`.

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

The counts must reconcile with the changes table before output. `scripts/render_output.py` computes them (and the title, row ordering, IDs, audience priority, and pre-publish HTML) from the change records; use it rather than hand-counting.

## Per-mode output

### Default mode (clean rewrite)
1. Create a new Google Doc with the title above.
2. Replace content with the clean rewrite. No inline emoji change markers; only ⚠️ gap markers remain in the body (they require author action).
3. Insert the pre-publish zone at the top.
4. Output the link to the new Google Doc.

### Show-changes mode
Same as default, but the body includes inline emoji markers (✍️ rewritten, 🗑️ removed, 📊 data, ⚠️ gap) at every change site so the author can audit where edits were made.

### In-place mode (OVERWRITES the original)
1. Capture the pre-update revision ID before any write.
2. Replace the document via `gdocs replace`; keep the clean body plus the pre-publish zone.
3. On a failed or partial replace, do not report success; surface the failure and restore the captured revision.
4. Output to the user: confirmation ("Document updated in-place."), the pinned pre-update revision ID and how to roll back to it, the violation summary, and total change and gap counts.

### Dry-run mode
No document is created or modified. Output in the conversation:
1. Changes table.
2. Violation summary.
3. Gap list.
4. Drift verification result.
