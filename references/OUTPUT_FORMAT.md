# Output Format

## Pre-Publish Zone (default, show-changes, and in-place modes)

Insert a "Changes Made" section at the top of the document, wrapped in yellow pre-publish banners (header + footer) instructing the author to delete everything between the banners before publishing.

- Banners: single-cell `<table>` with `background-color: #FFF9C4`, plain bold text (no headings, no font-size overrides).
- "Changes Made" label: `<p><b>`, not a heading.
- Changes table (without `--audience`):
  `<table data-col-widths="25, 75, 75, 120, 110, 120">` (Google Docs does not auto-size columns; these proportional widths keep # and Type narrow, Original/Revised/Reasoning wide).
- Changes table (with `--audience`):
  `<table data-col-widths="25, 30, 75, 75, 120, 110, 120">`
  - Adds a Priority column (P0/P1/P2) after #.
- Violation summary: Plain text paragraph after the changes table.
  Format: "Rules: X of 38 applicable. Y violations fixed. Z gaps flagged. Verification: N drift violations caught and fixed. Top categories: [list]."

### In-place mode output to user

- Confirmation: "Document updated in-place."
- Violation summary (same format as other modes).

## Default Mode (Clean Rewrite)

1. Create a new Google Doc.
   - Title: `[Claude] [/write-well]YYYY-MM-DD HH:MM - (Original Title)`
   - Timestamp in the author's timezone.
2. Replace content with clean rewrite. No inline emoji change markers. Only gap markers remain in the body (they require author action).
3. Insert pre-publish zone at top (see above).
4. Output the link to the new Google Doc.

## Show-Changes Mode

Same as default, but the rewrite includes inline emoji markers (✍️ 🗑️ 📊) at every change site so the author can audit exactly where edits were made.

1. Create a new Google Doc (same title format as default).
2. Replace content with rewritten version including inline emoji markers.
3. Insert pre-publish zone at top (see above).
4. Output the link to the new Google Doc.

## Dry-Run Mode

No document created or modified. Output in conversation:

1. Changes table (same format as other modes).
2. Violation summary.
