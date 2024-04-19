from fileinput import filename
from click import command
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import csv


#show interface task

def show_interface_status(task):
    r = task.run(task=netmiko_send_command, command_string="show interface status", use_textfsm=False)
    task.host["interface_status"] = r.result
    return r
nr = InitNornir(config_file="config.yaml", dry_run=True)
result = nr.run(task=show_interface_status)
print_result(result)

#write output to csv

for host, host_data in result.items():
    with open(f"{host}_interface_status.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["host", "interface", "status", "vlan", "duplex", "speed"])
        writer.writeheader()
        for host, host_data in result.items():
            for interface in host_data.result:
                writer.writerow({
                    "host": host,
                    "interface": interface["name"],
                    "status": interface["status"],
                    "vlan": interface["vlan"],
                    "duplex": interface["duplex"],
                    "speed": interface["speed"]
                })
