# Changelog

All notable changes to the `write-well` skill bundle are recorded here.

This is a **running log**: every change is documented as it is made, not only at
release boundaries. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Work that has
not yet been cut into a published version lives under **[Unreleased]**.

## [Unreleased]

### Added
- `REMEDIATION_PLAN.md` — phased plan to remediate the 32 findings (17 major)
  from the v0.1.0 static architecture review, with the decisions required, a
  finding-to-phase map, sequencing/dependencies, and version milestones.

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
