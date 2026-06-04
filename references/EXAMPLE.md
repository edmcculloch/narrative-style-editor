# Worked Example

A minimal end-to-end illustration of one paragraph reviewed in default mode. It is
illustrative, not a rule; follow `SKILL.md` and the other references for the
authoritative process. The violation summary below matches what
`scripts/render_output.py` computes from these four change records.

## Original (excerpt)

> Background
>
> Our innovative dashboard saw great adoption last quarter, and many teams now rely on it.

## Clean rewrite (body)

> Why the Dashboard Matters Now
>
> Our dashboard reached `[⚠️ NEEDS: adoption number]` active teams in Q1 2026, up from `[⚠️ NEEDS: prior-quarter number]`.

What changed: "Background" became an action-oriented header (Rule 28); "innovative"
(peacock, Rule 18) was removed; "great adoption" / "many teams" (weasel, Rule 17)
were flagged rather than invented (Rules 16-17); "last quarter" became an absolute
reference (Rule 21).

## Changes table (excerpt, default mode)

| ID | Type | Location | Original | Revised | Reasoning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Rewritten | §Background, ¶1 | "Background" | "Why the Dashboard Matters Now" | Rule 28 - action-oriented header |
| 2 | Removed | §Background, ¶2 | "innovative" | "" | Rule 18 - peacock word |
| 3 | Gap | §Background, ¶2 | "great adoption" | "[⚠️ NEEDS: adoption number]" | Rule 17 - weasel words |
| 4 | Gap | §Background, ¶2 | "last quarter" | "Q1 2026" | Rule 21 - absolute date |

## Violation summary (excerpt)

```text
Rules: 6 of 38 applicable.
Violations fixed: 2.
Gaps flagged: 2.
Verification: 0 drift violations caught and fixed. 0 unresolved drift violations remain.
Top categories: Precision and Data (2), Durability and Context (1), Language and Terminology (1).
```
