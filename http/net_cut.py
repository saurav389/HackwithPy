#!/usr/bin/env python
import netfilterqueue


def process_packet(packet):
	print(packet)
	#packet.drop() # this will recieve all the packet but not deliver to destination. This will result no internet connection to destination

	packet.accept() # this will accept the packet and allow the destination to recieve responce from router

queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()