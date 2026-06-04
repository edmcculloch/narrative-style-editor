---
name: narrative-style-editor
description: >-
  Review and rewrite a Google Doc against 38 rules for structure, clarity,
  data-driven precision, and editorial integrity, flagging gaps where the author
  must supply missing data rather than guessing. Use ONLY when the user shares a
  Google Doc URL and asks to review, improve, rewrite, or tighten it (or says
  "check my writing" / "make this clearer" about that doc), or when another skill
  must apply these writing standards to a Google Doc before publishing. Operates on
  a Google Doc, not free text. --in-place OVERWRITES the original (a revision is
  pinned for rollback); other modes create a new doc. Not for free-text prose (use
  write-it-well), UX copy tone (use tone-check), or content/strategy changes.
---

# Narrative Style Editor

## Overview

The narrative-style-editor skill rewrites Google Docs by applying 38 rules for structure, clarity, data-driven precision, and editorial integrity. It flags gaps where the author must provide missing information to prevent data hallucination.

It creates a new document for the rewritten content. It does not modify the original unless the user passes `--in-place`, which overwrites the original document (a pre-update revision ID is pinned for rollback).

This skill differs from write-it-well, which applies passive Zinsser prose principles. It adds data-backed precision, document durability, AI-tell vocabulary detection, and editorial integrity guardrails beyond general prose cleanup. These guardrails prevent urgency injection, attribution distortion, technical oversimplification, spin, and hallucinated data.

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
| `/narrative-style-editor <URL>` | Creates a new doc with a clean rewrite and changes table | No, except ⚠️ gap markers | No |
| `/narrative-style-editor --show-changes <URL>` | Creates a new doc with inline emoji markers and changes table | Yes | No |
| `/narrative-style-editor --in-place <URL>` | Overwrites the original doc with clean text and gap markers | No, except ⚠️ gap markers | Yes |
| `/narrative-style-editor --dry-run <URL>` | Previews the rewrite plan, changes table, and violation summary in conversation | N/A | No |

Add `--audience <type>` to any mode to prioritize rules for the reader. Matching is case-insensitive.

| Audience | P0 Rules |
| :--- | :--- |
| leadership | 1-3: TL;DR, ask, so-what; 5: baselines; 7: recommendation; 25-26: acronyms and jargon |
| peers | 16-19: precision and data; 6: trade-offs |
| xfn | 1-3: TL;DR, ask, so-what; 7: recommendation; 8: toy examples; 25-26: acronyms and jargon |

Rules listed for the audience are P0; all other applicable rules are P1. Audience priority changes severity only; no rules are skipped.

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

    - Validate the URL and extract the document ID with `python3 scripts/parse_doc_url.py "<URL>"` before any `gdocs` call.
    - Use `gdocs docs get` or `gdocs docs export`.
    - If the Google Docs Model Context Protocol (MCP) is unavailable, stop and notify the user:

      `Google Doc MCP is not available. Cannot read the document. To apply writing rules to plain text, read references/PRINCIPLES.md directly.`

    - Do not proceed with a partial workflow.

2. Read `references/PRINCIPLES.md`.

    - Identify the 38 writing rules.
    - Apply every applicable rule.
    - If an audience flag is provided, use the audience table to assign priority in the change log.
    - Audience priority changes severity only. It does not skip rules.
    - For Rule 25 (acronyms), run `python3 scripts/scan_acronyms.py` over the original to enumerate candidates; the script finds them and you decide define, expand, or leave each.

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

    After the rewrite is complete, run the mandatory drift-verification pass before producing output. Read `references/VERIFICATION.md` and follow it exactly. In summary:

    - A read-only, zero-trust verification subagent compares the rewrite against the original and audits it against the 14 drift-prone rules, the `Data`-row source-trace check, and the changes-table citation check.
    - The subagent must return a mandatory evidence checklist before any verdict; an unsupported `No drift detected.` is rejected and the pass is re-run.
    - Run a bounded fix-cycle loop: at most 3 correction cycles, with a final verification pass after the last fix. Log each fix as `Drift`; log anything still unresolved after the loop as `Unresolved Drift`.
    - Persist the final pass's evidence checklist into the pre-publish zone (see Output and `references/OUTPUT_FORMAT.md`).
    - If spawning a verification subagent is unavailable in the host, run the same checklist as an inline self-review pass instead, or stop and notify the user. Do not skip verification.

6. Compile a change log in document order.

    If `--audience` was specified, add a Priority column using the audience preset. Omit the Priority column if `--audience` is not used.

    Include all applicable change types:

    - `Rewritten`
    - `Removed`
    - `Data`
    - `Gap`
    - `Drift`
    - `Unresolved Drift`

    Each row's `Original` cell must be a verbatim substring of the source, every `Reasoning` must cite a real rule (1-38), and a `Data` value must trace to a span in the original. The changes table is an edit log, not a claim-provenance log. See `references/OUTPUT_FORMAT.md`.

## Output

Before creating or replacing any document, open `references/OUTPUT_FORMAT.md` and follow it for the document title, the pre-publish banner zone, the changes-table columns, and the violation-summary format. Those formats live there as the single source of truth; this file does not restate them. The change-log row types are listed in Process step 6.

Assemble the deterministic parts with `python3 scripts/render_output.py`: given your change records as JSON, it computes the violation-summary counts, orders and de-dupes the changes-table rows and numbers them, assigns audience priority, formats the title timestamp in the author's timezone, and emits the pre-publish banner and changes-table HTML. You supply judgment and prose; the script supplies the facts so they always reconcile.

### Default mode: new document, clean rewrite

Create a new Google Doc titled per `references/OUTPUT_FORMAT.md`. Include:

- Clean rewrite.
- ⚠️ gap markers.
- "Changes Made" table in the pre-publish zone at the top with yellow banners.
- Violation summary.
- The final verification pass's evidence checklist, inside the pre-publish zone below the changes table.

Output the link to the new document.

### `--show-changes` mode: new document with inline markers

Follow the Default mode process, but include inline emoji markers at every change site:

- ✍️ for rewritten text.
- 🗑️ for removed text.
- 📊 for data or specifics added or corrected from information already present in the original.
- ⚠️ for author-input gaps.

Output the link to the new document.

### `--in-place` mode

This mode OVERWRITES the author's original document. Proceed only when `--in-place` was explicitly passed; running `--dry-run` first is recommended.

1. Before any write, capture the current document revision so the change is recoverable: record the latest revision identifier (via the `gdocs` revisions API, or `gdocs docs get` revision metadata). Do not proceed until a revision ID has been captured.
2. Replace the document body via `gdocs replace`, keeping the clean rewritten body (⚠️ gaps only) and the "Changes Made" pre-publish zone at the top.
3. Verify the replace succeeded. If `gdocs replace` fails or only partially applies, do NOT report success: surface the failure and the captured revision ID, and restore the document to that revision (Google Docs File > Version history, or a `gdocs` revision-restore call if available).
4. On success, output: confirmation ("Document updated in-place."), the pinned pre-update revision ID and how to roll back to it, the violation summary, total change count, and total gap count.

### `--dry-run` mode

Do not create or modify a document. Output in the conversation, per `references/OUTPUT_FORMAT.md`:

- Changes table.
- Violation summary.
- Gap list.
- Drift verification result, including the evidence checklist.

## Changes table and violation summary

The changes-table columns (with and without `--audience`) and the violation-summary format are specified once in `references/OUTPUT_FORMAT.md`. Emit them exactly as defined there.

## Bundled scripts

Deterministic helpers live in `scripts/` (Python 3.9+, standard library only). Code computes facts; the model composes narrative. See `scripts/README.md`.

- `scripts/parse_doc_url.py` — validate the Google Doc URL and extract its ID (Process step 1).
- `scripts/scan_acronyms.py` — enumerate acronym candidates for Rule 25 (Process step 2).
- `scripts/render_output.py` — assemble the violation-summary counts, changes-table ordering and IDs, audience priority, title timestamp, and pre-publish HTML (Output).

For a worked end-to-end illustration, see `references/EXAMPLE.md`.
