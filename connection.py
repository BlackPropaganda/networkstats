from socket import getservbyname, getservbyport
# >>> getservbyport(80)
# 'http'


def get_proto_spec(dst_port, proto=None):
    if proto is not None:
        return getservbyport(dst_port, proto)
    else:
        return getservbyport(dst_port)


class Connection:
    def __init__(self, src_ip, dst_ip, src_mac, dst_mac, time, bytes_tx, src_port, dst_port, protocol):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.time = time
        self.protocol = protocol
        self.bytes = bytes_tx
        self.proto_info = None
        if self.dst_port < 1024:
            self.proto_info = get_proto_spec(self.dst_port, proto=protocol)

    def __str__(self):
        return f"{self.src_ip} -> {self.dst_ip} || {self.src_mac} -> {self.dst_mac} || {self.protocol} : {self.src_port}, {self.dst_port}"
