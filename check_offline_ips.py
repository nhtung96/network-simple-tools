import subprocess
import json

networks = {
    "network-name": "network-subnet",
    "abc": "192.168.1",
}

JSON_FILE = "offline_ips.json"
TEXT_FILE = "offline_ips.txt"

offline_data = {}

for network_name, network_prefix in networks.items():
    print(f"Checking network: {network_name} ({network_prefix}.0/24)")
    for host in range(2, 255):  
        ip = f"{network_prefix}.{host}"
        result = subprocess.run(
            ["arping", "-c", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:  
            print(f"{ip} (Unreachable)")
            if network_name not in offline_data:
                offline_data[network_name] = []
            offline_data[network_name].append(ip)


with open(JSON_FILE, "w") as json_file:
    json.dump(offline_data, json_file, indent=4)


with open(TEXT_FILE, "w") as text_file:
    for network_name, ips in offline_data.items():
        text_file.write(f"{network_name}:\n")
        text_file.write("\n".join(ips))
        text_file.write("\n\n")

print(f"Offline IPs logged in {JSON_FILE} and {TEXT_FILE}")
