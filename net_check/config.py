import os
import json


def load_config(filename="config.json"):
    config_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, filename)
    )
    config = json.load(open(config_file))
    return config
