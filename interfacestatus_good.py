from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
import csv

def show_interface_status(task):
    command_output = task.run(task=netmiko_send_command, command_string = "show interface status", use_textfsm=False)
    task.host["interface_status"] = command_output.result

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=show_interface_status)

status_counts = {"connected": 0, "notconnect": 0, "disabled": 0 }
for host, host_data in result.items():
    for line in host_data.result.splitlines():
        fields = line.split()
        if len(fields) > 1 and fields[1] in status_counts:
            status_counts[fields[1]] += 1

with open("interface_status_counters.csv", "w", newline="") as f:
    writer = csv.writer
    writer.writerow(["status", "count"])
    for status, count in status_counts.items():
        writer.writerow([status, count])
