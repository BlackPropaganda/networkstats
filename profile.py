import datetime
import dpkt
from dpkt.utils import mac_to_str, inet_to_str

from core.cache import Cache
from core.connection import Connection


def parse_connections(pcap):
    """Print out information about each packet in a pcap
       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """

    # list of connections
    connection_list = []

    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            # non-IP packet
            # print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
            continue

        # Now grab the data within the Ethernet frame (the IP packet)
        ip = eth.data

        # Check for TCP in the transport layer
        if isinstance(ip.data, dpkt.tcp.TCP) or isinstance(ip.data, dpkt.udp.UDP):
            # Set the TCP data
            tcp = ip.data
            # Now see if we can parse the contents as an HTTP request
            # try:
            #     request = dpkt.http.Request(tcp.data)
            # except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
            #     continue

            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            # do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            # more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            # fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

            # Print out the info
            # print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
            # print('Ethernet Frame: ', mac_to_str(eth.src), mac_to_str(eth.dst), eth.type)
            # print('IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)' %
            #     (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))
            # print('HTTP request: %s\n' % repr(request))

            # adding source and destination port for tcp/udp connections

            src_port = None
            dst_port = None

            protocol = ""
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                protocol = "tcp"

            if ip.p == dpkt.ip.IP_PROTO_UDP:
                protocol = "udp"

            src_port = ip.data.sport
            dst_port = ip.data.dport

            # adding connection with information from example
            # source mac and ip, destination mac and ip, and time are logged.
            src_ip = inet_to_str(ip.src)
            dst_ip = inet_to_str(ip.dst)
            src_mac = mac_to_str(eth.src)
            dst_mac = mac_to_str(eth.dst)

            time = str(datetime.datetime.utcfromtimestamp(timestamp))
            length = ip.len
            # conn = Connection(src_ip, dst_ip, src_mac, dst_mac, time, length, src_port, dst_port)
            # print(conn)
            connection_list.append(
                Connection(src_ip, dst_ip, src_mac, dst_mac, time, length, src_port, dst_port, protocol)
            )

            # # Check for Header spanning across TCP segments
            # if not ip.data.endswith(b'\r\n'):
            #     # print('\nHEADER TRUNCATED! Reassemble TCP segments!\n')
            #     no = None
    return connection_list


def get_connections(file):
    """Open up a test pcap file and print out the packets"""
    with open(file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        return parse_connections(pcap)


if __name__ == '__main__':
    pcap_cache = Cache(get_connections("data/pcap/test2.pcap"), config="config.json")
    pcap_cache.collect_hosts()
    # print packet statistics (protocol breakdown)
    #
    # for x in pcap_cache.dst_port_stats():
    #     print(x)
    #

    intel = pcap_cache.compile_intel()
    for insight in intel:
        print(insight)
