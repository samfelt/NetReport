import icmplib
import socket
from contextlib import closing
from .colors import colors as c

class Host(object):

    def __init__(self, address, name=None, group=None, ports=[], resolve=False):

        self.given_address = address
        self.name = name if name is not None else address
        self.group = group

        self.hostname = None
        self.ips = []
        self.resolve_error = None

        self.up = None
        self.rtt = 0
        self.ports_to_test = ports
        self.ports = {}

        if resolve:
            self._resolve()

    def __repr__(self):
        return f"Host({self.name}<{self.hostname}><{self.ips[0]}>)"

    def _resolve(self):
        """Attempt to resolve the address given during initialization. The
        objects hostname will be set as 'hostname' and a list of ip addresses
        associated with that hostname will be put in ips. If a resolution error
        occurs, it will be put in 'resolve_error'
        """
        if icmplib.is_hostname(self.given_address):
            self.hostname = self.given_address
            try:
                self.ips = icmplib.resolve(self.given_address)
                self.resolve_error = False
            except icmplib.exceptions.NameLookupError as e:
                self.resolve_error = True
        elif icmplib.is_ipv4_address(self.given_address):
            self.ips = [self.given_address]
        elif icmplib.is_ipv6_address(self.given_address):
            self.ips = [self.given_address]
        else:
            raise ValueError("address not identified as hostname or ip address")


    def get_address(self):
        """Return the address of the host as a string. This will be the
        hostname or the first ip address. To ensure that one of these exists,
        run the resolve method if 'hostname' is still None
        """
        if self.hostname is None:
            self._resolve()

        address = self.hostname if self.hostname is not None else self.ips[0]
        return address

    def table_list(self):
        """Return a list the formated stats that will be printed in the table
        in order. This is: * Name * Status * Ping time (rtt)
        """

        up = f"{c.Green}Up{c.NoC}"
        down = f"{c.Red}down{c.NoC}"

        if self.resolve_error:
            status = f"{c.Red}DNS error{c.NoC}"
        else:
            status = f"{up if self.up else down}"
        rtt = None if self.rtt == 0 else f"{int(self.rtt)} ms"

        ports = ""
        for port, status in self.ports.items():
            if status:
                ports += f"{c.Green}{port}{c.NoC}, "
            else:
                ports += f"{c.Red}{port}{c.NoC}, "
        ports = ports[:-2]

        return([self.name, status, rtt, ports])

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

    def port_test(self, ports, timeout=10):
        """
        Check if the list of ports are open on the remote host. This is done
        indepedantly of the ping test (this will still run if the ping test
        fails) in the case that the remote server is not responding to ICMP
        packets.
        """

        address = self.get_address()
        for port in ports:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((address, port))
                if sock.connect_ex((address, port)):
                    self.ports[port] = True
                else:
                    self.ports[port] = False
