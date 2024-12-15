import icmplib
from .colors import colors as c

class Host(object):

    def __init__(self, address, name=None, group=None):

        self.name = name if name is not None else address
        self.group = group
        self.hostname = None
        self.ips = []

        self.resolve_error = None
        self.up = None
        self.rtt = 0

        if icmplib.is_hostname(address):
            self.hostname = address
            try:
                self.ips = icmplib.resolve(address)
                self.resolve_error = False
            except icmplib.exceptions.NameLookupError as e:
                self.resolve_error = True
        elif icmplib.is_ipv4_address(address):
            self.ips = [address]
        elif icmplib.is_ipv6_address(address):
            self.ips = [address]
        else:
            raise ValueError("address not identified as hostname or ip address")

    def get_address(self):
        address = self.hostname if self.hostname is not None else self.ips[0]
        return address

    def table_list(self):
        """
        Return a list the formated stats that will be printed in the table in
        order. This is:
        * Name
        * Status
        * Ping time (rtt)
        """

        up = f"{c.Green}Up{c.NoC}"
        down = f"{c.Red}down{c.NoC}"

        if self.resolve_error:
            status = f"{c.Red}DNS error{c.NoC}"
        else:
            status = f"{up if self.up else down}"
        rtt = None if self.rtt == 0 else f"{self.rtt} ms"

        return([self.name, status, rtt])

    def ping_test(self, count=4, interval=1, timeout=5):
        address = self.get_address()
        try:
            details = icmplib.ping(
                address,
                count=count,
                interval=interval,
                timeout=timeout,
                privileged=False,
            )
            self.up = details.is_alive
            self.rtt = details.avg_rtt
        except icmplib.exceptions.NameLookupError:
            self.resolve_error = True


