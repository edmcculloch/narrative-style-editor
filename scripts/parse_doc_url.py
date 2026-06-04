#!/usr/bin/env python3
"""Validate a Google Docs URL and extract its document ID (R28).

Confirms the input is a Google Docs URL and extracts the document ID before any
`gdocs` call, so a malformed or non-Doc URL fails fast with a clear message instead
of an opaque downstream error. Standard library only.

Usage:
    parse_doc_url.py "<url>"
    echo "<url>" | parse_doc_url.py

Prints the document ID to stdout on success (exit 0). On failure, prints an error
to stderr and exits 2.
"""
from __future__ import annotations

import re
import sys

DOC_ID_RE = re.compile(r"https?://docs\.google\.com/document/d/([A-Za-z0-9_-]{10,})")


def extract(url):
    m = DOC_ID_RE.search(url.strip())
    return m.group(1) if m else None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    url = argv[0] if argv else sys.stdin.read().strip()
    if not url:
        sys.stderr.write("parse_doc_url.py: no URL provided\n")
        return 2
    doc_id = extract(url)
    if not doc_id:
        sys.stderr.write(
            "parse_doc_url.py: not a Google Docs URL "
            "(expected https://docs.google.com/document/d/<id>): %r\n" % url)
        return 2
    sys.stdout.write(doc_id + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
