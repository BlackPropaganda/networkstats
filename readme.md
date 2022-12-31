# networkstats
Python project with extends dpkt to dissect and analyse *.pcap files from tcpdump and wireshark for analysis and information gathering.

Wireshark is great for specific analysis on hosts, but sometimes networks at scale cannot be properly audited.
Something often slips through the cracks. This program goes packet by packet into wireshark and analyses ipv4
packets.

### Data Automatically Collected:
* Source
  * IP address
  * MAC address
  * Port
* Destination
  * IP address
  * MAC address
  * Port
* Packet Size
  * Enables Traffic volume analysis

### Data Not Collected
* Any protocol not TCP/UDP
  * DPKT currently only supports TCP/UDP IPV4
* Any IPv6 packet
  * DPKT doesn't support IPv6 (it can still retrieve this, however it is not analysed. More on this later.)

### Shodan API Implementation

The program also is coupled with shodan to enable quick public IP lookups.

The destination IPs are parsed, and checked to be public, non-multicast IPv4 Addresses.
To turn this feature on or off, see config.json, and host_lookup is either true, or false.

The information gathered from shodan is placed in memory into the host object as an Intel Object.

### Shodan Data Collected:

Public, non-multicast addresses (including but not limited to)
* Open Ports on host
* Organization name
* ISP
* Hostnames
* Domains
* Geospatial data
  * City
  * Country (name and two-digit code)
  * Latitude, Longitude

## Getting Started:
To use this extension, all you have to do is create a shodan account, then acquire your API key.
Once you have your API key, you can enter it into the config.json file. The program will automatically
use it upon running profile.py.