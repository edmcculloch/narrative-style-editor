---
description: Review a Google Doc and produce a rewritten version with improvements, applying 38 writing rules for clarity, precision, conciseness, and editorial integrity.
---

# /write-well

Run the write-well skill to review and rewrite a Google Doc.

## Usage

- `/write-well <URL>` — new doc with clean rewrite + changes table (default)
- `/write-well --show-changes <URL>` — new doc with inline emoji markers + changes table
- `/write-well --in-place <URL>` — edit the original doc (revision pinned for rollback)
- `/write-well --dry-run <URL>` — preview changes in conversation, no edits
- Add `--audience <type>` to any mode to prioritize rules for the reader: `leadership` | `peers` | `xfn` (default: all rules equal priority)

Applies 38 writing rules for clarity, precision, conciseness, and editorial integrity. Includes a verification pass that catches violations the rewrite itself introduced (anti-drift). Gaps where data or specifics are needed get ⚠️ markers in all modes. Inline emoji change markers only appear in `--show-changes` mode.
