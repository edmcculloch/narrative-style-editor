---
name: narrative-style-editor
description: >-
  Review and rewrite pasted text (markdown or plain) against 38 rules for
  structure, clarity, data-driven precision, and editorial integrity, flagging gaps
  where the author must supply missing data rather than guessing. Use when the user
  pastes text and asks to review, improve, rewrite, or tighten it (or says "check my
  writing" / "make this clearer"), or when another skill must apply these writing
  standards to a block of text. Preserves any markdown formatting in the input and
  returns everything in one console response; nothing is written to a file or an
  external document. Not for general prose polish (use write-it-well), UX copy tone
  (use tone-check), or content/strategy changes.
---

# Narrative Style Editor

## Overview

The narrative-style-editor skill rewrites pasted text (markdown or plain) by applying 38 rules for structure, clarity, data-driven precision, and editorial integrity. It flags gaps where the author must provide missing information to prevent data hallucination.

It returns the rewrite in one console response and never modifies a file or external document; the user copies the clean rewrite out of the response. If the input contains markdown, the rewrite preserves that formatting.

This skill differs from write-it-well, which applies passive Zinsser prose principles. It adds data-backed precision, document durability, AI-tell vocabulary detection, and editorial integrity guardrails beyond general prose cleanup. These guardrails prevent urgency injection, attribution distortion, technical oversimplification, spin, and hallucinated data.

## When to Use

- User pastes text and asks to review, improve, rewrite, or tighten it.
- User requests to "check my writing" or "make this clearer".
- Another skill must apply these writing standards to a block of text.
- The text is intended for leadership or cross-functional audiences.

## When NOT to Use

- General writing advice.
- Voice or style matching.
- User Experience (UX) copy tone analysis: use tone-check using Meta's 7-tone framework.
- Source code, configuration, or other non-prose text.
- Substantive content changes, including strategy or recommendations. This skill preserves author intent and does not rewrite arguments.

## Quick Reference

Paste the text to review after the command.

| Command | What happens | Emojis in body? |
| :--- | :--- | :--- |
| `/narrative-style-editor` | Console response: clean rewrite + changes table + violation summary + verification checklist | No, except ⚠️ gap markers |
| `/narrative-style-editor --show-changes` | Same, plus inline emoji markers at every change site | Yes |
| `/narrative-style-editor --dry-run` | Analysis only: changes table, violation summary, gap list, verification result — no rewrite block | N/A |

Add `--audience <type>` (`leadership` | `peers` | `xfn`, case-insensitive) to any mode to prioritize rules for the reader. The per-audience priority preset lives in `references/AUDIENCE.md`; read it only when an audience flag is passed. Priority changes severity only; no rules are skipped.

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

**Input**: The user pastes the text to review (markdown or plain) plus optional mode and audience flags.

Flags are non-interactive. If no mode flag is provided, return a clean rewrite with the full review in one console response. If no audience flag is provided, apply all rules with equal priority. The skill never writes to a file or external document; it returns its output in the conversation.

## Process

1. Take the pasted text as the original.

    - Use the text the user pasted (or the text another skill handed off) as the document under review. No file or URL is read.
    - If the input is markdown, note its structure — headings, lists, emphasis, links, code blocks, tables — so the rewrite preserves it.
    - If no text was provided, ask the user to paste it; do not proceed on an empty input.

2. Read `references/PRINCIPLES.md`.

    - Identify the 38 writing rules.
    - Apply every applicable rule.
    - If an audience flag is provided, read `references/AUDIENCE.md` and apply its preset to assign priority in the change log.
    - Audience priority changes severity only. It does not skip rules.
    - For Rule 25 (acronyms), run `python3 scripts/scan_acronyms.py` over the original to enumerate candidates; the script finds them and you decide define, expand, or leave each.
    - For Rule 30 (false profundity), run `python3 scripts/scan_profundity.py` over the original and again over your rewritten body before producing output; it surfaces manufactured-contrast kickers, sweeping generalizations, and "not X, but Y" reveals as candidates, and you decide cut, rewrite, or keep each. Candidates are suggestions, not verdicts.

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

    **Preserve markdown formatting**:

    If the input contains markdown, keep it intact in the rewrite — headings stay headings, lists stay lists, and emphasis, links, code, and tables are preserved. Do not flatten markdown to plain text, and do not add markdown the original did not use.

    **Default mode**:

    Use no inline emoji markers except ⚠️ gap markers. The rewrite is clean. Record changes only in the "Changes Made" table in the console output.

4. Flag gaps when information is missing.

    Do not hallucinate or guess.

    Use these markers:

    - `[⚠️ NEEDS: what is needed]` for missing data, numbers, owners, sources, decisions, or other required specifics.
    - `[⚠️ NEEDS: absolute date]` for relative time references.
    - `[⚠️ NEEDS: acronym definition]` for undefined acronyms that cannot be safely expanded from the document.
    - `[⚠️ NEEDS: attribution]` for unclear ownership, source, decision-maker, or team attribution.

5. Perform bounded iterative verification to prevent drift.

    After the rewrite is complete, run the mandatory drift-verification pass before producing output. Read `references/VERIFICATION.md` and follow it exactly. In summary:

    - A read-only, zero-trust verification subagent compares the rewrite against the original and audits it against the 15 drift-prone rules, the `Data`-row source-trace check, and the changes-table citation check.
    - The subagent must return a mandatory evidence checklist before any verdict; an unsupported `No drift detected.` is rejected and the pass is re-run.
    - Run a bounded fix-cycle loop: at most 3 correction cycles, with a final verification pass after the last fix. Log each fix as `Drift`; log anything still unresolved after the loop as `Unresolved Drift`.
    - Include the final pass's evidence checklist in the console output (see Output and `references/OUTPUT_FORMAT.md`).
    - If spawning a verification subagent is unavailable in the host, run the same checklist as an inline self-review pass instead, or stop and notify the user. Do not skip verification.

6. Compile a change log in document order.

    If `--audience` was specified, add a Priority column using the preset in `references/AUDIENCE.md`. Omit the Priority column if `--audience` is not used.

    Include all applicable change types:

    - `Rewritten`
    - `Removed`
    - `Data`
    - `Gap`
    - `Drift`
    - `Unresolved Drift`

    Each row's `Original` cell must be a verbatim substring of the source, every `Reasoning` must cite a real rule (1-38), and a `Data` value must trace to a span in the original. The changes table is an edit log, not a claim-provenance log. See `references/OUTPUT_FORMAT.md`.

## Output

Before producing the response, open `references/OUTPUT_FORMAT.md` and follow it for the console-response layout, the changes-table columns, and the violation-summary format. Those formats live there as the single source of truth; this file does not restate them. The change-log row types are listed in Process step 6.

Assemble the deterministic parts with `python3 scripts/render_output.py`: given your change records as JSON, it computes the violation-summary counts, orders and de-dupes the changes-table rows and numbers them, assigns audience priority, and emits the markdown changes table. You supply judgment and prose; the script supplies the facts so they always reconcile.

### Default mode: clean rewrite

Return one console response, in this order (see `references/OUTPUT_FORMAT.md`):

1. The clean rewrite as a copyable markdown block (⚠️ gap markers only; markdown formatting preserved).
2. The "Changes Made" markdown table from `render_output.py`.
3. The violation summary.
4. The final verification pass's evidence checklist.

### `--show-changes` mode: rewrite with inline markers

Same four parts as Default, but the rewrite block carries inline emoji markers at every change site:

- ✍️ for rewritten text.
- 🗑️ for removed text.
- 📊 for data or specifics added or corrected from information already present in the original.
- ⚠️ for author-input gaps.

### `--dry-run` mode: analysis only

Do not include a rewrite block. Output in the conversation, per `references/OUTPUT_FORMAT.md`:

- Changes table.
- Violation summary.
- Gap list.
- Drift verification result, including the evidence checklist.

## Changes table and violation summary

The changes-table columns (with and without `--audience`) and the violation-summary format are specified once in `references/OUTPUT_FORMAT.md`. Emit them exactly as defined there.

## Bundled scripts

Deterministic helpers live in `scripts/` (Python 3.9+, standard library only). Code computes facts; the model composes narrative. See `scripts/README.md`.

- `scripts/scan_acronyms.py` — enumerate acronym candidates for Rule 25 (Process step 2).
- `scripts/scan_profundity.py` — surface false-profundity / manufactured-contrast candidates for Rule 30 (Process step 2).
- `scripts/render_output.py` — assemble the violation-summary counts, changes-table ordering and IDs, audience priority, and the markdown changes table (Output).

For a worked end-to-end illustration, see `references/EXAMPLE.md`.
