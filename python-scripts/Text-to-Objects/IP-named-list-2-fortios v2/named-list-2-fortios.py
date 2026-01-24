#!/usr/bin/env python3
import re
import ipaddress

# ----------------------------
# Config
# ----------------------------
ENABLE_ALLOW_ROUTING = True  # Toggle "set allow-routing enable" on/off
ENABLE_COLOR = False       # Toggle color on/off
COLOR_ID = 7               # FortiGate color (1–32 typically)


def strip_inline_comment(s: str) -> str:
    # Remove anything after # or ; (common comment styles)
    return re.split(r"[#;]", s, maxsplit=1)[0].strip()


def normalize_subnet(line: str) -> tuple[str, str]:
    """
    Returns (subnet_for_fortigate, ip_only_for_name)

    Supports:
      - CIDR:          10.1.2.0/24
      - IP only:       10.1.2.3  (assumes /32)
      - IP + netmask:  10.1.2.0 255.255.255.0
    """
    s = strip_inline_comment(line)
    if not s:
        raise ValueError("empty line")

    # FortiGate-style: "IP NETMASK"
    parts = s.split()
    if len(parts) == 2 and "/" not in parts[0]:
        ip_str, mask_str = parts[0], parts[1]
        ipaddress.ip_address(ip_str)
        ipaddress.ip_address(mask_str)  # validates dotted-quad
        return f"{ip_str} {mask_str}", ip_str

    # CIDR or IP-only
    if "/" not in s:
        s = f"{s}/32"

    net = ipaddress.ip_network(s, strict=False)
    ip_only = str(net.network_address)
    return str(net), ip_only


def format_name_ip_pairs(input_file: str, output_file: str) -> None:
    written = 0
    skipped = 0

    # Read all meaningful lines (no blanks/comments)
    lines: list[str] = []
    with open(input_file, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            cleaned = strip_inline_comment(raw)
            if cleaned:
                lines.append(cleaned)

    if len(lines) % 2 != 0:
        print(
            f"Warning: input has an odd number of non-empty lines ({len(lines)}). "
            f"The last line will be ignored: '{lines[-1]}'"
        )

    with open(output_file, "w", encoding="utf-8") as out:
        for i in range(0, len(lines) - 1, 2):
            name_line = lines[i].strip().strip('"')
            ip_line = lines[i + 1].strip()

            try:
                subnet, _ip_only = normalize_subnet(ip_line)

                out.write(f'edit "{name_line}"\n')
                out.write(f"set subnet {subnet}\n")

                if ENABLE_ALLOW_ROUTING:
                    out.write("set allow-routing enable\n")

                if ENABLE_COLOR:
                    out.write(f"set color {COLOR_ID}\n")

                out.write("next\n\n")
                written += 1

            except Exception as e:
                skipped += 1
                print(f"[Pair starting line {i+1}] Skipped name='{name_line}' ip='{ip_line}': {e}")

    print(f"Done. Wrote {written} entries. Skipped {skipped} entries.")


if __name__ == "__main__":
    format_name_ip_pairs("input.txt", "output.txt")
