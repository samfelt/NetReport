from copy import deepcopy

# Valid Config
valid = {
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
        }
    ],
    "settings": {
        "quick_group": "Quick Test",
        "skip_quick": True,
        "ping_packets": 5,
        "ping_timeout": 2,
        "max_threads": 10
    }
}

# Extra section
extra_section = deepcopy(valid)
extra_section["New Section"] = {1:1, 2:2}
# Missing Groups Section
missing_groups = deepcopy(valid)
del missing_groups["groups"]

# Missing Hosts Section
missing_hosts = deepcopy(valid)
del missing_hosts["hosts"]

# Missing Settings Section
missing_settings = deepcopy(valid)
del missing_settings["settings"]

# groups is not a list 
groups_not_list = deepcopy(valid)
groups_not_list["groups"] = True

# Individual group not a string
group_not_str = deepcopy(valid)
group_not_str["groups"] = ["Default", 1, "Test"]

# hosts is not a list 
hosts_not_list = deepcopy(valid)
hosts_not_list["hosts"] = True

# Host has missing keys 
host_missing_fields = deepcopy(valid)
host_missing_fields["hosts"].append({"a": 1, "b": 2})
host_missing_fields["hosts"].append({"a": 1, "b": 2})

# settings is not a list 
settings_not_list = deepcopy(valid)
settings_not_list["settings"] = True

# Host has missing keys 
settings_wrong_fields = deepcopy(valid)
settings_wrong_fields["settings"]["new"] = True

