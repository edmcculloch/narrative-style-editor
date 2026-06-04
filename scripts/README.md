# Bundled scripts

Deterministic helpers for the narrative-style-editor skill. The principle: code
computes facts; the model only composes narrative from facts it is handed. Run
them from the repository root.

**Requirements:** Python 3.9+ (standard library only; no third-party packages).

## `render_output.py`

Assembles the deterministic output so the numbers always reconcile: violation-summary
counts (R2), changes-table ordering / de-duplication / sequential IDs (R6), the
title timestamp in the author's timezone (R7), the audience → P0/P1 priority from
the fixed preset (R19), and the pre-publish banner + changes-table HTML with the
canonical colour and column widths (R18).

The model supplies the change records (its judgment) and the per-row prose; the
script supplies the facts. Records must be emitted in document order (or each carry
a numeric `order` field).

```
python3 scripts/render_output.py --in spec.json
cat spec.json | python3 scripts/render_output.py
```

Input (JSON): `original_title`, `author_timezone` (IANA name, optional → UTC),
`now` (ISO instant, optional → current time), `audience`
(`leadership` | `peers` | `xfn` | null), `applicable_rule_count` (X, model
judgment), and `records[]`. Each record:
`{type, section, paragraph, original, revised, rule, reasoning [, order]}`, where
`type` is one of Rewritten, Removed, Data, Gap, Drift, Unresolved Drift.

Output (JSON): `title`, `violation_summary`, `pre_publish_html`, `rows[]`.

## `scan_acronyms.py`

The deterministic half of Rule 25 (R20): find acronym-like tokens and their first
occurrence. The model then decides define / expand / leave per candidate.

```
python3 scripts/scan_acronyms.py --in original.txt
```

## `parse_doc_url.py`

Validate a Google Docs URL and extract the document ID before any `gdocs` call (R28).

```
python3 scripts/parse_doc_url.py "https://docs.google.com/document/d/<id>/edit"
```
