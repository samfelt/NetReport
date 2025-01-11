import argparse

def parse_args(argv=None):
    """
    Parse arguemtns given on the command line
    """

    description = "Give quick information about network devices"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--version", action="store_true", help="Print version info"
    )

    parser.add_argument(
        "--check-config", "-c", action="store_true", help="Check for any errors in the config file"
    )
    parser.add_argument(
        "--skip-config-check", "-s", action="store_true", help="Skip config verification, may lead to unhandled exceptions"
    )

    parser.add_argument(
        "--quick", "-q", action="store_true", help="Test the quick test category"
    )

    args = parser.parse_args(argv)
    return args
