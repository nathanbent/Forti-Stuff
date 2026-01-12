#!/usr/bin/env python3
"""
generate_fortios.py

Usage examples:
  python generate_fortios.py domains.txt -o fortios_script.txt
  cat domains.txt | python generate_fortios.py -o fortios_script.txt
  python generate_fortios.py domains.txt --status disable
"""

import sys
import argparse
import re
from pathlib import Path

DOMAIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z]{2,})+$")

def normalize_domains(lines, dedupe=True, sort_result=True):
    seen = set()
    out = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        # allow comments starting with #
        if s.startswith("#"):
            continue
        # strip surrounding quotes if user put them
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # validate basic domain pattern; if invalid, still include but warn
        if DOMAIN_RE.match(s) is None:
            # include, but keep as-is (some users may have nonstandard hosts)
            pass
        key = s.lower()
        if dedupe:
            if key in seen:
                continue
            seen.add(key)
        out.append(s)
    if sort_result:
        out.sort(key=lambda x: x.lower())
    return out

def generate_fortios(domains, status="enable"):
    status = status.lower()
    if status not in ("enable", "disable"):
        raise ValueError("status must be 'enable' or 'disable'")
    lines = []
    for d in domains:
        # escape any double quotes by backslash just in case
        safe = d.replace('"', '\\"')
        lines.append(f'edit "{safe}"')
        lines.append(f'set status {status}')
        lines.append('next')
    return "\n".join(lines) + ("\n" if lines else "")

def main():
    p = argparse.ArgumentParser(description="Generate FortiOS script from a list of domains.")
    p.add_argument("input", nargs="?", help="Path to domains file; if omitted, read from stdin")
    p.add_argument("-o", "--output", help="Write generated script to this file (defaults to stdout)")
    p.add_argument("--status", choices=["enable", "disable"], default="enable",
                   help="Status to set for each edit block")
    p.add_argument("--no-dedupe", dest="dedupe", action="store_false",
                   help="Do not deduplicate domain entries")
    p.add_argument("--no-sort", dest="sort_result", action="store_false",
                   help="Do not sort domains; preserve order (after dedupe if enabled)")
    args = p.parse_args()

    if args.input:
        ppath = Path(args.input)
        if not ppath.exists():
            print(f"Error: input file '{args.input}' not found.", file=sys.stderr)
            sys.exit(2)
        raw_lines = ppath.read_text(encoding="utf-8", errors="ignore").splitlines()
    else:
        raw = sys.stdin.read()
        raw_lines = raw.splitlines()

    domains = normalize_domains(raw_lines, dedupe=args.dedupe, sort_result=args.sort_result)
    script = generate_fortios(domains, status=args.status)

    if args.output:
        Path(args.output).write_text(script, encoding="utf-8")
    else:
        sys.stdout.write(script)

if __name__ == "__main__":
    main()
