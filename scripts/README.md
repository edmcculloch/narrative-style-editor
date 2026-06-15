# Bundled scripts

Deterministic helpers for the narrative-style-editor skill. The principle: code
computes facts; the model only composes narrative from facts it is handed. Run
them from the repository root.

**Requirements:** Python 3.9+ (standard library only; no third-party packages).

## `render_output.py`

Assembles the deterministic output so the numbers always reconcile: violation-summary
counts (R2), changes-table ordering / de-duplication / sequential IDs (R6), the
audience → P0/P1 priority from the fixed preset (R19), and the "Changes Made" table
rendered as a GitHub-style markdown pipe table.

The model supplies the change records (its judgment) and the per-row prose; the
script supplies the facts. Records must be emitted in document order (or each carry
a numeric `order` field).

```
python3 scripts/render_output.py --in spec.json
cat spec.json | python3 scripts/render_output.py
```

Input (JSON): `audience` (`leadership` | `peers` | `xfn` | null),
`applicable_rule_count` (X, model judgment), and `records[]`. Each record:
`{type, section, paragraph, original, revised, rule, reasoning [, order]}`, where
`type` is one of Rewritten, Removed, Data, Gap, Drift, Unresolved Drift. `section`
is optional — when absent, the row location degrades to `¶N` (or `—`).

Output (JSON): `violation_summary`, `changes_table_md`, `rows[]`.

## `scan_acronyms.py`

The deterministic half of Rule 25 (R20): find acronym-like tokens and their first
occurrence. The model then decides define / expand / leave per candidate.

```
python3 scripts/scan_acronyms.py --in original.txt
cat original.txt | python3 scripts/scan_acronyms.py
```

## `scan_profundity.py`

The deterministic half of Rule 30 (No false profundity): flag candidate sentences —
manufactured-contrast kickers ("Most teams skip that. A firm in your position can't."),
sweeping generalizations, "not X, but Y" reveals, and dramatic one-liners. The model
then decides cut / rewrite / keep per candidate; matches are suggestions, not verdicts.
Run it over both the original and the rewritten body before producing output.

```
python3 scripts/scan_profundity.py --in original.txt
cat original.txt | python3 scripts/scan_profundity.py
```
