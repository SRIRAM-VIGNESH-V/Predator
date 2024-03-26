from collections import Counter
from colored import fg, attr
from json import dump
from sys import exit
from re import search
from scapy.all import *
from random import randint
from prettytable import PrettyTable
from src.net_sniff import NetSniff

class PCAPParser(NetSniff):
    def __init__(self):
        self.filtered_packets = []

    def __init__(self):
        super().__init__(None, None , None, None)
        
    def filt_src_ip(self, capture, src_ip):
        """ Filter source IP addresses from capture 
        Args:
            capture (scapy.plist.PacketList): scapy packet capture
            src_ip (str): target source IP address to filter for        
        """
        try:
            src_ip = search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", src_ip).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-src-ip` MUST BE A VALID IP ADDRESSES"
                % (fg(9), attr(0))
            )
            exit(1)
        for pkt in capture:
            if pkt.haslayer(IP) and pkt[IP].src == src_ip:
                self.filtered_packets.append(pkt)
        return self.filtered_packets
    
    def filt_not_src_ip(self, capture, src_ip):
        """ Filter source IP addresses from capture that do not match `src_ip`
        Args:
            capture (scapy.plist.PacketList): scapy packet capture
            src_ip (str): target source IP address to not filter for        
        """
        try:
            src_ip = search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", src_ip).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-not-src-ip` MUST BE A VALID IP ADDRESSES"
                % (fg(9), attr(0))
            )
            exit(1)
        for pkt in capture:
            if pkt.haslayer(IP) and pkt[IP].src != src_ip:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_dst_ip(self, capture, dst_ip):
        """ Filter destination IP addresses from capture 
        
        Args:
            capture (scapy.plist.PacketList): scapy packet capture
            dst_ip (str): target destination IP address to filter for
        """
        try:
            dst_ip = search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", dst_ip).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-dst-ip` MUST BE A VALID IP ADDRESSES"
                % (fg(9), attr(0))
            )
            exit(1)
        for pkt in capture:
            if pkt.haslayer(IP) and pkt[IP].dst == dst_ip:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_dst_ip(self, capture, dst_ip):
        """ Filter destination IP addresses from capture 
        
        Args:
            capture (scapy.plist.PacketList): scapy packet capture
            dst_ip (str): target destination IP address to filter for
        """
        try:
            dst_ip = search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", dst_ip).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-not-dst-ip` MUST BE A VALID IP ADDRESSES"
                % (fg(9), attr(0))
            )
            exit(1)
        for pkt in capture:
            if pkt.haslayer(IP) and pkt[IP].dst != dst_ip:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_src_port(self, capture, src_port):
        """ Filter for packets with a source port that matches `src_port` """
        for pkt in capture:
            try:
                if (pkt.haslayer(TCP) and pkt[TCP].sport == int(src_port)
                or pkt.haslayer(UDP) and pkt[UDP].sport == int(src_port)):
                    self.filtered_packets.append(pkt)
            except ValueError:
                print(
                    "[ %sERROR%s ] SPECIFIED `-src-port` MUST BE WITHIN RANGE: 1-65535"
                    % (fg(9), attr(0))
                )
                exit(1)
        return self.filtered_packets

    def filt_not_src_port(self, capture, src_port):
        """ Filter for packets with a source port that does not match `src_port` """
        for pkt in capture:
            try:
                if (pkt.haslayer(TCP) and pkt[TCP].sport != int(src_port)
                or pkt.haslayer(UDP) and pkt[UDP].sport != int(src_port)):
                    self.filtered_packets.append(pkt)
            except ValueError:
                print(
                    "[ %sERROR%s ] SPECIFIED `-not-src-port` MUST BE WITHIN RANGE: 1-65535"
                    % (fg(9), attr(0))
                )
                exit(1)
        return self.filtered_packets

    def filt_dst_port(self, capture, dst_port):
        """ Filter for packets with a destination port that equals `dst_port` """
        for pkt in capture:
            try:
               if (pkt.haslayer(TCP) and pkt[TCP].dport == int(dst_port)
                or pkt.haslayer(UDP) and  pkt[UDP].dport == int(dst_port)):
                    self.filtered_packets.append(pkt)
            except ValueError:
                print(
                    "[ %sERROR%s ] SPECIFIED `-dst-port` MUST BE WITHIN RANGE: 1-65535"
                    % (fg(9), attr(0))
                )
                exit(1)
        return self.filtered_packets

    def filt_not_dst_port(self, capture, dst_port):
        """ Filter for packets with destination port's that do not match `dst_port` """
        for pkt in capture:
            try:
                if (pkt.haslayer(TCP) and pkt[TCP].dport != int(dst_port)
                or pkt.haslayer(UDP) and pkt[UDP].dport != int(dst_port)):
                    self.filtered_packets.append(pkt)
            except ValueError:
                print(
                    "[ %sERROR%s ] SPECIFIED `-not-dst-port` MUST BE WITHIN RANGE: 1-65535"
                    % (fg(9), attr(0))
                )
                exit(1)
        return self.filtered_packets

    def filt_src_mac(self, capture, src_mac):
        """ Filter for packets whose source MAC address equals `src_mac` """
        try:
            src_mac = search(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}", src_mac).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-src-mac` MUST BE A VALID MAC ADDRESS"
                % (fg(9), attr(0))
                )
            exit(1)

        for pkt in capture:
            if pkt.haslayer(Ether) and pkt[Ether].src == src_mac:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_src_mac(self, capture, src_mac):
        """ Filter for packets whose source MAC address does not equal `src_mac` """
        try:
            src_mac = search(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}", src_mac).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-not-src-mac` MUST BE A VALID MAC ADDRESS"
                % (fg(9), attr(0))
                )
            exit(1)

        for pkt in capture:
            if pkt.haslayer(Ether) and pkt[Ether].src != src_mac:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_dst_mac(self, capture, dst_mac):
        """ Filter for packets with destination MAC address that is equal to `dst_mac` """
        try:
            dst_mac = search(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}", dst_mac).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-dst-mac` MUST BE A VALID MAC ADDRESS"
                % (fg(9), attr(0))
                )
            exit(1)

        for pkt in capture:
            if pkt.haslayer(Ether) and pkt[Ether].dst == dst_mac:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_dst_mac(self, capture, dst_mac):
        """ Filter for packets with destination MAC addresses not matching `dst_mac` """
        try:
            dst_mac = search(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}", dst_mac).group(0)
        except AttributeError:
            print(
                "[ %sERROR%s ] SPECIFIED `-not-dst-mac` MUST BE A VALID MAC ADDRESS"
                % (fg(9), attr(0))
                )
            exit(1)

        for pkt in capture:
            if pkt.haslayer(Ether) and pkt[Ether].dst != dst_mac:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_tcp(self, capture, _):
        """ Filter for TCP packets """
        for pkt in capture:
            if pkt.haslayer(TCP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_tcp(self, capture, _):
        """ Filter for non-TCP packets """
        for pkt in capture:
            if not pkt.haslayer(TCP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_udp(self, capture, _):
        """ Filter for UDP packets """
        for pkt in capture:
            if pkt.haslayer(IP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_udp(self, capture, _):
        """ Filter for non-UDP packets """
        for pkt in capture:
            if not pkt.haslayer(UDP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_icmp(self, capture, _):
        """ Filter for ICMP packets """
        for pkt in capture:
            if pkt.haslayer(ICMP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_icmp(self, capture, _):
        """ Filter for non-ICMP packets """
        for pkt in capture:
            if not pkt.haslayer(ICMP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_arp(self, capture, _):
        """ Filter for ARP packets """
        for pkt in capture:
            if pkt.haslayer(ARP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_arp(self, capture, _):
        """ Filter for non-ARP packets """
        for pkt in capture:
            if not pkt.haslayer(ARP):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_dns(self, capture, _):
        """ Filter for DNS packets """
        for pkt in capture:
            if pkt.haslayer(DNS):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_not_dns(self, capture, _):
        """ Filter for non-DNS packets """
        for pkt in capture:
            if not pkt.haslayer(DNS):
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def filt_tcp_flags(self, capture, target_flags):
        """ Filter for packets with TCP flags in the order specified in the list `target_flags` """
        target_flags = [flag.upper() for flag in target_flags]
        for pkt in capture:
            if pkt.haslayer(TCP):
                pkt_flags = sorted([self.FLAGS[flag] for flag in pkt[TCP].flags])
                if pkt_flags == sorted(target_flags):
                    self.filtered_packets.append(pkt)
        return self.filtered_packets

    def len_less_equal(self, capture, value):
        """ Filter for packets with a length less than or equal to `value` """
        for pkt in capture:
            if pkt.haslayer(Ether) and len(pkt) <= value:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def len_greater_equal(self, capture, value):
        """ Filter for packets with a length greater than or equal to `value` """
        for pkt in capture:
            if pkt.haslayer(Ether) and len(pkt) >= value:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def len_equal(self, capture, value):
        """ Filter for packets with a length that is equal to `value` """
        for pkt in capture:
            if pkt.haslayer(Ether) and len(pkt) == value:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def ttl_equal(self, capture, value):
        """ Filter for packets with time-to-live equal to `value` """
        for pkt in capture:
            if pkt.haslayer(Ether) and pkt[Ether].ttl == value:
                self.filtered_packets.append(pkt)
        return self.filtered_packets

    def summary(self, capture):
        """ Prints a summary of the data contained in a capture.
        This summary includes:
            - unique IP and the number of times they appear
            - unique port number and the number of time they appear
            - unique mac addresses and the number of times they appear

        Args:
            capture (scapy.plist.PacketList): scapy packet capture list
        """
        try:
            # FILTERING IP ADDRESSES
            ip_list = (
                [pkt[IP].src for pkt in capture if pkt.haslayer(IP)]
                + [pkt[IP].dst for pkt in capture if pkt.haslayer(IP)]
            )
            ip_dict = Counter(ip_list)

            header_1, header_2 = "%sIP Address%s"%(fg(75), attr(0)), "Count"
            t = PrettyTable([header_1, header_2], padding_width=3)
            for ip, count in ip_dict.most_common():
                t.add_row([ip, count])
            print(t)

            try:
                # FILTERING PORT NUMBERS
                port_list = (
                    [pkt[1].sport for pkt in capture if TCP in pkt or UDP in pkt]
                    + [pkt[1].dport for pkt in capture if TCP in pkt or UDP in pkt]
                )
            except Exception as err:
                print(err)
                
            port_dict = Counter(port_list)
            
            header_1, header_2 = "%sPORT%s"%(fg(75), attr(0)), "Count"
            t = PrettyTable([header_1, header_2], padding_width=3)
            for port, count in port_dict.most_common():
                t.add_row([port, count])
            print(t)

            # FILTERING MAC ADDRESSES
            mac_list = (
                [pkt[Ether].src for pkt in capture if pkt.haslayer(Ether)]
                + [pkt[Ether].dst for pkt in capture if pkt.haslayer(Ether)]
            )
            mac_dict = Counter(mac_list)

            header_1, header_2 = "%sMAC Address%s"%(fg(75), attr(0)), "Count"
            t = PrettyTable([header_1, header_2], padding_width=3)
            for mac, count in mac_dict.most_common():
               t.add_row([mac, count]) 
            print(t)

            # FILTERING PACKET LENGTHS
            i = 0
            pkt_len_sum = 0
            for pkt in capture:
                if pkt.haslayer(Ether):
                    i += 1
                    pkt_len_sum += len(pkt)
            average_pkt_len = round(pkt_len_sum / i, 1)
            print("%sAVERAGE PACKET LENGTH%s: %s bytes" % (fg(109), attr(0), average_pkt_len))

            # FILTERING TTL
            i = 0
            pkt_ttl_sum = 0
            for pkt in capture:
                if pkt.haslayer(IP):
                    try:
                        i += 1
                        pkt_ttl_sum += pkt[IP].ttl
                    except AttributeError:
                        continue
            average_pkt_ttl = round(pkt_ttl_sum / i, 1)
            print("%sAVERAGE TTL%s: %s " % (fg(109), attr(0), average_pkt_ttl))
        except:
            print(
                "[ %sERROR%s ] COULDN'T GENERATE COMPLETE CAPTURE SUMMARY"
                % (fg(9), attr(0))
            )
            exit(1)

    def json_summary(self, capture, filename):
        """ Generate JSON file containing summary of packet capture.
        The JSON file will contain:
            - ip: count
            - port: count
            - mac: count
        
        Args:
            capture (scapy.plist.PacketList): scapy packet capture list
            filename (str): name of JSON file to create
        """
        capture_summary = {}

        ip_list = ([pkt[IP].src for pkt in capture if pkt.haslayer(IP)]
        + [pkt[IP].dst for pkt in capture if pkt.haslayer(IP)])
        ip_dict = Counter(ip_list)
        capture_summary["ip_dict"] = ip_dict

        port_list = ([pkt[IP].sport for pkt in capture if pkt.haslayer(TCP) or pkt.haslayer(UDP)]
        + [pkt[IP].dport for pkt in capture if pkt.haslayer(TCP) or pkt.haslayer(UDP)])
        port_dict = Counter(port_list)
        capture_summary["port_dict"] = port_dict

        mac_list = ([pkt[Ether].src for pkt in capture if pkt.haslayer(Ether)]
        + [pkt[Ether].dst for pkt in capture if pkt.haslayer(Ether)])
        mac_dict = Counter(mac_list)
        capture_summary["mac_dict"] = mac_dict
        
        try:
            if filename:
                with open(filename, "w") as cap_sum_file:
                    dump(capture_summary, cap_sum_file, indent=4)
            else:
                with open("capture_summary.json", "w") as cap_sum_file:
                    dump(capture_summary, cap_sum_file, indent=4)
        except:
            print(
                "[ %sERROR%s ] THERE WAS AN ERROR CREATING SUMMARY JSON FILE... PLEASE TRY AGAIN"
                % (fg(9), attr(0))
            )
