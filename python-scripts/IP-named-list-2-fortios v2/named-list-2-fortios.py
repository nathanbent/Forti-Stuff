#!/usr/bin/env python3
import re
import ipaddress

# ----------------------------
# Config
# ----------------------------
NAME_TEMPLATE = "Test IP"   # Object name prefix
ENABLE_COLOR = True           # Toggle color on/off
COLOR_ID = 7                  # FortiGate color (1–32 typically)


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
        ipaddress.ip_address(mask_str)
        return f"{ip_str} {mask_str}", ip_str

    # CIDR or IP-only
    if "/" not in s:
        s = f"{s}/32"

    net = ipaddress.ip_network(s, strict=False)
    ip_only = str(net.network_address)
    return str(net), ip_only


def format_ip_list(input_file: str, output_file: str) -> None:
    written = 0
    skipped = 0

    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:

        for lineno, raw_line in enumerate(infile, start=1):
            line = strip_inline_comment(raw_line)

            if not line:
                continue

            try:
                subnet, ip_only = normalize_subnet(line)
                name = f"{NAME_TEMPLATE} - {ip_only}"

                outfile.write(f'edit "{name}"\n')
                outfile.write(f"set subnet {subnet}\n")

                if ENABLE_COLOR:
                    outfile.write(f"set color {COLOR_ID}\n")

                outfile.write("next\n\n")
                written += 1

            except Exception as e:
                skipped += 1
                print(f"[Line {lineno}] Skipped '{raw_line.strip()}': {e}")

    print(f"Done. Wrote {written} entries. Skipped {skipped} entries.")


if __name__ == "__main__":
    format_ip_list("input.txt", "output.txt")
