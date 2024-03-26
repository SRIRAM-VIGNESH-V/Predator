# Predator
Networks Forensic tool for sniffing network traffic with Python for live capture observation or PCAP creation and analysis.


# Predator Modes of Operation: Live, Read, Write
**NOTE**: Read and write modes were not created to handle large PCAP files but rather for parsing and creating small PCAP files. It large files file are used, memory overflow exceptions will be raised. Live mode does not have this limitation. 

### Live Mode
**Usage**:
```
  -live, --live-mode    Perfrom live capture analysis
  -i [INTERF [INTERF ...]], --interf [INTERF [INTERF ...]]
                        The interface to listen on (more than one is allowed)
  -c <NUM>, --count <NUM>
                        The number of packets to capture (default = 0 = infinity)
  -f <BPF FITLER>, --filter <BPF FITLER>
                        Berkeley packet filter to apply to capture
```

### Read Mode
**Usage**:
```
  -read, --read-mode    Read a PCAP file for analysis
  -r <FILENAME>, --rfile <FILENAME>
                        name of PCAP file to read for parsing
  -rc <NUM>, --read-count <NUM>
                        number of packets to read from pcap file
  -hex, --hex-dump      Print out the hex dump of each packet along with packet flow summary
  -pc, --packet-count   Prints the number of the packets within a PCAP file
  -no-prn, --no-print   Do not print out traffic flow output to console
  -src-ip-cnt <IP> [<IP> ...], --source-ip-count <IP> [<IP> ...]
                        Prints the number of times an IP address was the source IP. Multiple IP addresses can be specified
  -dst-ip-cnt <IP> [<IP> ...], --destination-ip-count <IP> [<IP> ...]
                        Prints the number of times an IP addresses was the destination IP. Multiple IP addresses can be specified
  -ip-cnt <IP> [<IP> ...], --ip-count <IP> [<IP> ...]
                        Prints the number of times an IP address was the source or destination IP. Multiple IP addresses can be specified
  -ts <HOUR:MINUTE>, --time-start <HOUR:MINUTE>
                        Filter for packets that start from the specified hour:minute value and onwards
  -te <HOUR:MINUTE>, --time-end <HOUR:MINUTE>
                        Filter for packets whose hour:minute value does not go beyond the specified hour:minute value provided
  -tr <HOUR:MINUTE> [<HOUR:MINUTE> ...], --time-range <HOUR:MINUTE> [<HOUR:MINUTE> ...]
                        Filter for packets whose hour:minute value falls inbetween the desired time range
```


### Write Mode
The arguments provided by the Live mode should be used with Write mode as capturing packets requires packet sniffing.

**Usage**:
```
  -write, --write-mode  capture live traffic and write to PCAP file (must
                        specify `-c` option)
  -w <FILENAME>, --wfile <FILENAME>
                        name of PCAP file to create
```

### Read/Write Mode
Most arguments can be used for both Read & Write modes:
```
  -src-ip <IP>, --source-ip <IP>
                        Filter packets based on a specified source IP address
  -not-src-ip <IP>, --not-source-ip <IP>
                        Filter packets that do not contain the specified source IP address
  -dst-ip <IP>, --destination-ip <IP>
                        Filter packets based on a specified destination IP address
  -not-dst-ip <IP>, --not-destination-ip <IP>
                        Filter packets that do not contain the specified destination IP address
  -src-port <PORT>, --source-port <PORT>
                        Filter packets based on a specified source port number
  -not-src-port <PORT>, --not-source-port <PORT>
                        Filter packets that do not contain the specified source port number
  -dst-port <PORT>, --destination-port <PORT>
                        Filter packets based on a specified destination port number
  -not-dst-port <PORT>, --not-destination-port <PORT>
                        Filter packets based on a specified destination port number
  -src-mac <MAC>, --source-mac <MAC>
                        Filter packets based on a specified source mac address
  -not-src-mac <MAC>, --not-source-mac <MAC>
                        Filter packets that do not contain the specified source mac address
  -dst-mac <MAC>, --destination-mac <MAC>
                        Filter packets based on a specified destination mac address
  -not-dst-mac <MAC>, --not-destination-mac <MAC>
                        Filter packets that do not contain the specified destination mac address
  -tcp, --filter-tcp    Filter TCP packets only
  -not-tcp, --not-filter-tcp
                        Filter for non-TCP packets only
  -udp, --filter-udp    Filter UDP packets only
  -not-udp, --not-filter-udp
                        Filter for non-UDP packets only
  -icmp, --filter-icmp  Filter ICMP packets only
  -not-icmp, --not-filter-icmp
                        Filter for non-ICMP packets only
  -arp, --filter-arp    Filter for ARP packets only
  -not-arp, --not-filter-arp
                        Filter for non-ARP packets only
  -dns, --filter-dns    Filter for DNS packets only
  -not-dns, --not-filter-dns
                        Filter for non-DNS packets only
  -tf <TCP FLAG> [<TCP FLAG> ...], --tcp-flags <TCP FLAG> [<TCP FLAG> ...]
                        Filter packets by TCP flag. Seperate each flag by spaces.
  -le <NUM>, --len-less-equal <NUM>
                        Filters for packets with a length that is less than or equal to the specified number
  -ge <NUM>, --len-greater-equal <NUM>
                        Filters for packets with a length that is greater than or equal to the specified number
  -len-eq <NUM>, --len-equal <NUM>
                        Filters for packets with a length that is equal to the specified number
  -ttl-eq <NUM>, --ttl-equal <NUM>
                        Filters for packets with a ttl that is equal to the specified number
  -sum, --summary       Summary of the packet capture <for read & write mode>
  -j <FILENAME>, --json <FILENAME>
                        Create JSON file containing capture summary (ip:count, port:count, mac:count)
```
## Berkeley Packet Filter Examples
Berkeley Packet Filter are for Predator's **Live** and **Write** mode of operation. Berkeley Packet Filters are recommended to filter for content relevant to the content that the user is seeking. Python is no where near as fast at C at parsing network packets so it wouldn't be effective to capture in Live or Write Mode without an appropiate BP filter. 
```
# Matching IP
-------------
dst host 192.168.1.0
src host 192.168.1
dst host 172.16
src host 10
host 192.168.1.0
host 192.168.1.0/24
src host 192.168.1/24

# Matching Port/Portranges
--------------------------
src port <PORT>
dst port <PORT>
port <PORT>
src portrange 80-88
tcp portrange 1501-1549

# Matching MAC
--------------
ether host <MAC>
ether src host <MAC>
ether dst host <MAC>
```
