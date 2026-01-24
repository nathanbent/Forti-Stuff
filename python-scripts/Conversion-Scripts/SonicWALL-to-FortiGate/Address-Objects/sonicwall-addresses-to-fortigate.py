#!/usr/bin/env python3
"""
Convert SonicWall-style addrObj exports (URL-encoded key=value lines)
into FortiGate CLI (FortiOS) address objects.

Input : input.txt
Output: output.txt

Behavior:
- Decodes URL encoding (e.g. %20 -> space, %21 -> !)
- Groups entries by index (_0, _1, _2, ...)
- Skips placeholder/group objects with 0.0.0.0/0.0.0.0
- If mask is 0.0.0.0, assumes /32 (255.255.255.255)
- DOES NOT set associated-interface
"""

from __future__ import annotations

import re
import ipaddress
from urllib.parse import unquote_plus
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"


@dataclass
class AddrObj:
    idx: int
    name: Optional[str] = None
    name_disp: Optional[str] = None
    zone: Optional[str] = None
    ip1: Optional[str] = None
    ip2: Optional[str] = None
    raw: Dict[str, str] = field(default_factory=dict)


KEY_RE = re.compile(r"^(?P<key>[A-Za-z0-9]+)_(?P<idx>\d+)$")


def decode(s: str) -> str:
    return unquote_plus(s)


def is_zero_ip(ip: Optional[str]) -> bool:
    return (ip or "").strip() == "0.0.0.0"


def normalize_subnet(ip1: str, ip2: str) -> Tuple[str, str]:
    ip1 = ip1.strip()
    ip2 = ip2.strip()

    ipaddress.IPv4Address(ip1)
    ipaddress.IPv4Address(ip2)

    if ip2 == "0.0.0.0":
        return ip1, "255.255.255.255"

    return ip1, ip2


def load_objects(lines) -> Dict[int, AddrObj]:
    objs: Dict[int, AddrObj] = {}

    for line in lines:
        line = line.strip()
        if not line or "=" not in line:
            continue

        k, v = line.split("=", 1)
        k = k.strip()
        v = decode(v.strip())

        m = KEY_RE.match(k)
        if not m:
            continue

        key = m.group("key")
        idx = int(m.group("idx"))

        obj = objs.setdefault(idx, AddrObj(idx=idx))
        obj.raw[key] = v

        if key == "addrObjId":
            obj.name = v
        elif key == "addrObjIdDisp":
            obj.name_disp = v
        elif key == "addrObjZone":
            obj.zone = v
        elif key == "addrObjIp1":
            obj.ip1 = v
        elif key == "addrObjIp2":
            obj.ip2 = v

    return objs


def choose_name(obj: AddrObj) -> str:
    return (obj.name or obj.name_disp or f"addrObj_{obj.idx}").strip()


def should_emit(obj: AddrObj) -> bool:
    if obj.ip1 is None or obj.ip2 is None:
        return False
    if is_zero_ip(obj.ip1) and is_zero_ip(obj.ip2):
        return False
    return True


def generate_fortios(objs: Dict[int, AddrObj]) -> str:
    out = []
    out.append("config firewall address")

    for idx in sorted(objs):
        obj = objs[idx]
        if not should_emit(obj):
            continue

        name = choose_name(obj)

        try:
            ip, mask = normalize_subnet(obj.ip1, obj.ip2)
        except Exception:
            out.append(f'    # Skipped "{name}" (invalid IP data)')
            continue

        out.append(f'    edit "{name}"')
        out.append(f"        set subnet {ip} {mask}")
        out.append("    next")

    out.append("end")
    return "\n".join(out) + "\n"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
        objs = load_objects(f)

    output = generate_fortios(objs)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Converted {len(objs)} indexed records → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
