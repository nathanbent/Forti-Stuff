# Forti-Stuff

> FortiScripts to make my FortiLife easier (sometimes)

## The Premise
I've been spending more time in the FortiGate CLI during deployments and migrations, and have been creating scripts to help with this process.

## The Stuff
These are fairly basic scripts to take a large input set and output them into FortiOS compatible format.

### Scripts
- Named lists to FortiOS (`named-list-2-fortios.py`)
- Bulk lists to be automatically named (`address-list-2-fortios.py`)
- Bulk webfilter URL import named (`webfilter-2-fortios.py`)
More coming soon!

## How to use
- The python scripts generally take a input.txt and make an output.txt
- An input.txt.sample is provided to show how to format the input.txt
- These are mostly to help bulk import IPs and FQDNs from copy/paste stuff