from nornir.plugins.tasks import networking
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir import InitNornir

BACKUP_PATH="./Documents/configs"

def backup_config(task, path):
    r = task.run(task=networking.napalm_get, getters=["config"])
    task.run(
        task=write_file,
        content=r.result["config"]["running"],
        filename=f"{path}/{task.host}.txt",
        )

nr = InitNornir(config_file="./config.yaml")


devices = nr.filter(role="switch")

result = devices.run(
    name="Backup Devices configurations", path=BACKUP_PATH, task=backup_config
)
print_result(result, vars=["stdout"])