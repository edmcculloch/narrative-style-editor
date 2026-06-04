# Verification Protocol

Run this bounded, iterative drift-verification pass after the rewrite is complete
and before producing output (Process step 5 in `SKILL.md`). It uses a read-only,
zero-trust verification subagent to catch drift the rewrite itself introduced. The
subagent audits; it does not rewrite text.

## Loop control

Initialize:

- `max_fix_cycles = 3`
- `fix_cycle = 0`
- `drift_detected = true`

While `drift_detected == true`, run one verification pass (the steps below), then
take main-agent action (step 7). The limit applies to correction cycles, not
verification passes: run one initial pass, up to three fix cycles, and a final
pass after the third fix. Do not stop immediately after the third fix unless the
final pass confirms `No drift detected.`

## 1. Assign the verifier role

The subagent is a zero-trust drift auditor.

- Assume drift may exist.
- Identify every real drift violation introduced by the rewrite.
- Do not assume the rewrite is correct.
- Do not invent violations.
- Do not reward over-reporting.
- A finding is valid only if it is supported by evidence from the original and rewritten text.

## 2. Provide subagent input

- Original document text.
- Current rewritten document text.
- Current change log (the changes table).
- The 14 drift-prone rules:
    - 16: Replace adjectives with data; no unbacked qualifiers.
    - 17: Weasel words.
    - 18: Peacock words.
    - 19: Cite every data claim.
    - 21: Absolute dates only; no relative time references.
    - 25: Define every acronym on first use.
    - 28: Use action-oriented headers; no label headers such as "Next Steps" or "Background."
    - 29: No filler openers.
    - 31: Avoid AI-tell vocabulary.
    - 34: No urgency injection.
    - 35: Preserve attribution.
    - 36: Do not oversimplify technical meaning.
    - 37: No spin.
    - 38: No invented proposals.

## 3. Give the subagent its task

Drift comparison:

- Compare the current rewrite against the original document paragraph by paragraph.
- Evaluate the rewrite against all 14 drift-prone rules.
- Identify only drift introduced or amplified by the rewrite.
- Do not flag language that was already present in the original unless the rewrite worsened it.
- Do not flag edits that bring the text into compliance with a drift-prone rule.
- For each potential violation, verify that the issue is present in the rewrite and either absent from the original or materially worsened by the rewrite.

Data-source check (applies to every `Data` change-log row):

- Confirm the added or corrected value traces to a specific span in the original document.
- A value that does not trace to the original is fabricated data: report it as drift under Rule 19 (or Rule 16).

Changes-table citation check (applies to every row):

- The `Original` cell must be a verbatim substring of the original document. Flag any that is not.
- The `Reasoning` must cite a real rule number in the range 1-38, and that rule must be the one actually governing the change. Flag invalid or mismatched citations.

Compliance examples (not drift):

- Changing a label header to an action-oriented header.
- Adding an acronym definition.
- Removing AI-tell vocabulary.
- Replacing a relative time reference with an absolute date already available in the original.

Drift examples:

- Introducing a new undefined acronym.
- Introducing a new label header that was not in the original.
- Converting "not started" into "at risk".
- Converting "discussed with team" into "team committed".
- Converting a technical term into a less precise simplification.
- Adding a proposal, owner, date, risk, dependency, or next step not present in the original.
- Entering a number as a `Data` change that is not derivable from the original.

## 4. Require a mandatory evidence checklist

The subagent must produce the checklist before returning any verdict. It has two parts.

Part A: a 14-row table, one row per drift-prone rule, each with:

- Rule number.
- Rule name.
- Status: `Pass`, `Fail`, or `Existing issue - not drift`.
- Rewrite evidence:
    - For `Fail`, the exact quote from the rewrite that violates the rule.
    - For `Pass`, a representative quote when applicable, or `No violating instance found in reviewed scope`.
    - For absence-based rules, a pass may be justified by reviewed scope rather than a quote.
- Original comparison: whether the issue was absent from the original, present in the original, or worsened by the rewrite.
- Justification: why the evidence is or is not drift.

Part B: two check results:

- Data-source check: `Pass` / `Fail`, listing any `Data` row whose value does not trace to the original.
- Citation check: `Pass` / `Fail`, listing any row whose `Original` is not a verbatim substring or whose cited rule is invalid or mismatched.

## 5. Require subagent output

The subagent must first provide the mandatory checklist (Parts A and B). Then one of:

- If no violations exist, return exactly: `No drift detected.`
- If violations exist, a structured list, one entry per violation:

  | Field | Required content |
  | :--- | :--- |
  | Location | `§[Original Section], ¶[N]` |
  | Original | Exact relevant original text |
  | Rewrite introduced | Exact problematic phrase from the rewrite |
  | Rule violated | `[rule number] - [explanation]` |
  | Why this is drift | What changed relative to the original |

## 6. Validate the verifier output

Treat the response as invalid if any of the following are true:

- It returns `No drift detected.` without the mandatory checklist (Parts A and B).
- It reports violations without comparing the original and rewrite.
- It reports a violation without quoting the problematic rewrite text.
- It reports a violation but does not explain why the issue is drift rather than a pre-existing issue.
- It rewrites text instead of auditing.

If the output is invalid or incomplete: reject the result, re-run the subagent with the same inputs, and do not proceed on an unsupported `No drift detected.` signal.

## 7. Take main-agent action

If the subagent returns a valid checklist and `No drift detected.`:

- Set `drift_detected = false`. End verification.

If valid violations exist and `fix_cycle < max_fix_cycles`:

- Fix only the identified violations. Do not make unrelated rewrites.
- Add each fix to the change log with: Type `Drift`, Location, Rule violated, Before, After, and the verification pass number.
- Increment `fix_cycle` by 1. Run another verification pass.

If valid violations exist and `fix_cycle == max_fix_cycles`:

- Do not continue rewriting.
- Add each remaining issue to the change log with: Type `Unresolved Drift`, Location, Rule violated, Remaining issue, and Reason unresolved after bounded verification.
- End verification.

## 8. Persist the evidence

Persist the final verification pass's checklist (Parts A and B) so the drift
conclusion is auditable after the run:

- Default, `--show-changes`, and `--in-place` modes: include it inside the
  pre-publish zone, below the changes table. It is deleted with the rest of the
  zone before publishing.
- `--dry-run` mode: include it in the conversation as part of the drift
  verification result.

The violation summary's `A drift violations caught` and `B unresolved drift
violations remain` counts must match this checklist and the `Drift` /
`Unresolved Drift` rows in the changes table.
