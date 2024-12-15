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

    args = parser.parse_args(argv)
    return args
