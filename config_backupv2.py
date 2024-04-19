from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file
from datetime import datetime 
from nornir.core.connections.connection import ConnectionOptions
import os

nr = InitNornir(config_file="config.yaml")
backup_dir = "/home/sysadmin/Documents/backupconfig"

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def backup_config(task):
    command = "show running-config"
    connection_settings = task.host.get_connection_parameters("netmiko")
    extras = connection_settings.get("extras", {})
    if isinstance(extras, ConnectionOptions):
        if extras.secret:
            connection_settings.secret = extras.secret
        elif extras.enable_password:
            print(f"Using enable password for {task.host.name}.")
            connection_settings.secret = extras.enable_password
        else:
            print(f"No enable password or secret specified for {task.host.name}.")
    elif isinstance(extras, dict):
        if extras.get("secret", None):
            connection_settings["secret"] = extras["secret"]
        elif extras.get("enable_password", None):
            print(f"Using enable password for {task.host.name}.")
            connection_settings["secret"] = extras["enable_password"]
        else:
            print(f"No enable password or secret specified for {task.host.name}.")
    else:
        print(f"Unrecognized extras object for {task.host.name}.")
    print(f"Connection settings for {task.host.name}: {connection_settings}")
    config = task.run(task=netmiko_send_command, command_string=command, **connection_settings)
    if not config.result:
        print(f"Failed to retrieve config for {task.host.name}.")
        return
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{task.host.name}_{timestamp}_running_config.txt"
    filepath = os.path.join(backup_dir, filename)
    try:
        task.run(task=write_file, filename=filepath, content=config.result)
        print(f"Backup completed for {task.host.name}.")
    except Exception as e:
        print(f"Failed to write file for {task.host.name}: {e}")

result = nr.run(task=backup_config)
if result.failed:
    print("Failed to backup the following hosts:")
    for host, task_result in result.items():
        if task_result.failed:
            print(f"- {host}: {task_result.exception}")
print("Backup finished.")