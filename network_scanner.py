import scapy.all as scapy
import argparse

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="Target Ip/Ip range")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_dict = {"ip":element[1].psrc,"mac":element[1].hwsrc}
        client_list.append(client_dict)
        # print(element[1].psrc,"\t\t\t",element[1].hwsrc)
    return client_list


def print_result(result_list):
    print("IP \t\t\t\t MAC ADDRESS\n________________________________________________________")
    for client in result_list:
        print(client["ip"]+"\t\t\t"+client["mac"])

option = argument()
scan_result = scan(option.target)
print_result(scan_result)

