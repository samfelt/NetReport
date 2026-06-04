import sys
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from rich import box
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn, TimeElapsedColumn
from rich.table import Table
from . import __prog__, __version__
from .args import parse_args
from .config import load_config, valid_config, verify_config
from .host import Host
from .results import print_group_table
from .colors import colors as c

import time

console=Console()

def run():
    """
    Main Function
    """

    args = parse_args(sys.argv[1:])

    if args.version:
        print(f"{__prog__} v{__version__}")
        return 0

    # Verify Config File
    config = load_config()
    if args.check_config:
        errors = verify_config(config)
        if len(errors) == 0:
            console.print(":white_heavy_check_mark: Config file passed check")
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

    # Check if current user is able to ping
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
        test_socket.close()
    except PermissionError:
        print("WARNING: Current user can't open ICMP socket")
        print("         Add gid to net.ipv4.ping_group_range")

    settings = config["settings"]

    all_hosts = [
        Host(
            host["address"],
            host["name"],
            host["group"],
            host["ports"]
        ) for host in config["hosts"]
    ]

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

        # Create Futures
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

        # Set up progress bars
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        progress.start()
        ping_tests = progress.add_task("[green]Ping Tests...", total=len(ping_futures))
        port_tests = progress.add_task("[blue]Port Tests...", total=len(ping_futures))

        # Start tests
        i = 0
        while not all([future.done() for future in all_futures]):
            pings_done = [f.done() for f in ping_futures].count(True)
            ports_done = [f.done() for f in port_futures].count(True)

            progress.update(ping_tests, completed=pings_done)
            progress.update(port_tests, completed=ports_done)
            i += 1
            time.sleep(0.1)

        #Stop Progress
        pings_done = [f.done() for f in ping_futures].count(True)
        ports_done = [f.done() for f in port_futures].count(True)
        progress.update(ping_tests, completed=pings_done)
        progress.update(port_tests, completed=ports_done)
        progress.stop()

    # Print final table, rich table later
    groups = {}
    for host in hosts:
        group = "No Group" if host.group is None else host.group
        if group in groups.keys():
            groups[group].append(host)
        else:
            groups[group] = [host]

    for group_name, group_hosts in groups.items():
        table = Table(box=box.SIMPLE, row_styles=["none", "none"])
        table.add_column(group_name , style="cyan")
        table.add_column("Status")
        table.add_column("Ping")
        table.add_column("Port Scan")

        for host in group_hosts:
            if host.resolve_error:
                state = "[red]DNS error"
            else:
                state = f"{'[green]Up' if host.up else '[red]Down'}"
            rtt = None if host.rtt == 0 else f"{int(host.rtt)} ms"

            ports = ""
            for port, status in host.ports.items():
                if status:
                    ports += f"[green]{port}, "
                else:
                    ports += f"[red]{port}, "
            ports = ports[:-2]

#            import ipdb;ipdb.set_trace()
            table.add_row(host.name, state, rtt, ports)
        console.print(table)
        print()

#    import ipdb;ipdb.set_trace()
"""
    for group_name, hosts in groups.items():
        print_group_table(group_name , [ host.table_list() for host in hosts ])
        print()
"""

if __name__ == "__main__":
    exit(run())
