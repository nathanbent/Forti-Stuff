# Forti-Stuff

> FortiScripts to make my FortiLife easier (sometimes)

## The Premise
I've been spending more time in the FortiGate CLI during deployments and migrations, and have been creating scripts to help with this process.

## The Stuff
This is a collection of things I've found useful for FortiStuff- mostly FortiOS.  Also some random notes I've found (like color codes)

### Address Object helpers

- Named lists to FortiOS (`python-scripts/address-object-helpers/fortios-ip-address-list-generator.py`)
    - 
- Bulk lists to be automatically named (`address-list-2-fortios.py`)
    - This takes a list of IPs and applies a basic naming scheme to them.
        - Basically `<custom_prefix-entry_#-entry>` so like `Google_DNS-1-8.8.8.8`
    - Has *very* basic intelligence:
        - 1.1.1.1 will be created as 1.1.1.1/32
        - 192.168.0.0/24 will be created as 192.168.0.0/24
- Bulk webfilter URL import named (`webfilter-2-fortios.py`)
More coming soon!

## How to use
- The python scripts generally take a input.txt and make an output.txt
- An input.txt.sample is provided to show how to format the input.txt
- These are mostly to help bulk import IPs and FQDNs from copy/paste stuff

## FortiColors

! Please let me know if any are wrong - I haven't double-checked this yet

```
1 - Black
2  - Deep blue
3  - Medium green
4  - Dark red
5  - Light red
6  - Bright red
7  - Dark red
8  - Dark orange
9  - Orange
10 - Yellow
11 - Dark yellow
12 - Brown
13 - Bright green
14 - Muted green
15 - Dark green
16 - Deep green
17 - Cyan blue
18 - Light blue
19 - Royal blue
20 - Indigo
21 - Purple
22 - Violet
23 - Magenta
24 - Dark pink
25 - Maroon
26 - Light gray
27 - Dark gray
28 - Light orange
29 - Tan
30 - Blue gray
31 - Lavender
32 - Olive gray
```