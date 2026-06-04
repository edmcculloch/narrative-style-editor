---
name: write-well
description: >-
  Review and rewrite a Google Doc by applying 38 rules for structure, clarity,
  data-driven precision, and editorial integrity, flagging gaps where the author
  must supply missing data instead of guessing. Use when the user shares a Google
  Doc URL and asks to review, improve, rewrite, tighten, "check my writing", or
  "make this clearer", especially for leadership or cross-functional audiences.
  Supports --show-changes, --in-place, --dry-run, and --audience modes. Not for
  general writing advice, voice or style matching, UX copy tone, non-Google-Doc
  text, or substantive content or strategy changes.
---

# Write Well

## Overview

Write-well rewrites Google Docs by applying 38 rules for structure, clarity, data-driven precision, and editorial integrity. It flags gaps where the author must provide missing information to prevent data hallucination.

Write-well creates a new document for rewritten content. It does not modify the original document unless the user specifies `--in-place`.

This skill differs from write-it-well, which applies passive Zinsser prose principles. Write-well adds data-backed precision, document durability, AI-tell vocabulary detection, and editorial integrity guardrails. These guardrails prevent urgency injection, attribution distortion, technical oversimplification, spin, and hallucinated data.

## When to Use

- User asks to review, improve, or rewrite a Google Doc.
- User requests to "check my writing", "make this clearer", or "review my doc".
- Another skill must apply writing standards before publishing.
- Document is intended for leadership or cross-functional audiences.

## When NOT to Use

- General writing advice.
- Voice or style matching.
- User Experience (UX) copy tone analysis: use tone-check using Meta's 7-tone framework.
- Non-Google-Doc content, including plain text or code: read `references/PRINCIPLES.md` directly instead of running this workflow.
- Substantive content changes, including strategy or recommendations. This skill preserves author intent and does not rewrite arguments.

## Quick Reference

| Command | What happens | Emojis in body? | Edits original? |
| :--- | :--- | :--- | :--- |
| `/write-well <URL>` | Creates a new doc with a clean rewrite and changes table | No, except ⚠️ gap markers | No |
| `/write-well --show-changes <URL>` | Creates a new doc with inline emoji markers and changes table | Yes | No |
| `/write-well --in-place <URL>` | Rewrites the original doc with clean text and gap markers | No, except ⚠️ gap markers | Yes |
| `/write-well --dry-run <URL>` | Previews the rewrite plan, changes table, and violation summary in conversation | N/A | No |

Add `--audience <type>` to any mode to prioritize rules for the reader.

| Audience | P0 Rules |
| :--- | :--- |
| Leadership | 1-3: TL;DR, ask, so-what; 5: baselines; 7: recommendation; 25-26: acronyms and jargon |
| Peers | 16-19: precision and data; 6: trade-offs |
| xfn | 1-3: TL;DR, ask, so-what; 7: recommendation; 8: toy examples; 25-26: acronyms and jargon |

"Relaxed" means the rule is applied, but violations are flagged as P2 in the changes table instead of P0 or P1. No rules are skipped.

## Common Mistakes

| Mistake | Why it matters |
| :--- | :--- |
| Adding urgency not in the original | Rule 34: "not started" does not mean "at risk" |
| Paraphrasing away attribution | Rule 35: "discussed with team" does not mean "no commitment" |
| Simplifying technical terms | Rule 36: "risk evaluation" does not mean "could break" |
| Positive-spinning neutral facts | Rule 37: "not started" does not mean "on track" |
| Inventing next steps | Rule 38: "alignment in progress" does not mean "proposing RACI" |
| Guessing numbers, dates, or sources | Flag with `[⚠️ NEEDS: what]` instead |

## Workflow

**Input**: The user provides a Google Doc Uniform Resource Locator (URL) and optional mode and audience flags.

Flags are non-interactive. If no mode flag is provided, create a new document with a clean rewrite. If no audience flag is provided, apply all rules with equal priority. Never modify the original document unless `--in-place` is explicitly passed.

## Process

1. Read the original document.

    - Use `gdocs docs get` or `gdocs docs export`.
    - If the Google Docs Model Context Protocol (MCP) is unavailable, stop and notify the user:

      `Google Doc MCP is not available. Cannot read the document. To apply writing rules to plain text, read references/PRINCIPLES.md directly.`

    - Do not proceed with a partial workflow.

2. Read `references/PRINCIPLES.md`.

    - Identify the 38 writing rules.
    - Apply every applicable rule.
    - If an audience flag is provided, use the audience table to assign priority in the change log.
    - Audience priority changes severity only. It does not skip rules.

3. Rewrite the document.

    - Preserve author intent, voice, and substantive arguments.
    - Fix structure, clarity, precision, and conciseness.
    - Do not summarize or shorten sections unless they are redundant.
    - Do not add content the author did not include.
    - Keep the original text if a change might alter nuance.
    - Do not invent data, dates, names, sources, owners, decisions, risks, commitments, or next steps.
    - Use absolute dates where dates are required.
    - Define acronyms on first use.
    - Preserve attribution exactly unless the original attribution is ambiguous, in which case flag the ambiguity as a gap.

    **`--show-changes` only**:

    Insert inline emoji markers at every change site:

    - ✍️ text rewritten for clarity, structure, or precision.
    - 🗑️ text removed for filler, redundancy, or AI-tell vocabulary.
    - 📊 data or specifics added or corrected from information already present in the original.

    **All modes**:

    Insert ⚠️ gap markers where author input is needed. These markers remain because they require author action.

    **Default and `--in-place` modes**:

    Use no inline emoji markers except ⚠️ gap markers. The rewrite is clean. Document changes only in the "Changes Made" table in the pre-publish zone.

4. Flag gaps when information is missing.

    Do not hallucinate or guess.

    Use these markers:

    - `[⚠️ NEEDS: what is needed]` for missing data, numbers, owners, sources, decisions, or other required specifics.
    - `[⚠️ NEEDS: absolute date]` for relative time references.
    - `[⚠️ NEEDS: acronym definition]` for undefined acronyms that cannot be safely expanded from the document.
    - `[⚠️ NEEDS: attribution]` for unclear ownership, source, decision-maker, or team attribution.

5. Perform bounded iterative verification to prevent drift.

    After the rewrite is complete, run a mandatory verification pass using a read-only verification subagent. The subagent checks whether the rewrite introduced drift against the original document. The subagent does not rewrite text.

    Initialize:

    - `max_fix_cycles = 3`
    - `fix_cycle = 0`
    - `drift_detected = true`

    While `drift_detected == true`:

    1. Spawn a read-only verification subagent.

    2. Assign the verifier role.

        The subagent is a zero-trust drift auditor.

        - Assume drift may exist.
        - Identify every real drift violation introduced by the rewrite.
        - Do not assume the rewrite is correct.
        - Do not invent violations.
        - Do not reward over-reporting.
        - A finding is valid only if it is supported by evidence from the original and rewritten text.

    3. Provide subagent input.

        - Original document text.
        - Current rewritten document text.
        - Current change log.
        - The 12 drift-prone rules:
            - 17: Weasel words.
            - 18: Peacock words.
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

    4. Give the subagent task.

        - Compare the current rewrite against the original document paragraph by paragraph.
        - Evaluate the rewrite against all 12 drift-prone rules.
        - Identify only drift introduced or amplified by the rewrite.
        - Do not flag language that was already present in the original unless the rewrite worsened it.
        - Do not flag edits that bring the text into compliance with a drift-prone rule.
        - For each potential violation, verify that the issue is present in the rewrite and either absent from the original or materially worsened by the rewrite.

        Compliance examples:

        - Changing a label header to an action-oriented header is compliance, not drift.
        - Adding an acronym definition is compliance, not drift.
        - Removing AI-tell vocabulary is compliance, not drift.
        - Replacing a relative time reference with an absolute date already available in the original is compliance, not drift.

        Drift examples:

        - Introducing a new undefined acronym is drift.
        - Introducing a new label header that was not in the original is drift.
        - Converting "not started" into "at risk" is drift.
        - Converting "discussed with team" into "team committed" is drift.
        - Converting a technical term into a less precise simplification is drift.
        - Adding a proposal, owner, date, risk, dependency, or next step not present in the original is drift.

    5. Require a mandatory evidence checklist.

        The subagent must produce a 12-row checklist before returning any final result.

        Each row must include:

        - Rule number.
        - Rule name.
        - Status: `Pass`, `Fail`, or `Existing issue - not drift`.
        - Rewrite evidence:
            - For `Fail`, provide the exact quote from the rewrite that violates the rule.
            - For `Pass`, provide either a representative quote when applicable or state `No violating instance found in reviewed scope`.
            - For absence-based rules, a pass may be justified by reviewed scope rather than a quote.
        - Original comparison:
            - State whether the issue was absent from the original, present in the original, or worsened by the rewrite.
        - Justification:
            - Explain why the evidence is or is not drift.

    6. Require subagent output.

        The subagent must first provide the mandatory 12-row evidence checklist.

        Then the subagent must provide one of the following:

        - If no drift violations exist, return exactly:

          `No drift detected.`

        - If drift violations exist, return a structured list:

          | Field | Required content |
          | :--- | :--- |
          | Location | `§[Section], ¶[N]` |
          | Original | Exact relevant original text |
          | Rewrite introduced | Exact problematic phrase from the rewrite |
          | Rule violated | `[rule number] - [explanation]` |
          | Why this is drift | Brief explanation of what changed relative to the original |

    7. Validate the verifier output.

        Treat the verifier response as invalid if any of the following are true:

        - It returns `No drift detected.` without the mandatory 12-row evidence checklist.
        - It reports violations without comparing the original and rewrite.
        - It reports a violation without quoting the problematic rewrite text.
        - It reports a violation but does not explain why the issue is drift rather than a pre-existing issue.
        - It rewrites text instead of auditing.

        If the verifier output is invalid or incomplete:

        - Reject the verification result.
        - Run the verification subagent again with the same inputs.
        - Do not proceed based on an unsupported `No drift detected.` signal.

    8. Take main-agent action.

        If the subagent returns a valid 12-row checklist and `No drift detected.`:

        - Set `drift_detected = false`.
        - End verification.

        If valid drift violations exist and `fix_cycle < max_fix_cycles`:

        - Fix only the identified drift violations.
        - Do not make unrelated rewrites.
        - Add each fix to the change log with:
            - Type: `Drift`
            - Location.
            - Rule violated.
            - Before.
            - After.
            - Verification pass number.
        - Increment `fix_cycle` by 1.
        - Run another verification pass.

        If valid drift violations exist and `fix_cycle == max_fix_cycles`:

        - Do not continue rewriting.
        - Add each remaining issue to the change log with:
            - Type: `Unresolved Drift`
            - Location.
            - Rule violated.
            - Remaining issue.
            - Reason unresolved after bounded verification.
        - End verification.

    The limit applies to correction cycles, not verification passes.

    - The process may run one initial verification pass, up to three fix cycles, and a final verification pass after the third fix.
    - Do not stop immediately after the third fix unless the final verification confirms `No drift detected.`
    - If the final verification still finds drift, record the remaining issues as `Unresolved Drift`.

6. Compile a change log in document order.

    If `--audience` was specified, add a Priority column using the audience preset. Omit the Priority column if `--audience` is not used.

    Include all applicable change types:

    - `Rewritten`
    - `Removed`
    - `Data`
    - `Gap`
    - `Drift`
    - `Unresolved Drift`

## Output

Follow `references/OUTPUT_FORMAT.md` for formatting details.

### Default mode: new document, clean rewrite

Create a document with the title:

`[Claude] [/write-well]YYYY-MM-DD HH:MM - [Original Title]`

Include:

- Clean rewrite.
- ⚠️ gap markers.
- "Changes Made" table in the pre-publish zone at the top with yellow banners.
- Violation summary.

Output the link to the new document.

### `--show-changes` mode: new document with inline markers

Follow the Default mode process, but include inline emoji markers at every change site:

- ✍️ for rewritten text.
- 🗑️ for removed text.
- 📊 for data or specifics added or corrected from information already present in the original.
- ⚠️ for author-input gaps.

Output the link to the new document.

### `--in-place` mode

Rewrite the original document with ⚠️ gaps only.

Include:

- "Changes Made" pre-publish zone at the top.
- Clean rewritten document body.
- Pinned pre-update revision ID for rollback.
- Total change count.
- Total gap count.
- Drift verification count.

Replace the document via `gdocs replace`.

Output confirmation, the pinned revision ID for rollback, and total change and gap counts.

### `--dry-run` mode

Do not create or modify a document.

Output in the conversation:

- Changes table.
- Violation summary.
- Gap list.
- Drift verification result.

## Changes Table

Use document order.

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

Add a Priority column.

| ID | Priority | Type | Location | Original | Revised | Reasoning |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | P0 | Rewritten | §[Section], ¶[N] | "[text]" | "[rewritten]" | Rule N - why |
| 2 | P1 | Removed | §[Section], ¶[N] | "[text]" | "" | Rule N - why |
| 3 | P1 | Data | §[Section], ¶[N] | "[text]" | "[corrected]" | Rule N - why |
| 4 | P0 | Gap | §[Section], ¶[N] | "[text]" | "[⚠️ NEEDS: what]" | Rule N - author needs [what] |
| 5 | P1 | Drift | §[Section], ¶[N] | "[original]" | "[corrected rewrite]" | Verification caught Rule N violation |
| 6 | P1 | Unresolved Drift | §[Section], ¶[N] | "[original]" | "[remaining issue]" | Rule N - unresolved after bounded verification |

## Violation Summary

Include the violation summary after the changes table.

Use this format:

```text
Rules: X of 38 applicable.
Violations fixed: Y.
Gaps flagged: Z.
Verification: A drift violations caught and fixed. B unresolved drift violations remain.