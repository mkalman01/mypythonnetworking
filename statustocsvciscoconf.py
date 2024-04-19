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

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=show_interface_status)

# Iterate through each host and print the results
for host, host_data in result.items():
    print(f"Results for {host}:")
    for interface in host_data.result:  # Use host_data.result instead of host_data["interface_status"]
        # Print the entire interface object to inspect its structure
        print(interface)
        # Assuming 'interface' is a dictionary with keys like 'interface' and 'status'
        print(f"Interface: {interface['interface']}, Status: {interface['status']}")
