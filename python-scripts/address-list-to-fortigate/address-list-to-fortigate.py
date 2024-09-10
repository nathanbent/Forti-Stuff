def generate_fortigate_addresses(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for index, ip in enumerate(infile, start=1):
            ip = ip.strip()
            if ip:  # Make sure the line is not empty
                outfile.write(f"edit XXX-{index}\n")
                outfile.write(f"set subnet {ip}/32\n")
                outfile.write("next\n\n")

if __name__ == "__main__":
    input_file = "input.txt"  # Replace with your input filename
    output_file = "output.txt"  # Replace with your desired output filename
    generate_fortigate_addresses(input_file, output_file)
    print(f"FortiGate configuration saved to {output_file}")
