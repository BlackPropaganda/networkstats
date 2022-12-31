import ipaddress


# checks if IP to send to shodan is private or public
def is_public_ip(ip_v4):
    ip = ipaddress.IPv4Address(ip_v4)
    # returning true if public, false for private

    # false if multicast IP destination
    first_octet = ip_v4.split(".")[0]
    if 224 <= int(first_octet) <= 239:
        return False

    return not ip.is_private


class Host:
    def __init__(self, ip, mac):
        self.ip_addr = ip
        self.mac = mac
        self.bytes_tx = 0
        self.raw_intel = None
        self.intel_ = None

    def __str__(self):
        return f"{self.ip_addr} : {self.mac}"

    def __eq__(self, other):
        return self.ip_addr == other.ip_addr
