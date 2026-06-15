# Changelog

All notable changes to the `write-well` skill bundle are recorded here.

This is a **running log**: every change is documented as it is made, not only at
release boundaries. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Work that has
not yet been cut into a published version lives under **[Unreleased]**.

## [Unreleased]

### Added
- `scripts/scan_profundity.py` — the deterministic half of Rule 30. It flags
  manufactured-contrast kickers (a sweeping generalization followed by a short
  punchy kicker), bare sweeping generalizations, "not X, but Y" / "It's not X.
  It's Y." reveals, and curated dramatic one-liners, with line/column/offset and a
  per-pattern reason. Candidates are suggestions; the model decides cut/rewrite/keep.
  Wired into Process step 2 of `SKILL.md` (run over original and rewrite) and the
  bundled-scripts list. Standard library only, mirrors the `scan_acronyms.py` I/O
  contract (stdin or `--in FILE`; JSON `{count, candidates}`).

### Changed
- Rule 30 (No false profundity) now explicitly covers the **manufactured-contrast
  kicker**: an unverifiable sweeping generalization ("most teams…", "everyone…",
  "anyone can…") used to set up a punchy short-sentence payoff, plus the
  "not X, but Y" reveal. These are common LLM tells; the "most/many/everyone" half
  is also a Rule 17 weasel violation. Added three worked examples.
- Added Rule 30 to the verifier's drift-prone rule set (now 15, was 14) in
  `references/VERIFICATION.md` (list, evaluation step, and Part A row count) and
  `SKILL.md`, so the anti-drift pass catches a false-profundity contrast the
  rewrite itself introduces. No rule renumbering; the 1-38 citation range is
  unchanged (Rule 30 already existed).
- Relocated the audience priority preset table out of the always-loaded `SKILL.md`
  into a new load-on-demand `references/AUDIENCE.md`, read only when `--audience` is
  passed (R31, context economy). `SKILL.md` keeps a one-line pointer and the valid
  audience values; `render_output.py`'s `AUDIENCE_P0` constant stays the operative
  encoding, and the reference notes the two must stay in sync. Closes the last
  deferred review finding from the v0.1.0 architecture review.
- **Converted the skill from Google Docs to portable text-in / text-out.** Input is
  now pasted text (markdown or plain; formatting preserved); output is a single
  console response — clean rewrite block, a markdown changes table, the violation
  summary, and the verification checklist. Removed all Google-Docs/HTML output: the
  pre-publish banner zone, `#FFF9C4` banners, `<table>` / `data-col-widths`, the
  document title + timezone timestamp, and revision-pinning. `SKILL.md`,
  `references/OUTPUT_FORMAT.md`, `references/VERIFICATION.md` (step 8),
  `.claude/commands/narrative-style-editor.md`, `README.md`, and `scripts/README.md`
  updated. No rule renumbering; the 1-38 citation contract is unchanged.
- `scripts/render_output.py` now emits a markdown pipe table (`changes_table_md`)
  instead of pre-publish HTML, and dropped the title/timestamp: removed the
  `original_title` / `author_timezone` / `now` inputs and the `title` /
  `pre_publish_html` outputs. The compute functions (counts, ordering, priority,
  summary) are unchanged.

### Removed
- `scripts/parse_doc_url.py` — Google-Docs-URL validation; no URL is read anymore.
- The `--in-place` mode — it overwrote the Google Doc; the default console rewrite,
  which the user copies out, replaces it.

### Fixed
- `scripts/scan_profundity.py`: added smart-quote (curly apostrophe `’`) support so
  reveals like "It's not X. It's Y." are still caught when a Google Doc uses `’`, and
  tightened the standalone-kicker rule to require a genuine contrast cue (but/yet,
  can't/won't, only/few) instead of any absolute marker — plain factual short sentences
  (e.g. "None failed.") no longer flag, and the remaining standalone flags carry a
  low-confidence, "you decide" reason.

## [1.0.0] - 2026-06-04

Remediation milestone 3: a deterministic scripts layer (Phase 4) and polish
(Phase 6). Closes review findings R2, R6, R7, R17, R18, R19, R20, R27, R28, R30,
and R32, and partially R8. R31 remains deferred.

### Added
- `scripts/` (Python 3.9+, standard library only) — the deterministic layer (D3):
  - `render_output.py` — computes violation-summary counts (R2); orders, de-dupes,
    and numbers changes-table rows (R6); assigns audience P0/P1 priority (R19);
    formats the title timestamp in the author's timezone (R7); and emits the
    pre-publish banner and changes-table HTML with the canonical colour and column
    widths (R18).
  - `scan_acronyms.py` — the deterministic half of Rule 25: find acronym-like
    tokens and their first occurrence; the model decides define/expand/leave (R20).
  - `parse_doc_url.py` — validate the Google Doc URL and extract its ID before any
    `gdocs` call (R28).
  - `scripts/README.md` — dependencies and the input/output contracts.
- `references/EXAMPLE.md` — a worked end-to-end example (R30), wired from `SKILL.md`.

### Changed
- `SKILL.md` now invokes the scripts in the workflow: URL validation in step 1, the
  acronym scan in step 2, and deterministic output assembly in Output. The model
  supplies judgment and prose; code supplies the facts so the summary, IDs,
  ordering, timestamp, and priority are reproducible.
- Rule 32 reframed (R32): it now explains why a parenthetical em-dash is the AI tell
  and explicitly exempts en-dash numeric ranges and `→` arrows, so it no longer
  over-fires on compliant text.
- Expanded `README.md` to describe the skill, modes, layout, and scripts.

### Fixed
- Declared the verification-subagent dependency and added a guard with an inline
  self-review fallback; verification is never skipped (R17).
- Declared the `gdocs` HTML input-contract assumption (HTML, `background-color`,
  `data-col-widths`) in `references/OUTPUT_FORMAT.md` (R27).
- Loop bookkeeping (R8): the fix-cycle counters remain main-agent orchestration, but
  the per-output counts and pass-number reconciliation are now deterministic via
  `render_output.py` and the verification checklist (partial).

### Deferred
- R31 (relocate the audience preset table to a load-on-demand reference) — optional,
  low impact.

## [0.3.0] - 2026-06-04

Remediation milestone 2: attribution and audit trail (Phase 3) and extraction of
the verification protocol (Phase 5). Closes review findings R1, R3, R4, R5, R9,
and R15, and partially R29.

### Added
- `references/VERIFICATION.md` — the bounded drift-verification protocol, extracted
  from `SKILL.md` (R15). `SKILL.md` step 5 is now a short summary plus a pointer,
  shrinking the always-loaded body from ~401 to ~204 lines.

### Changed
- **The `Data` path is now audited** (R1): the verifier's drift-prone set adds
  Rule 16 (replace adjectives with data) and Rule 19 (cite every data claim), for
  14 rules total, and a new Data-source-trace check flags any `Data` value not
  derivable from the original as fabricated data (drift).
- **Resolvable claim locations** (R5): defined the `¶N` convention (paragraphs from
  the section start in the original, excluding headings, tables, and the pre-publish
  zone) and pinned `§Section` to the original heading, so rows stay resolvable after
  header rewrites (Rule 28).
- **Verifiable citations** (R9): `Original` cells must be verbatim substrings of the
  source and `Reasoning` must cite a real rule (1-38); the verifier runs a citation
  check that flags non-verbatim quotes and invalid or mismatched rule numbers.
- **Edit log, not claim log** (R4): documented that the changes table records changed
  spans, not every preserved factual claim, and that preserved text is not
  independently re-verified (use `--show-changes` when data integrity must be
  inspectable).

### Fixed
- **Audit trail persisted** (R3): the final verification pass's evidence checklist is
  now written into the pre-publish zone (below the changes table) for default,
  show-changes, and in-place modes, and into the dry-run output, so the
  "drift caught / unresolved" counts trace to their evidence. This partially
  addresses R29 by putting the checklist in the dry-run result; durable file
  persistence for dry-run remains optional.

### Deferred
- R31 (move the audience preset table to a load-on-demand reference) — optional and
  low impact; the small preset table stays in `SKILL.md` for now.

## [0.2.0] - 2026-06-04

Remediation milestone 1: naming consistency, command relocation, coherence and
spec fixes (Phase 1), and `--in-place` safety (Phase 2). Closes review findings
D1, D2, R10–R14, and R21–R26.

### Changed
- **Renamed the skill to `narrative-style-editor`** (D1, R16): the frontmatter
  `name`, the `/narrative-style-editor` command, the document title, and every
  body reference now match the directory. (`write-it-well` and `tone-check`
  remain as references to sibling skills.)
- **Global rule numbering** (R10): `references/PRINCIPLES.md` now numbers all 38
  rules 1–38 across sections; fixed the duplicate "3" in Editorial Integrity and
  the restart in Anti-Patterns, so every `Rule N` citation in `SKILL.md`
  resolves to exactly one rule.
- **Single source of truth for output formats** (R12, R21, R25, R26): the
  document title, changes-table columns, and violation-summary format now live
  only in `references/OUTPUT_FORMAT.md`; `SKILL.md` points to it with an explicit
  "open this before creating or replacing a document" instruction.
- **Reconciled the violation summary** (R12): one canonical format that keeps
  both the unresolved-drift count and a now-defined `Top categories` field, plus
  explicit count-derivation rules.
- **Routing moved into the description** (R14): the frontmatter now gates on a
  Google Doc URL, names the `write-it-well` / `tone-check` boundaries and the
  subroutine trigger; the command description matches.
- **Audience presets** (R23, R24): lowercased the labels
  (`leadership` / `peers` / `xfn`), made matching case-insensitive, removed the
  dangling "Relaxed" / P2 concept, and stated the P0/P1 rule. The Priority column
  is now P0/P1.

### Fixed
- `--in-place` rollback is now actually specified (R11): capture the pre-update
  revision ID before any write, surface it with rollback instructions, and the
  spec's in-place output now includes it.
- `--in-place` safety (R13): the frontmatter and command warn that the mode
  OVERWRITES the original; added failure handling for a failed or partial
  `gdocs replace` (no false success; restore the captured revision) and a
  recommendation to run `--dry-run` first.
- Dry-run output (R22): the spec now lists all four items (changes table,
  violation summary, gap list, drift verification result).
- Closed an unterminated code fence at the end of `SKILL.md`.

### Moved
- `commands/write-well.md` → `.claude/commands/narrative-style-editor.md`
  (D2, R16): the slash command now lives in the standard location and is no
  longer an orphan inside the bundle.

### Added (docs, since 0.1.0)
- `REMEDIATION_PLAN.md` — phased plan to remediate the 32 v0.1.0 review findings,
  with the required decisions, a finding-to-phase map, and version milestones.

## [0.1.0] - 2026-06-03

Initial draft of the `write-well` skill, assembled from source documents and
published as the first version.

### Added
- `SKILL.md` — skill definition: overview, when / when-not-to-use, four modes
  (default, `--show-changes`, `--in-place`, `--dry-run`), `--audience` presets
  (leadership / peers / xfn), the bounded iterative drift-verification protocol,
  the change-log / changes-table spec, and the violation summary.
- `commands/write-well.md` — slash-command wrapper for `/write-well`.
- `references/PRINCIPLES.md` — the 38 writing rules (structure & purpose,
  sentence-level clarity, precision & data, durability & context, language &
  terminology, anti-patterns, editorial integrity).
- `references/OUTPUT_FORMAT.md` — output spec: pre-publish banner zone,
  changes-table column widths, document-title format, per-mode output steps.
- `.gitignore` — excludes local Claude Code session settings
  (`.claude/settings.local.json`).

### Changed (normalization applied while assembling from the source files)
- Unified the skill identity to `write-well`: added YAML frontmatter
  (`name` + description) to `SKILL.md`; named the command file `write-well.md`.
- Repaired transcription / OCR artifacts so the bundle is internally coherent:
  - Flag syntax restored: `--show-changes`, `--in-place`, `--dry-run`, `--audience`.
  - Markup restored in `OUTPUT_FORMAT.md` (`<table>` tags, `data-col-widths`,
    banner colour `#FFF9C4`).
  - Good/bad example markers `❌` / `✅` and the gap-marker convention
    `[⚠️ NEEDS: …]` restored in `PRINCIPLES.md`.
  - Typos fixed: `xTn` → `xfn`, `TL:DR` → `TL;DR`, `laC` → `IaC`,
    `01 2026` → `Q1 2026`, `PO/P1/P2` → `P0/P1/P2`.
- Deliberately **preserved** (legitimate review targets, not normalized away):
  the per-section rule numbering in `PRINCIPLES.md`, the two differing
  violation-summary formats, and the `commands/` placement.

### Notes
- A static architecture/design review (9 lenses, read-only) was run against this
  version. It found **32 issues (17 major) + 3 credits**. Nothing was executed,
  so this is a design-defect list, not a behavioral verdict. Remediation is
  tracked under **[Unreleased]** and detailed in `REMEDIATION_PLAN.md`.

[Unreleased]: ./CHANGELOG.md
[0.1.0]: ./CHANGELOG.md
