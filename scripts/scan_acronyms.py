#!/usr/bin/env python3
"""Deterministic acronym detection for Rule 25 (R20).

Rule 25 calls itself a "mechanical check": scan the document for acronym-like
sequences and verify each is defined on first use. The detection and
first-occurrence bookkeeping are deterministic, so code does them; the MODEL then
decides, for each candidate, whether to define it, expand it from context, or leave
it (a common acronym for a technical audience).

Reads text from stdin or --in FILE. Prints, as JSON, every acronym-like token with
its first occurrence (1-based line and column, plus character offset). Standard
library only.

A token is acronym-like if it is >=3 characters and either all uppercase or has 2+
uppercase letters with mixed case (e.g. MAU, SIEM, IaC, PaaS, DevOps), excluding a
small allowlist of near-universal acronyms.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

ALLOWLIST = {"USA", "API", "URL", "HTML", "HTTP", "HTTPS", "JSON", "CSV", "PDF", "ID", "OK"}
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]{2,}")


def is_acronym_like(tok):
    uppers = sum(1 for ch in tok if ch.isupper())
    if uppers < 2:
        return False
    if tok.upper() in ALLOWLIST:
        return False
    # all-caps (MAU, SIEM) or mixed case with >=2 capitals (IaC, PaaS, DevOps)
    return tok.isupper() or any(ch.islower() for ch in tok)


def scan(text):
    first = {}
    order = []
    offset = 0
    for lineno, line in enumerate(text.splitlines(keepends=True), start=1):
        for m in TOKEN_RE.finditer(line):
            tok = m.group(0)
            if not is_acronym_like(tok) or tok in first:
                continue
            first[tok] = {
                "acronym": tok,
                "line": lineno,
                "column": m.start() + 1,
                "offset": offset + m.start(),
            }
            order.append(tok)
        offset += len(line)
    return [first[t] for t in order]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect acronym-like tokens (Rule 25).")
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
