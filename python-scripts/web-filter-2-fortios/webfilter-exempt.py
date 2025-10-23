#!/usr/bin/env python3
"""
generate_fortios_exempt.py

Generates a FortiOS script like:
  edit "website.com"
  set status enable
  set action exempt
  next
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
        if not s or s.startswith("#"):
            continue
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        if DOMAIN_RE.match(s) is None:
            pass  # keep non-standard names too
        key = s.lower()
        if dedupe and key in seen:
            continue
        seen.add(key)
        out.append(s)
    if sort_result:
        out.sort(key=lambda x: x.lower())
    return out

def generate_fortios(domains, status="enable", action="exempt"):
    status = status.lower()
    action = action.lower()
    if status not in ("enable", "disable"):
        raise ValueError("status must be 'enable' or 'disable'")
    lines = []
    for d in domains:
        safe = d.replace('"', '\\"')
        lines.append(f'edit "{safe}"')
        lines.append(f'set status {status}')
        lines.append(f'set action {action}')
        lines.append('next')
    return "\n".join(lines) + ("\n" if lines else "")

def main():
    p = argparse.ArgumentParser(description="Generate FortiOS exempt-action script from a list of domains.")
    p.add_argument("input", nargs="?", help="Path to domains file; if omitted, read from stdin")
    p.add_argument("-o", "--output", help="Write generated script to this file (defaults to stdout)")
    p.add_argument("--status", choices=["enable", "disable"], default="enable",
                   help="Status to set for each edit block")
    p.add_argument("--action", default="exempt",
                   help="Action to set (default: exempt)")
    p.add_argument("--no-dedupe", dest="dedupe", action="store_false",
                   help="Do not deduplicate entries")
    p.add_argument("--no-sort", dest="sort_result", action="store_false",
                   help="Do not sort entries")
    args = p.parse_args()

    raw_lines = (Path(args.input).read_text(encoding="utf-8", errors="ignore").splitlines()
                 if args.input else sys.stdin.read().splitlines())
    domains = normalize_domains(raw_lines, dedupe=args.dedupe, sort_result=args.sort_result)
    script = generate_fortios(domains, status=args.status, action=args.action)

    if args.output:
        Path(args.output).write_text(script, encoding="utf-8")
    else:
        sys.stdout.write(script)

if __name__ == "__main__":
    main()
