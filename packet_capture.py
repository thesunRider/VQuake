from scapy.all import *

capture = 'test.pcap'
pcap = rdpcap(capture)

ports=137

def write(pkt):
    wrpcap('filtered.pcap', pkt, append=True)  #appends packet to output file

for pkt in pcap:
    if pkt.haslayer(UDP) and pkt.getlayer(UDP).sport == ports:  #checks for UDP layer and sport 137
        write(pkt)  #sends the packet to be written if it meets criteria
    else:
        pass