#!/usr/bin/env python3
import re

# ----------------------------
# Config
# ----------------------------

# False = one FQDN per line
# True  = pairs: name, fqdn
USE_EXPLICIT_NAMES = False

ENABLE_PREFIX = True
NAME_PREFIX = "NTP-"

ENABLE_COLOR = False
COLOR_ID = 7
ENABLE_ALLOW_ROUTING = False

LOWERCASE_FQDN = False


def strip_inline_comment(s: str) -> str:
    return re.split(r"[#;]", s, maxsplit=1)[0].strip()


def validate_fqdn(fqdn: str) -> str:
    f = fqdn.strip().strip('"').strip("'")
    if LOWERCASE_FQDN:
        f = f.lower()

    if not f:
        raise ValueError("empty fqdn")
    if any(ch.isspace() for ch in f):
        raise ValueError("fqdn contains whitespace")

    candidate = f[2:] if f.startswith("*.") else f

    if "://" in candidate or "/" in candidate:
        raise ValueError("fqdn looks like a URL")

    labels = candidate.split(".")
    if len(labels) < 2:
        raise ValueError("fqdn must contain a dot")

    allowed = re.compile(r"^[A-Za-z0-9-]+$")
    for lab in labels:
        if not lab:
            raise ValueError("empty fqdn label")
        if lab.startswith("-") or lab.endswith("-"):
            raise ValueError("label starts/ends with '-'")
        if not allowed.match(lab):
            raise ValueError(f"invalid chars in label: {lab}")

    return f


def safe_obj_name(name: str) -> str:
    n = name.replace('"', "").replace("\n", " ").strip()
    n = re.sub(r"\s+", " ", n)
    if not n:
        raise ValueError("empty object name")
    return n


def build_obj_name(name_from_input: str | None, fqdn: str) -> str:
    base = name_from_input if USE_EXPLICIT_NAMES else fqdn
    base = safe_obj_name(base)

    if ENABLE_PREFIX and NAME_PREFIX:
        return safe_obj_name(f"{NAME_PREFIX}{base}")

    return base


def write_fqdn_object(out, obj_name: str, fqdn: str) -> None:
    out.write(f'edit "{obj_name}"\n')
    out.write("set type fqdn\n")
    out.write(f'set fqdn "{fqdn}"\n')

    if ENABLE_ALLOW_ROUTING:
        out.write("set allow-routing enable\n")

    if ENABLE_COLOR:
        out.write(f"set color {COLOR_ID}\n")

    out.write("next\n\n")


def load_lines(input_file: str) -> list[str]:
    lines = []
    with open(input_file, "r", encoding="utf-8") as f:
        for raw in f:
            cleaned = strip_inline_comment(raw)
            if cleaned:
                lines.append(cleaned)
    return lines


def format_fqdn_objects(input_file: str, output_file: str) -> None:
    written = 0
    skipped = 0
    lines = load_lines(input_file)

    with open(output_file, "w", encoding="utf-8") as out:
        if USE_EXPLICIT_NAMES:
            if len(lines) % 2 != 0:
                print(f"Warning: odd number of lines ({len(lines)}); last ignored")

            for i in range(0, len(lines) - 1, 2):
                name_line = lines[i].strip().strip('"')
                fqdn_line = lines[i + 1].strip()

                try:
                    fqdn = validate_fqdn(fqdn_line)
                    obj_name = build_obj_name(name_line, fqdn)
                    write_fqdn_object(out, obj_name, fqdn)
                    written += 1
                except Exception as e:
                    skipped += 1
                    print(f"[Pair {i+1}] Skipped name='{name_line}' fqdn='{fqdn_line}': {e}")

        else:
            for lineno, fqdn_line in enumerate(lines, start=1):
                try:
                    fqdn = validate_fqdn(fqdn_line)
                    obj_name = build_obj_name(None, fqdn)
                    write_fqdn_object(out, obj_name, fqdn)
                    written += 1
                except Exception as e:
                    skipped += 1
                    print(f"[Line {lineno}] Skipped fqdn='{fqdn_line}': {e}")

    print(f"Done. Wrote {written} entries. Skipped {skipped} entries.")


if __name__ == "__main__":
    format_fqdn_objects("input.txt", "output.txt")
