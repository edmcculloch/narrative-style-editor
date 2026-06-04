# Remediation Plan — `write-well` v0.1.0 architecture review

Phased plan to close the **32 issues (17 major) + 3 credits** from the static
architecture review of v0.1.0. Finding IDs (`R1`–`R32`) map to the review
synthesis; `⭐` marks the priority lenses (Determinism, Attribution).

**Boundary:** the review was static. These fixes address design defects; they do
not substitute for a behavioral evaluation (does the skill trigger correctly, are
the rewrites good?), which should run after remediation.

**Working agreement:** every change is logged in `CHANGELOG.md` under
`[Unreleased]` as it lands, and rolled into a version heading at each milestone.

---

## Phase 0 — Decisions needed before some work can start

These are yours to call; they gate later phases.

- **D1 — Skill name vs directory (`R16`/name mismatch).** Frontmatter `name` is
  `write-well`; the directory/repo is `narrative-style-editor`. Options: (a) rename
  the directory to `write-well`; (b) keep the repo name and ensure the skill is
  loaded/registered by its frontmatter `name`; (c) rename the skill to
  `narrative-style-editor` (touches every `/write-well` reference). Recommend (a)
  or (b).
- **D2 — Command file location (`R16`).** Move `commands/write-well.md` to
  `.claude/commands/` (standard, harness-discoverable) or keep it in-bundle and
  document the intent. Recommend moving out.
- **D3 — Deterministic layer (gates Phase 4).** The determinism findings recommend
  code own the fact-computation. Pick the mechanism: (a) add a `scripts/` helper
  the skill calls; (b) push deterministic ops to the Google Docs MCP side; (c) keep
  model-synthesis but add explicit "derive-by-tallying / assert-table-matches-summary"
  guardrails. (a) gives the strongest guarantees; (c) is the lightest. This choice
  also depends on whether the target runtime (Claude Code vs claude.ai sandbox) can
  execute bundled scripts.
- **D4 — Release tagging.** Whether to cut git tags / GitHub releases at each
  milestone (e.g. `v0.1.0` now, `v0.2.0` after Phase 1–2). Offered, not assumed.

---

## Phase 1 — Coherence & routing (low risk, high value, text-only)

Quick spec/text edits. No behavior change beyond consistency. Do `R10` first;
other phases reference rule numbers.

- **`R10` — Rule numbering.** Number `PRINCIPLES.md` rules globally `1–38` (or add a
  global number beside each section-local one); fix the duplicate "3" in Editorial
  Integrity and the Anti-Patterns restart; confirm the total is exactly 38; then
  re-verify every `Rule N` citation in `SKILL.md` (drift list, Common Mistakes,
  audience presets) resolves 1:1. **Foundational — blocks `R1`, `R9`.**
- **`R12` — Violation-summary format.** Reconcile `SKILL.md` and `OUTPUT_FORMAT.md`
  to one canonical string. Keep the `B unresolved drift` count; define or drop
  `Top categories`. Have `SKILL.md` reference the spec rather than restate it.
- **`R14` — Triggering / routing.** Move routing signals into the frontmatter
  description: the Google-Doc URL as a hard precondition, the discriminator vs
  `write-it-well` (Google-Doc-only + data/integrity scope), the subroutine trigger
  ("when another skill must apply writing standards before publishing"), and the
  `tone-check` redirect. Align `commands/write-well.md`'s description.
- **`R22` — Dry-run output.** Add the gap list + drift-verification result to the
  `OUTPUT_FORMAT.md` dry-run section to match `SKILL.md`.
- **`R23` — "Relaxed"/P2.** Either add explicit P1/P2 tiers to the audience presets
  (and a P2 example row) or remove the dangling "Relaxed"/P2 sentence.
- **`R21` — Title delimiter.** One delimiter for `(Original Title)` in both files;
  add a space after `]` before the date.
- **`R24` — Audience label casing.** Use one casing (`leadership`/`peers`/`xfn`)
  across `SKILL.md` and the command file; state case-insensitivity if applicable.
- **`R25` — Changes-table schema duplication.** Keep one source of truth (the table
  templates in `OUTPUT_FORMAT.md`); reduce `SKILL.md` to a pointer.
- **`R26` — Reference pointer.** Reword the `OUTPUT_FORMAT.md` pointer to an explicit
  "open this before creating/replacing any document" trigger.

_Effort: S. Risk: low. Milestone candidate: **v0.2.0** (with Phase 2)._

---

## Phase 2 — `--in-place` safety (the only destructive mode)

- **`R11` — Rollback actually implemented.** Add ordered steps: (1) before any
  write, call the specific `gdocs` method to fetch + record the current revision ID;
  (2) `gdocs replace`; (3) surface the ID and the exact restore call. Make the
  `OUTPUT_FORMAT.md` in-place output include the revision ID (currently omitted,
  contradicting `SKILL.md`).
- **`R13` — Disclosure + failure handling.** Warn in the frontmatter that
  `--in-place` overwrites the original; strengthen the command wording from "edit"
  to "overwrite/replace"; add a pre-write diff/confirmation; on a failed/partial
  `gdocs replace`, do **not** report success — surface the failure and the revision
  ID and attempt/instruct restore. Define the success criterion before emitting
  "Document updated in-place."

_Effort: M. Risk: medium (touches the destructive path). Milestone: **v0.2.0**._

---

## Phase 3 — Attribution & audit trail (⭐ priority lens)

- **`R1` ⭐ — Data path audited.** Add the data-citation rules (PRINCIPLES "replace
  adjectives with data" / "cite every data claim") to the verifier's drift-prone
  set; require every `Data`/📊 row to cite the exact source span the figure came
  from. Closes the main hallucination vector.
- **`R3` ⭐ — Persist the verifier checklist.** Write the final pass's 12-row
  evidence checklist into the output (appendix or inside the pre-publish zone) for
  default/show-changes/in-place, and into the transcript for dry-run.
- **`R5` ⭐ — Resolvable locations.** Define the `¶N` convention precisely (e.g.
  paragraphs from document start, excluding headers/tables/pre-publish zone) and pin
  `§Section` to the original header (carry both original and revised header text,
  since Rule 28 rewrites headers).
- **`R9` ⭐ — Verify citations.** Require `Original` cells to be exact verbatim
  substrings of the source; constrain `Rule N` to the `1–38` set; add a self-check
  that the cited rule is the one applied at that location. (Depends on `R10`.)
- **`R4` ⭐ — Per-claim vs per-edit.** State that the changes table is an edit log,
  not a claim-provenance log, and that preserved text is not independently verified;
  optionally require `--show-changes` (or a "preserved data claims" note) when data
  integrity must be inspectable.
- **`R29` ⭐ — Dry-run trail (optional).** Offer to write the dry-run report to a
  file/comment so the audit survives the session.

_Effort: M. Risk: low–medium. Milestone candidate: **v0.3.0**._

---

## Phase 4 — Determinism: move fact-computation off the model (⭐ priority lens)

Gated by **D3**. Roughly half the per-output work has a fixed input→output contract
and is model-synthesized only because the bundle ships zero scripts. Whichever
mechanism D3 selects (script / MCP-side / guardrail), the contracts are:

- **`R2` ⭐ — Violation-summary counts.** Derive every count from the structured
  change records: `Y=count(type∈{Rewritten,Removed,Data})`, `Z=count(Gap)`,
  `A=count(Drift)`, `B=count(Unresolved Drift)`, `Top categories = sorted Rule
  frequency`. Assert table-vs-summary agreement before output.
- **`R6` ⭐ — Changes-table mechanics.** Model emits unordered records tagged with a
  parseable location; deterministic step sorts by (section, paragraph), de-dupes,
  assigns IDs `1..N`, selects the column set by `--audience`.
- **`R7` ⭐ — Timestamp.** Compute `YYYY-MM-DD HH:MM` from the real clock; define the
  author-timezone source (MCP field/config, else UTC labeled). Model never invents it.
- **`R8` ⭐ — Verification loop.** Move the fix-cycle counters / `<` vs `==` boundary
  / "one final pass after the last fix" / pass-number stamping into harness control
  flow. Invoke the model per iteration to detect/fix only.
- **`R18` ⭐ — Fixed HTML.** Template the pre-publish banner + changes-table HTML;
  centralize `#FFF9C4` and both `data-col-widths` strings as constants; model fills
  cells, not structural markup.
- **`R19` ⭐ — Priority lookup.** Encode the audience→`P0/P1/P2` preset as a lookup;
  code stamps the Priority cell (keep rule *applicability* as model judgment).
- **`R20` ⭐ — Acronym scan.** Run the acronym regex + first-occurrence dedup in
  code; hand the model the bounded candidate list to decide define/expand/leave.
- **`R17` — Subagent dependency.** Declare the verification-subagent capability and
  guard it like the MCP check; define a single-agent fallback or stop-and-notify.
- **`R27` — gdocs input contract.** Declare that the MCP ingests the specified HTML
  and honors `background-color`/`data-col-widths`, or switch to the structured form
  it consumes.
- **`R28` — URL validation.** Validate the Google Doc URL / extract the doc ID
  before the first `gdocs` call, with a clear error on failure.

_Effort: L (architectural). Risk: medium. Milestone candidate: **v1.0.0**._

---

## Phase 5 — Context economy & file layering

- **`R15` — Extract verification protocol.** Move the ~160-line step 5 (~41% of the
  body) to `references/VERIFICATION.md`; replace it in `SKILL.md` with a ~6-line
  summary + "read this when running the verification pass" pointer; cite rule numbers
  instead of re-listing the drift-prone rules (also closes the rule-list duplication).
  Best done after Phase 3/4 verification edits settle, or extract first then edit in
  the new file.
- **`R16` — Command file.** Per **D2**, relocate to `.claude/commands/` or add an
  orientation pointer in `SKILL.md`.
- **`R31` — Audience preset placement (optional).** Move the preset table to a
  reference loaded only when `--audience` is passed.

_Effort: M. Risk: low. Milestone: fold into **v0.3.0**/**v1.0.0**._

---

## Phase 6 — Polish & docs

- **`R30` — Worked example.** Add one end-to-end example: a real input paragraph →
  cleaned rewrite with a `⚠️` gap marker → the 2–3 filled changes-table rows → the
  rendered violation summary.
- **`R32` — Em-dash rule.** Reframe Rule 32 with its rationale (parenthetical
  em-dashes are the AI tell) and carve out en-dash numeric ranges and `→` arrows.
- **README.** Expand the repo `README.md` to describe the skill, modes, and usage.

_Effort: S. Risk: none._

---

## Preserve (credits — do not regress)

- Strong anti-hallucination guardrails: typed `⚠️ NEEDS` markers, "do not invent…",
  zero-trust verifier with **bounded inputs**.
- Compact 86-word metadata description.
- The verifier's bounded input set (only the loop scaffolding moves to code, `R8`).

---

## Suggested sequencing & milestones

1. **v0.2.0** — Phase 1 (coherence/routing) + Phase 2 (`--in-place` safety).
2. **v0.3.0** — Phase 3 (attribution/audit trail) + Phase 5 (extract verification).
3. **v1.0.0** — Phase 4 (determinism layer, after D3) + Phase 6 (polish).

Dependencies: `R10` → `R1`,`R9`; `D3` → all of Phase 4; `R15` interacts with
Phase 3/4 verification edits. Re-run the static review after each milestone, then a
behavioral evaluation before `v1.0.0`.
