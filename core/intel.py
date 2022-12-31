from socket import getservbyport

from core.geo.location import Location


class Intel:
    def __init__(self, host_, raw_intel):
        try:
            self.host_ = host_
            self.os_ = raw_intel.get("os")
            self.org = raw_intel.get("org")
            self.isp = raw_intel.get("isp")
            self.domains = raw_intel.get("domains")
            self.host_names = raw_intel.get("hostnames")
            self.location = Location(self.host_.ip_addr, raw_intel)
            self.ports = raw_intel.get("ports")
            self.ports_human = []

            # get service names for ports
            for port in self.ports:
                if port is not None:
                    try:
                        self.ports_human.append(getservbyport(port))
                    except OSError:
                        # port not found
                        self.ports_human.append("UNK")

        except KeyError:
            self.host_ = host_
            self.os_ = "N/A"
            self.org = "N/A"
            self.isp = "N/A"
            self.domains = "N/A"
            self.host_names = "N/A"
            self.location = Location(self.host_.ip_addr, raw_intel)
            self.ports = "N/A"

    def report(self):
        return f"" \
               f"{self.host_}\n" \
               f"{self.os_}\n" \
               f"{self.ports}\n" \
               f"{self.ports_human}\n" \
               f"{self.org}\n" \
               f"{self.host_names}\n" \
               f"{self.domains}\n" \
               f"{self.isp}\n" \
               f"{self.location}\n" \
                "===================="

    def to_dict(self):
        return {
            "host": f"{self.host_}",
            "os": f"{self.os_}",
            "ports": f"{self.ports}",
            "org": f"{self.org}",
            "hostnames": f"{self.domains}",
            "domains": f"{self.domains}",
            "isp": f"{self.isp}",
            "location": f"{self.location.to_dict()}"
        }

    def __str__(self):
        return f"{self.host_} : {self.os_} : {self.ports} : {self.ports_human} : {self.org} \n\t{self.location}"
