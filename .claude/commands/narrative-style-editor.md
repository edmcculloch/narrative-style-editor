---
description: Review and rewrite a Google Doc, applying 38 rules for structure, clarity, precision, and editorial integrity. Requires a Google Doc URL; for free-text prose use write-it-well, for UX copy tone use tone-check.
---

# /narrative-style-editor

Run the narrative-style-editor skill to review and rewrite a Google Doc.

## Usage

- `/narrative-style-editor <URL>` — new doc with clean rewrite + changes table (default)
- `/narrative-style-editor --show-changes <URL>` — new doc with inline emoji markers + changes table
- `/narrative-style-editor --in-place <URL>` — OVERWRITES the original doc via replace (pre-update revision pinned for rollback)
- `/narrative-style-editor --dry-run <URL>` — preview changes in conversation, no edits
- Add `--audience <type>` to any mode to prioritize rules for the reader: `leadership` | `peers` | `xfn` (default: all rules equal priority)

Applies 38 writing rules for clarity, precision, conciseness, and editorial integrity. Includes a verification pass that catches violations the rewrite itself introduced (anti-drift). Gaps where data or specifics are needed get ⚠️ markers in all modes. Inline emoji change markers only appear in `--show-changes` mode.
