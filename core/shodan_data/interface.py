import shodan
import json
from time import sleep


class Interface:
    def __init__(self, config_file):
        with open(config_file) as configs:
            self.configs = json.load(configs)
            self.api_key = self.configs["shodan_api"]
            # control variable, to use or not to use shodan.
            self.search_hosts = self.configs["host_search"]
        self.api = shodan.Shodan(self.api_key)

    def host_search(self, ip_addr):
        print(f"Querying: {ip_addr}")
        # avoiding rate limiting
        sleep(1)
        if self.search_hosts:
            try:
                # data = self.api.host(ip_addr)
                # print("Interface:")
                # print(data)
                return self.api.host(ip_addr)
            except shodan.exception.APIError as e:
                print(f"Cannot lookup: {ip_addr}\n Error: {e}")
                return {"Error": "Not Found"}
        else:
            # print(f"querying: {ip_addr}")
            return None


"""
# host search return pattern
{
        'total': 8669969,
        'matches': [
                {
                        'data': 'HTTP/1.0 200 OK\r\nDate: Mon, 08 Nov 2010 05:09:59 GMT\r\nSer...',
                        'hostnames': ['pl4t1n.de'],
                        'ip': 3579573318,
                        'ip_str': '89.110.147.239',
                        'os': 'FreeBSD 4.4',
                        'port': 80,
                        'timestamp': '2014-01-15T05:49:56.283713'
                },
                ...
        ]
}
"""


if __name__ == '__main__':
    iface = Interface("../../config.json")
    # pretty = iface.host_search("8.8.8.8")
    # print(pretty)

    # for match in iface.host_search("8.8.8.8")['matches']:
    #     print("")

    # Lookup the host
    #  host = iface.host_search('8.8.8.8')
    # print(host)
