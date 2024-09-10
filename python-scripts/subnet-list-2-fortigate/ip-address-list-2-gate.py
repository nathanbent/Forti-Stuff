def format_ip_list(input_file, output_file):
    # Open and read the input file
    with open(input_file, 'r') as infile:
        ip_list = infile.read()

    # Split the input into individual entries by splitting on newlines
    entries = ip_list.strip().split('\n\n')

    # Open the output file for writing
    with open(output_file, 'w') as outfile:
        for entry in entries:
            # Split each entry into name and IP/Subnet part
            lines = entry.split('\n')
            if len(lines) >= 2:
                name = lines[0].strip('* ')
                ip_subnet = lines[1].strip()

                # Write the formatted output for each entry with the name in quotes
                outfile.write(f'edit "{name}"\n')
                outfile.write(f"set subnet {ip_subnet}\n")
                outfile.write("next\n\n")
            else:
                print(f"Skipping incomplete entry: {entry}")

# Call the function with the input and output file names
format_ip_list('input.txt', 'output.txt')
