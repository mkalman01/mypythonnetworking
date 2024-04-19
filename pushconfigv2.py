from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result, print_title

nr = InitNornir(config_file="config.yaml")

with open("push.txt", "r") as f:
    config_commands = f.read()

result = nr.run(task=netmiko_send_config, config_commands=config_commands)

print_title("Deploying config")
print_result(result)

