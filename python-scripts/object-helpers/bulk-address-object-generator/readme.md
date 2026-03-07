# object-helper-v3

A Python script that generates FortiGate firewall address objects and address groups from a list of FQDNs and/or IP addresses/CIDRs.

## Requirements

- Python 3.10+
- No external dependencies (standard library only)

## Usage

```
python object-helper-v3.py [-i INPUT] [-o OUTPUT] [options]
```

### Basic Examples

```bash
# Read from input.txt, write to output.txt
python object-helper-v3.py

# Specify input/output files
python object-helper-v3.py -i hosts.txt -o fortigate.cfg

# Print to stdout
python object-helper-v3.py -i hosts.txt --stdout

# Add a prefix to all object names
python object-helper-v3.py -i hosts.txt --prefix SITE --prefix-delim -

# Use tab-delimited name/value pairs
python object-helper-v3.py -i hosts.txt --delimiter '\t'

# Create an all-objects group and per-FQDN groups
python object-helper-v3.py -i hosts.txt --all-group 'My Objects' --per-fqdn-group
```

## Input Formats

**Default** — one FQDN or IP/CIDR per line:
```
example.com
*.wildcard.com
10.0.0.1
192.168.1.0/24
```

**Explicit names** (`-e` / `--explicit-names`) — alternating name/value pairs:
```
my-server
10.0.0.1
my-fqdn
example.com
```

**Delimiter** (`--delimiter DELIM`) — single-line `name<delim>value` format:
```
my-server:10.0.0.1
my-fqdn:example.com
```

Lines beginning with `#` or `;` (and inline comments) are ignored.

## Output

The script generates FortiGate CLI config blocks ready to paste into the CLI or load via script:

```
config firewall address
edit "Prefix-example.com"
    set type fqdn
    set fqdn "example.com"
next
end

config firewall addrgrp
edit "Prefix-Generated Objects"
    set member "Prefix-example.com"
next
end
```

## Options

| Flag | Description |
|------|-------------|
| `-i`, `--input FILE` | Input file (default: `input.txt`) |
| `-o`, `--output FILE` | Output file (default: `output.txt`) |
| `--stdout` | Write generated config to stdout |
| `-e`, `--explicit-names` | Input is alternating name/value pairs |
| `--delimiter DELIM` | Each line is `name<DELIM>fqdn` (e.g. `\t` or `:`) |
| `-p`, `--prefix PREFIX` | Prepend prefix to every object name |
| `--prefix-delim DELIM` | Separator between prefix and object name |
| `--lowercase` | Lowercase all FQDNs before processing |
| `--no-fqdn-objects` | Skip FQDN address objects |
| `--ip-objects` | Also emit resolved /32 IP objects (requires DNS) |
| `--max-ips N` | Max resolved IPs per FQDN (default: 20) |
| `--dns-timeout SEC` | DNS lookup timeout in seconds (default: 3.0) |
| `--dns-workers N` | Parallel DNS threads (default: 10) |
| `--all-group NAME` | Wrap all objects in a single address group |
| `--per-fqdn-group` | Create one address group per FQDN |
| `--color ID` | Set color ID (1–32) on address objects |
| `--interface IFACE` | Set `associated-interface` on address objects |
| `--allow-routing` | Set `allow-routing enable` on address objects |
| `--no-comment` | Suppress comment fields |

## Configuration

Many additional settings (comments, group options, fabric objects, passive FQDN learning, cache TTL, etc.) can be set by editing the `Config` dataclass at the top of the script under the `USER CONFIG` section.

## Notes

- Object names are validated against FortiGate's 79-character limit; names exceeding this will produce a warning.
- Wildcard FQDNs (e.g. `*.example.com`) are supported as FQDN objects but cannot be resolved for IP objects.
- Duplicate object names are detected and skipped with a warning.
- The `{prefix}` placeholder can be used in group name templates for fine-grained prefix placement.