---
description: Review and rewrite pasted text (markdown or plain), applying 38 rules for structure, clarity, precision, and editorial integrity. Returns the rewrite in the conversation; for general prose polish use write-it-well, for UX copy tone use tone-check.
---

# /narrative-style-editor

Run the narrative-style-editor skill to review and rewrite pasted text.

## Usage

- `/narrative-style-editor` — paste text; returns a clean rewrite + changes table (default)
- `/narrative-style-editor --show-changes` — same, plus inline emoji markers at every change site
- `/narrative-style-editor --dry-run` — analysis only (changes table, violation summary, gap list, verification); no rewrite block
- Add `--audience <type>` to any mode to prioritize rules for the reader: `leadership` | `peers` | `xfn` (default: all rules equal priority)

Applies 38 writing rules for clarity, precision, conciseness, and editorial integrity. Includes a verification pass that catches violations the rewrite itself introduced (anti-drift). Gaps where data or specifics are needed get ⚠️ markers in all modes. Inline emoji change markers only appear in `--show-changes` mode. If the input is markdown, the rewrite preserves its formatting.
