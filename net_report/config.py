import os
import pathlib
import json

default_config = {
    "hosts" : [
        {
            "address" : "www.google.com",
            "group": "Default",
            "name" : "Google",
            "ping" : True
        },
        {
            "address" : "www.amazon.com",
            "group": "Default",
            "name" : "Amazon",
            "ping" : True
        },
        {
            "address" : "1.1.1.1",
            "group": "Default",
            "name" : "Cloudflare",
            "ping" : True
        }
    ],
    "settings": {
        "ping_packets": 5,
        "ping_timeout": 2,
        "max_threads": 10
    }
}

def load_config():
    config_file = "netreport.json"
    config_path = os.path.join(pathlib.Path.home(), ".config", config_file)

    if not os.path.exists(config_path):
        with open(config_path, "w") as file:
            json.dump(default_config, file, )
        print(f"Wrote default config at '{config_path}'")
    config = json.load(open(config_path))
    return config
