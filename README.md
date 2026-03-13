# Forti-Stuff

> FortiScripts to make my FortiLife easier (sometimes)

## What's this?

I've been spending more time in the FortiGate CLI during deployments and migrations, so I've been building up a collection of scripts and notes to make that less painful. Mostly FortiOS stuff, with some random tidbits thrown in (like color codes).

## What's in here

```
Forti-Stuff/
├── python-scripts/
│   ├── object-helpers/              <- Helps with bulk object stuff.
│   │   ├── bulk-address-object-generator/  <- Bulk firewall address object generator.
│   │   └── web-filter/             <- Web filter URL list generator.
│   ├── testing-conversion-scripts/ <- WIP
│   │   └── SonicWALL-to-FortiGate/
│   └── deprecated-Text-to-Objects/ <- Old stuff, kept for reference
└── useful-commands/                <- CLI notes and diagnostic commands
```

## The Main Script — `object-helper-v3`

**Location:** `python-scripts/object-helpers/bulk-address-object-generator/`

This is the one you want. It takes a list of IPs, CIDRs, and/or FQDNs and spits out FortiGate CLI config blocks ready to paste in or run as a script. Handles address objects, address groups, prefixes, DNS resolution, and a bunch of other options.

See the [readme](python-scripts/object-helpers/bulk-address-object-generator/readme.md) in that folder for full usage and options.

Quick example:
```bash
# Defaults: reads input.txt, writes output.txt
python object-helper-v3.py

# With a prefix and an all-objects group
python object-helper-v3.py --prefix SITE --all-group "Site Objects"

# Print to stdout instead of a file
python object-helper-v3.py --stdout
```

## Conversion Scripts (WIP)

**Location:** `python-scripts/testing-conversion-scripts/`

Work in progress — don't get too excited yet.

- **SonicWALL to FortiGate** — Converts SonicWALL address object exports (URL-encoded key=value format) into FortiOS address objects.

## Commands & Notes

**Location:** `useful-commands/`

Random CLI commands and notes I've found useful.

- [FortiSwitch Diagnostics](useful-commands/fortiswitch-diag.md) — diag commands for FortiSwitch (MAC cache, config resync, etc.)
- [IPsec Diagnostics](useful-commands/ipsec-diag.md) — diag commands for IPsec tunnels

## FortiColors

Mapping of FortiOS color IDs, because the GUI doesn't tell you and I got tired of guessing.

> Heads up — I haven't double-checked all of these, let me know if something's wrong.

```
1  - Black          17 - Cyan blue
2  - Deep blue      18 - Light blue
3  - Medium green   19 - Royal blue
4  - Dark red       20 - Indigo
5  - Light red      21 - Purple
6  - Bright red     22 - Violet
7  - Dark red       23 - Magenta
8  - Dark orange    24 - Dark pink
9  - Orange         25 - Maroon
10 - Yellow         26 - Light gray
11 - Dark yellow    27 - Dark gray
12 - Brown          28 - Light orange
13 - Bright green   29 - Tan
14 - Muted green    30 - Blue gray
15 - Dark green     31 - Lavender
16 - Deep green     32 - Olive gray
```