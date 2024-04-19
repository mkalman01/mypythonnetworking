from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from datetime import datetime   
import os

nr = InitNornir(config_file="config.yaml")
backup_dir = "/home/sysadmin/Documents/backupconfig/"

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def backup_config(task):
    command = "show running-config"
    config = task.run(task=netmiko_send_command, command_string=command)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{task.host.name}_{timestamp}_running_config.txt"
    filepath = os.path.join(backup_dir, filename)
    task.run(task=write_file, filename=filepath, content=config.result)
    print(f"Backup completed for {task.host.name}.")

result = nr.run(task=backup_config)
#print_result(result)
print("Backup finished.")