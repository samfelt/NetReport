# NetReport
Get a quick view of network info

## Allowing non-root users to create icmp sockets

```bash
#1000 is my user's group, setting to "0 2147483647" would allow everyone
sudo sysctl net.ipv4.ping_group_range="1000 1000"
```
