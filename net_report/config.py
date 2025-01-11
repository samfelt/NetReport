import os
import pathlib
import json

_sections = sorted(["groups", "hosts", "settings"])
_host_keys= sorted(["address", "name", "group", "ping", "ports"])
_settings=sorted(["quick_test", "max_threads", "ping_packets", "ping_timeout"])
_default_config = {
    "groups" : [
        "Default"
    ],
    "hosts" : [
        {
            "address" : "www.google.com",
            "group": "Default",
            "name" : "Google",
            "ping" : True,
            "ports" : [],
        },
        {
            "address" : "www.amazon.com",
            "group": "Default",
            "name" : "Amazon",
            "ping" : True,
            "ports" : [],
        },
        {
            "address" : "1.1.1.1",
            "group": "Default",
            "name" : "Cloudflare",
            "ping" : True,
            "ports" : [],
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
            json.dump(_default_config, file, )
        print(f"Wrote default config at '{config_path}'")
    config = json.load(open(config_path))
    return config

def valid_config(config):
    """After reading the config into a dictionary, check if there are any
    errors with the config. If any are found, return False
    """

    if verify_config(config, return_on_first=True) == []:
        return True
    return False

def _verify_groups(config, return_on_first=False):
    """Verify the groups section of the config."""

    errors = []
    if not isinstance(config, list):
        errors.append("'groups' section must contain a list")
        return errors
    if not all(isinstance(group, str) for group in config):
        errors.append("Each group must be a string")
        if return_on_first: return errors
    return errors


def _verify_hosts(config, return_on_first=False):
    """Verify the hosts section of the config"""

    errors = []
    if not isinstance(config, list):
        errors.append("'hosts' section must contain a list")
        return errors

    for host in config:
        if sorted(host.keys()) != _host_keys:
            name = host.get("name", "UNKOWN")
            errors.append(f"host '{name}' does not have the correct parameters: {_host_keys}")
            if return_on_first: return errors

    return errors


def _verify_settings(config, return_on_first=False):
    """Verify the groups section of the config"""

    errors = []
    if not isinstance(config, dict):
        errors.append("'hosts' section must contain a list")
        return errors
    if sorted(config.keys()) != _settings:
        errors.append(f"Too many or not enough settings, required are: {_settings}")
        if return_on_first: return errors
    return errors

def verify_config(config, return_on_first=False):
    """Verify the config. For each error found, append the line number and
    description of the error to a list, then return the list of all the errors.
    If 'return_on_first' is set to True, return once a single error is found.
    """

    section_verifiers = {
        "groups" : _verify_groups,
        "hosts" : _verify_hosts,
        "settings" : _verify_settings,
    }

    errors = []
    sections_verified = []

    for section in config.keys():
        if section in section_verifiers.keys():
            section_errors = section_verifiers[section](config[section], return_on_first)
            errors.extend(section_errors)
            sections_verified.append(section)
            if return_on_first and len(errors): return errors
        else:
            errors.append(f"Additional section found, '{section}'")
            if return_on_first: return errors

    missing_sections = set(section_verifiers.keys()) - set(sections_verified)
    if len(missing_sections) != 0:
        errors.append(f"Missing sections: {missing_sections}")
        if return_on_first: return errors

    return errors

