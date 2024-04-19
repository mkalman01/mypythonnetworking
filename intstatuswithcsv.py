import csv
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from ciscoconfparse import CiscoConfParse

def parse_interface_status(output):
    parse = CiscoConfParse(output.splitlines())
    interfaces = parse.find_objects(r'^interface')
    result = []
    for interface in interfaces:
        status = interface.re_search_children(r'shut|notconnect|monitoring|disabled')
        if status:
            result.append({
                'interface': interface.text.strip().split()[-1],
                'status': status[0].text.strip(),
                # Add other relevant information as needed
            })
    return result

def show_interface_status(task):
    r = task.run(task=netmiko_send_command, command_string="show interface status")
    task.host["interface_status"] = parse_interface_status(r.result)
    return r

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")

# Run the show_interface_status task
result = nr.run(task=show_interface_status)

# Write the output to a CSV file
csv_file_path = "interface_status_output.csv"
with open(csv_file_path, "w", newline="") as csvfile:
    fieldnames = ["host", "interface", "status"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data
    for host, host_data in result.items():
        for interface_result in host_data.result.result:
            # Check if the interface_result is a dictionary
            if isinstance(interface_result, dict):
                writer.writerow({
                    "host": host,
                    "interface": interface_result.get("interface", ""),
                    "status": interface_result.get("status", "")
                })
            else:
                # Print the invalid result for further inspection
                print(f"Skipping invalid interface result: {interface_result}")

print(f"Results written to {csv_file_path}")