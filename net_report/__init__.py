import sys
from .args import parse_args
from .config import load_config
from .host import Host
from .results import print_group_table
from .colors import colors as c

__prog__ = "NetReport"
__version__ = "0.0.3"

def main():
    """
    Main Function
    """

    args = parse_args(sys.argv[1:])

    if args.version:
        print(f"{__prog__} v{__version__}")
        return 0

    config = load_config()

    settings = config["settings"]

    hosts = [ Host(host["address"], host["name"], host["group"], host["ports"]) for host in config["hosts"] ]

    if args.quick:
        hosts = [ host for host in hosts if host.group == settings["quick_test"] ]

    # Run pings
    clear = f"\r\033[K\r"
    for i, host in enumerate(hosts):
        print(f"{clear}({i+1}/{len(hosts)}) | Pinging {c.Bold}{host.name}{c.NoC} ({host.get_address()})...",
              end="", flush=True)
        host.ping_test(settings["ping_packets"], 0.3, settings["ping_timeout"])
    print(clear, end="", flush=True)

    # Run ports
    for i, host in enumerate(hosts):
        print(f"{clear}({i+1}/{len(hosts)}) | Scanning ports {c.Bold}{host.name}{c.NoC} ({host.get_address()})...",
              end="", flush=True)
        host.port_test(host.ports_to_test, 2)
    print(clear, end="", flush=True)

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

#    import ipdb;ipdb.set_trace()

if __name__ == "__main__":
    exit(main())
