#!/usr/bin/env python3
"""Deterministic false-profundity / manufactured-contrast detection for Rule 30.

Rule 30 (No false profundity) bans dramatic lines that sound deep but say nothing,
including the *manufactured-contrast kicker*: an unverifiable sweeping generalization
("most teams...", "everyone...", "anyone can...") used to set up a punchy short
sentence, plus the "not X, but Y" reveal. Spotting candidate sentences is mechanical,
so code does it; the MODEL then decides, per candidate, whether it is genuine false
profundity to cut or rewrite, or a legitimate, specific sentence to keep.

Reads text from stdin or --in FILE. Prints, as JSON, each candidate sentence with its
matched pattern(s), a reason per pattern, any paired setup line, and first-occurrence
position (1-based line and column, plus character offset). Candidates are SUGGESTIONS,
not verdicts: a short factual sentence ("None failed.") can match and still be fine.
Standard library only.

Patterns:
  sweeping_generalization  opens with an unbacked quantifier (Most/Many/Everyone/
                           Anyone/Nobody/No one/Few) and contains no number. Also a
                           Rule 17 weasel issue.
  manufactured_contrast    a sweeping-generalization sentence immediately followed by a
                           short (<=7-word) kicker, OR any short (<=6-word) kicker with
                           an absolute marker (can't/never/only...) right after a long
                           (>=14-word) sentence. The classic "...; few can." tell.
  contrast_reveal          "not just/only/merely/about X ... but Y", "isn't about/just/
                           only ...", or the two-sentence "It's not X. It's Y." reveal.
  false_profundity         curated dramatic one-liners ("Everything changed.", etc.).
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import sys

SWEEPING_RE = re.compile(
    r"^(most|many|everyone|everybody|anyone|anybody|nobody|no\s+one|few)\b", re.I
)
NUM_RE = re.compile(r"\d|%")
MARKER_RE = re.compile(
    r"\b(can'?t|cannot|won'?t|don'?t|doesn'?t|didn'?t|never|always|none|"
    r"no\s+one|nobody|few|only|everything|nothing|anyone)\b",
    re.I,
)
CONTRAST_IN_SENT_RE = re.compile(
    r"(\bnot\s+(just|only|merely|about)\b.+\bbut\b"
    r"|\bisn'?t\s+(about|just|only|the)\b"
    r"|\bit'?s\s+not\b.+\bit'?s\b)",
    re.I,
)
NOT_OPENER_RE = re.compile(
    r"^(it'?s|this\s+is|that'?s|these\s+are|we'?re|i'?m)\s+not\b", re.I
)
NOT_CONTINUE_RE = re.compile(
    r"^(it'?s|this\s+is|that'?s|these\s+are|we'?re|i'?m)\b", re.I
)
PROFUNDITY_RE = re.compile(
    r"^(everything\s+(changed|is\s+different|was\s+different)"
    r"|and\s+then\s+it\s+hit\s+me"
    r"|that\s+changes\s+everything"
    r"|nothing\s+(was|would\s+be|is)\s+(ever\s+)?the\s+same"
    r"|the\s+rest\s+is\s+history"
    r"|let\s+that\s+sink\s+in)\b",
    re.I,
)

SHORT_KICKER_MAX = 6  # words: a standalone punchy kicker after a long sentence
PAIR_KICKER_MAX = 7   # words: the kicker right after a sweeping generalization
LONG_SETUP_MIN = 14   # words: the "long sentence" before a standalone kicker

SENTENCE_RE = re.compile(r"\S.*?[.!?]+(?=\s|$)", re.S)
PARAGRAPH_RE = re.compile(r"(?:[^\n]+\n?)+")


def make_locator(text):
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)

    def locate(off):
        li = bisect.bisect_right(starts, off) - 1
        return li + 1, off - starts[li] + 1

    return locate


def normalize(s):
    return re.sub(r"\s+", " ", s).strip()


def iter_paragraphs(text):
    for m in PARAGRAPH_RE.finditer(text):
        if m.group(0).strip():
            yield m.start(), m.group(0)


def iter_sentences(pstart, ptext):
    return [(pstart + m.start(), normalize(m.group(0)))
            for m in SENTENCE_RE.finditer(ptext)]


def scan(text):
    locate = make_locator(text)
    flagged = {}  # offset -> candidate

    def add(off, sent, pattern, reason, setup=None):
        c = flagged.get(off)
        if c is None:
            line, col = locate(off)
            c = {"offset": off, "line": line, "column": col,
                 "sentence": sent, "patterns": [], "reasons": []}
            flagged[off] = c
        if pattern not in c["patterns"]:
            c["patterns"].append(pattern)
            c["reasons"].append(reason)
        if setup and "setup" not in c:
            c["setup"] = setup

    for pstart, ptext in iter_paragraphs(text):
        sents = iter_sentences(pstart, ptext)
        wcs = [len(s.split()) for _, s in sents]
        for i, (off, s) in enumerate(sents):
            sweeping = bool(SWEEPING_RE.match(s)) and not NUM_RE.search(s)
            if sweeping:
                add(off, s, "sweeping_generalization",
                    "Opens with an unbacked sweeping quantifier and cites no number "
                    "(Rule 17 weasel + Rule 30). State who / how many, or delete the framing.")
            if CONTRAST_IN_SENT_RE.search(s):
                add(off, s, "contrast_reveal",
                    "'not just/only/about X ... but Y' or 'isn't ...' reveal (Rule 30). "
                    "State the point plainly instead of the rhetorical split.")
            if (NOT_OPENER_RE.match(s) and i + 1 < len(sents)
                    and NOT_CONTINUE_RE.match(sents[i + 1][1])):
                add(off, s, "contrast_reveal",
                    "Two-sentence \"It's not X. It's Y.\" reveal (Rule 30). "
                    "Drop the reveal; state it plainly.")
            if PROFUNDITY_RE.search(s):
                add(off, s, "false_profundity",
                    "Dramatic one-liner that states nothing concrete (Rule 30). "
                    "Say what actually happened, with data.")
            # manufactured-contrast pair: sweeping setup followed by a short kicker
            if sweeping and i + 1 < len(sents) and wcs[i + 1] <= PAIR_KICKER_MAX:
                koff, ks = sents[i + 1]
                add(koff, ks, "manufactured_contrast",
                    "Short kicker right after a sweeping generalization (the \"...; few "
                    "can.\" tell; Rule 30). Cut it, or replace the generalization with the "
                    "specific fact.", setup=s)
            # standalone short kicker after a long sentence, with an absolute marker
            if (i > 0 and wcs[i] <= SHORT_KICKER_MAX and wcs[i - 1] >= LONG_SETUP_MIN
                    and MARKER_RE.search(s)):
                add(off, s, "manufactured_contrast",
                    "Short punchy kicker (absolute marker) after a long sentence (Rule 30). "
                    "Likely a manufactured payoff; fold it into the prior sentence or cut.",
                    setup=sents[i - 1][1])

    return [flagged[o] for o in sorted(flagged)]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Detect Rule 30 false-profundity / manufactured-contrast candidates.")
    parser.add_argument("--in", dest="infile", help="input text file (default: stdin)")
    args = parser.parse_args(argv)
    text = open(args.infile, encoding="utf-8").read() if args.infile else sys.stdin.read()
    results = scan(text)
    json.dump({"count": len(results), "candidates": results}, sys.stdout,
              ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
