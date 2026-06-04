#!/usr/bin/env python3
"""Deterministic output assembly for the narrative-style-editor skill.

The model supplies judgment: which of the 38 rules apply, the rewritten prose, and
the per-row Original / Revised / Reasoning text. This script owns the deterministic
facts so they are reproducible and always reconcile with each other:

- violation-summary counts (R2)
- changes-table ordering, de-duplication, and sequential IDs (R6)
- the document-title timestamp in the author's timezone (R7)
- the pre-publish banner + changes-table HTML, with the canonical colour and
  column widths (R18)
- the audience -> P0/P1 priority assignment from the fixed preset (R19)

It performs no model reasoning. Standard library only (Python 3.9+).

Input (stdin, or --in FILE): a JSON object
    {
      "original_title": "Q3 Planning",
      "author_timezone": "America/New_York",   # IANA name; omit/null -> UTC
      "now": "2026-06-04T15:04:00+00:00",        # optional ISO instant; omit -> now()
      "audience": "leadership",                   # leadership|peers|xfn or null
      "applicable_rule_count": 21,                # X: rules judged applicable (model)
      "records": [
        {"type": "Rewritten", "section": "Overview", "paragraph": 2,
         "original": "Conversion improved.", "revised": "Conversion rose 2.1% to 3.4%.",
         "rule": 16, "reasoning": "Rule 16 - replace adjective with data"}
      ]
    }

Output (stdout): a JSON object
    {"title": ..., "violation_summary": ..., "pre_publish_html": ..., "rows": [...]}

Exit codes: 0 ok; 2 invalid input.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - py<3.9
    ZoneInfo = None

# --- Fixed constants (single source of truth) -------------------------------
BANNER_COLOR = "#FFF9C4"
COL_WIDTHS_PLAIN = "25, 75, 75, 120, 110, 120"
COL_WIDTHS_AUDIENCE = "25, 30, 75, 75, 120, 110, 120"
CHANGE_TYPES = ["Rewritten", "Removed", "Data", "Gap", "Drift", "Unresolved Drift"]
FIX_TYPES = {"Rewritten", "Removed", "Data"}  # count toward "violations fixed"

# audience -> set of P0 rule numbers (the preset table in SKILL.md)
AUDIENCE_P0 = {
    "leadership": {1, 2, 3, 5, 7, 25, 26},
    "peers": {6, 16, 17, 18, 19},
    "xfn": {1, 2, 3, 7, 8, 25, 26},
}

# global rule number -> category (matches references/PRINCIPLES.md)
_CATEGORY_RANGES = [
    (1, 8, "Structure and Purpose"),
    (9, 15, "Sentence-Level Clarity"),
    (16, 20, "Precision and Data"),
    (21, 24, "Durability and Context"),
    (25, 28, "Language and Terminology"),
    (29, 33, "Anti-Patterns"),
    (34, 38, "Editorial Integrity"),
]


def category_for(rule):
    try:
        r = int(rule)
    except (TypeError, ValueError):
        return None
    for lo, hi, name in _CATEGORY_RANGES:
        if lo <= r <= hi:
            return name
    return None


def fail(msg):
    sys.stderr.write("render_output.py: %s\n" % msg)
    sys.exit(2)


def resolve_now(spec):
    raw = spec.get("now")
    if raw:
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            fail("could not parse 'now' as ISO 8601: %r" % raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = datetime.now(timezone.utc)
    tzname = spec.get("author_timezone")
    if tzname:
        if ZoneInfo is None:
            fail("zoneinfo unavailable; cannot honour author_timezone")
        try:
            dt = dt.astimezone(ZoneInfo(tzname))
        except Exception:  # noqa: BLE001 - report any tz lookup failure uniformly
            fail("unknown author_timezone: %r" % tzname)
    return dt


def order_and_number(records):
    """Preserve document order, de-dupe exact sites, assign sequential IDs.

    The model emits records in document order. If every record carries a numeric
    "order" field, sort by it (stable); otherwise input order is kept. Section and
    paragraph are used for the location string and de-duplication, not for sorting
    (section names are not positional).
    """
    decorated = list(enumerate(records))
    if records and all("order" in r for r in records):
        decorated.sort(key=lambda p: (_as_int(p[1].get("order")), p[0]))
    seen = set()
    out = []
    for _, rec in decorated:
        key = (rec.get("type"), rec.get("section"), rec.get("paragraph"),
               rec.get("original"), rec.get("revised"))
        if key in seen:
            continue
        seen.add(key)
        out.append(rec)
    for i, rec in enumerate(out, start=1):
        rec["_id"] = i
    return out


def _as_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def priority_for(rule, audience):
    if not audience:
        return None
    p0 = AUDIENCE_P0.get(audience)
    if p0 is None:
        fail("unknown audience: %r (expected leadership|peers|xfn)" % audience)
    try:
        return "P0" if int(rule) in p0 else "P1"
    except (TypeError, ValueError):
        return "P1"


def build_rows(records, audience):
    rows = []
    for rec in records:
        location = "§%s, ¶%s" % (rec.get("section", ""), rec.get("paragraph", ""))
        row = {
            "id": rec["_id"],
            "type": rec.get("type", ""),
            "location": location,
            "original": rec.get("original", ""),
            "revised": rec.get("revised", ""),
            "reasoning": rec.get("reasoning", ""),
        }
        if audience:
            row["priority"] = priority_for(rec.get("rule"), audience)
        rows.append(row)
    return rows


def counts(records, applicable_rule_count):
    by_type = {t: 0 for t in CHANGE_TYPES}
    for rec in records:
        t = rec.get("type")
        if t in by_type:
            by_type[t] += 1
    cat_freq = {}
    for rec in records:
        cat = category_for(rec.get("rule"))
        if cat:
            cat_freq[cat] = cat_freq.get(cat, 0) + 1
    top = sorted(cat_freq.items(), key=lambda kv: (-kv[1], kv[0]))
    top_categories = ", ".join("%s (%d)" % (c, n) for c, n in top[:3]) or "none"
    return {
        "X": applicable_rule_count,
        "Y": sum(by_type[t] for t in FIX_TYPES),
        "Z": by_type["Gap"],
        "A": by_type["Drift"],
        "B": by_type["Unresolved Drift"],
        "top_categories": top_categories,
    }


def violation_summary(c):
    return (
        "Rules: %(X)s of 38 applicable.\n"
        "Violations fixed: %(Y)d.\n"
        "Gaps flagged: %(Z)d.\n"
        "Verification: %(A)d drift violations caught and fixed. "
        "%(B)d unresolved drift violations remain.\n"
        "Top categories: %(top_categories)s." % c
    )


def _cell(text):
    return "<td>%s</td>" % html.escape(str(text), quote=False)


def changes_table_html(rows, audience):
    if audience:
        headers = ["ID", "Priority", "Type", "Location", "Original", "Revised", "Reasoning"]
        widths = COL_WIDTHS_AUDIENCE
        order = ["id", "priority", "type", "location", "original", "revised", "reasoning"]
    else:
        headers = ["ID", "Type", "Location", "Original", "Revised", "Reasoning"]
        widths = COL_WIDTHS_PLAIN
        order = ["id", "type", "location", "original", "revised", "reasoning"]
    parts = ['<table data-col-widths="%s">' % widths]
    parts.append("<tr>%s</tr>" % "".join("<th>%s</th>" % h for h in headers))
    for row in rows:
        parts.append("<tr>%s</tr>" % "".join(_cell(row.get(k, "")) for k in order))
    parts.append("</table>")
    return "".join(parts)


def banner(text):
    return ('<table style="background-color: %s"><tr><td><b>%s</b></td></tr></table>'
            % (BANNER_COLOR, html.escape(text, quote=False)))


def pre_publish_html(rows, audience, summary):
    head = banner("PRE-PUBLISH - delete everything between these banners before publishing.")
    foot = banner("END PRE-PUBLISH - delete everything above this banner before publishing.")
    return "\n".join([
        head,
        "<p><b>Changes Made</b></p>",
        changes_table_html(rows, audience),
        "<p>%s</p>" % html.escape(summary, quote=False).replace("\n", "<br>"),
        "<p><i>Verification evidence checklist: paste the final pass's checklist here "
        "(see references/VERIFICATION.md).</i></p>",
        foot,
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Assemble deterministic narrative-style-editor output.")
    parser.add_argument("--in", dest="infile", help="input JSON file (default: stdin)")
    args = parser.parse_args(argv)

    raw = open(args.infile, encoding="utf-8").read() if args.infile else sys.stdin.read()
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("input is not valid JSON: %s" % exc)

    records = spec.get("records")
    if not isinstance(records, list):
        fail("'records' must be a list")
    for rec in records:
        if rec.get("type") not in CHANGE_TYPES:
            fail("record has invalid type %r (expected one of %s)" % (rec.get("type"), CHANGE_TYPES))

    audience = spec.get("audience")
    if audience is not None and audience not in AUDIENCE_P0:
        fail("unknown audience: %r (expected leadership|peers|xfn or null)" % audience)

    ordered = order_and_number(records)
    rows = build_rows(ordered, audience)
    c = counts(ordered, spec.get("applicable_rule_count", "X"))
    summary = violation_summary(c)
    ts = resolve_now(spec).strftime("%Y-%m-%d %H:%M")
    title = "[Claude] [/narrative-style-editor] %s - (%s)" % (ts, spec.get("original_title", ""))

    out = {
        "title": title,
        "violation_summary": summary,
        "pre_publish_html": pre_publish_html(rows, audience, summary),
        "rows": rows,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
