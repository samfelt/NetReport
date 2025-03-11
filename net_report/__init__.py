import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from .args import parse_args
from .config import load_config, valid_config, verify_config
from .host import Host
from .results import print_group_table
from .colors import colors as c

import time

__prog__ = "NetReport"
__version__ = "0.0.3"


def run():
    """
    Main Function
    """

    args = parse_args(sys.argv[1:])

    if args.version:
        print(f"{__prog__} v{__version__}")
        return 0

    config = load_config()
    if args.check_config:
        errors = verify_config(config)
        if len(errors) == 0:
            print("config file passed check")
            return 0
        else:
            print(f"config file contains {len(errors)} errors:")
            print("------------------------------")
            for error in errors:
                print(error)
            return -1

    if not args.skip_config_check and not valid_config(config):
        print("There is a problem with the config file")
        print("Run with '--check-config' to see errors")
        return -1

    settings = config["settings"]

    all_hosts = [ Host(host["address"], host["name"], host["group"], host["ports"]) for host in config["hosts"] ]
    quick_hosts = [ host for host in all_hosts if host.group == settings["quick_group"] ]
    hosts = []

    if settings["skip_quick"]:
        hosts = list(set(all_hosts) - set(quick_hosts))

    if args.quick:
        hosts = quick_hosts

    # Run pings
    with ThreadPoolExecutor(
        max_workers=settings["max_threads"],
        thread_name_prefix="NetRepThread"
    ) as pool:

        futures = {}
        for h in hosts:
            ping_future = pool.submit(h.ping_test, settings["ping_packets"], 0.3, settings["ping_timeout"])
            port_future = pool.submit(h.port_test, h.ports_to_test, 2)
            futures[h] = {
                "ping": ping_future,
                "port": port_future,
            }
        ping_futures = [future["ping"] for future in futures.values()]
        port_futures = [future["port"] for future in futures.values()]
        all_futures = ping_futures + port_futures

        print(f"\033[s", end="", flush=True)
        clear = f"\033[K"
        while not all([future.done() for future in all_futures]):
            pings_done = [f.done() for f in ping_futures].count(True)
            ports_done = [f.done() for f in port_futures].count(True)
            print(f"\033[u", end="", flush=True)
            print(f"{clear}({pings_done}/{len(ping_futures)}) Ping tests")
            print(f"{clear}({ports_done}/{len(port_futures)}) Port tests")
            time.sleep(0.5)
        print(f"\033[u", end="", flush=True)

    groups = {}
    for host in hosts:
        group = "No Group" if host.group is None else host.group
        if group in groups.keys():
            groups[group].append(host)
        else:
            groups[group] = [host]

    for group_name, hosts in groups.items():
        print_group_table(group_name , [ host.table_list() for host in hosts ])
        print()

if __name__ == "__main__":
    exit(run())
