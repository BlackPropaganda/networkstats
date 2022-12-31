import json

from core.host import Host, is_public_ip
from core.connection import get_proto_spec
from core.shodan_data.interface import Interface
from core.intel import Intel


class Cache:
    def __init__(self, connection_list, config="configs.json"):
        with open(config, "r") as config_file:
            self.configs = json.load(config_file)

        self.connection_list = connection_list
        self.host_list = []
        self.internet_host_list = []
        self.intel_list = []
        self.api = Interface(config)
        self.tx_stats = []
        self.dst_port_list = []
        self.dst_port_statistics = []

    # collects host and gathers intel
    def collect_hosts(self):
        for conn in self.connection_list:
            # print(conn)
            # enter source host ip and mac
            src_ip = conn.src_ip
            src_mac = conn.src_mac

            src_host = Host(src_ip, src_mac)
            # if source host does not already exist in cache list
            if not self.host_list.__contains__(src_host):
                # if public, run shodan
                # print("===================")
                # print(is_public_ip(src_ip))
                # print(self.internet_host_list.__contains__(src_host))
                # print("===================")
                if is_public_ip(src_ip) and not self.internet_host_list.__contains__(src_host):
                    # print(src_host)
                    results = self.api.host_search(src_ip)
                    src_host.raw_intel = results
                    self.internet_host_list.append(src_host)
                self.host_list.append(
                    src_host
                )
                # print(src_host)

            # enter destination host ip and mac
            dst_ip = conn.dst_ip
            dst_mac = conn.dst_mac

            dst_host = Host(dst_ip, dst_mac)
            # if destination host does not already exist in cache list
            if not self.host_list.__contains__(dst_host):
                if is_public_ip(dst_ip) and not self.internet_host_list.__contains__(dst_host):
                    results = self.api.host_search(dst_ip)
                    dst_host.raw_intel = results
                    self.internet_host_list.append(dst_host)

                self.host_list.append(
                    dst_host
                )
                # print(dst_host)

    def dst_port_stats(self):
        # parallel array for destination ports
        num_dst_ports = []
        for conn in self.connection_list:
            if conn.dst_port <= 1024 and not self.dst_port_list.__contains__(conn.dst_port):
                self.dst_port_list.append(conn.dst_port)
                num_dst_ports.append(1)
            elif conn.dst_port <= 1024 and self.dst_port_list.__contains__(conn.dst_port):
                index = self.dst_port_list.index(conn.dst_port)
                num_dst_ports[index] += 1

        counter = 0
        for x in self.dst_port_list:
            # print(f"{x} : {num_dst_ports[counter]}")
            self.dst_port_statistics.append(
                [get_proto_spec(x), num_dst_ports[counter]]
            )
            counter += 1
        return self.dst_port_statistics

    def compile_intel(self):
        for host in self.internet_host_list:
            if host.raw_intel is not None:
                self.intel_list.append(
                    Intel(host, host.raw_intel)
                )
        return self.intel_list

    def write_intel(self):
        pass
