from nornir import InitNornir
from nornir_scrapli.tasks import send_command, save_config
from nornir_utils.plugins.functions import print_result
import os
import datetime

backup_dir = "/home/sysadmin/Documents/backupconfig/"

nr = InitNornir(config_file="config.yaml")

def backup_config(task):
    r = task.run(task=send_command, command_string="show running-config")
    config = r.result
    task.run(
        task=save_config,
        filename=f"{backup_dir}/{task.host}_config_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.txt",
        config=config,
    )

result = nr.run(task=backup_config)
print_result(result)

print ("Backup is done")

