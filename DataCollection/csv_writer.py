#CSV Writer 
import csv 
import socket 
import struct 
import sys
import pydivert

class DataWriter:
    def __init__(self,file,fields):
        self.csvfile = open(file,'w', newline='')
        self.fields=fields
        self.writer = csv.DictWriter(self.csvfile, delimiter =',',fieldnames=fields)    
        #self.fieldnames={'src_port':'src_port' , 'dst_port':'dst_port', 'seq':'seq', 'ack':'ack', 'doff':'doff', 'tcph_len':'tcph_len','h_size':'h_size', 'data_size':'data_size', 'is_proxy':'is_proxy'}
        #self.writer.writerow(self.fieldnames)
        #self.data = {'src_port':0 , 'dst_port':0, 'seq':0, 'ack':0, 'doff':0, 'tcph_len':0,'h_size':0, 'data_size':0, 'is_proxy':0}
    def write_data(self):
        self.writer.writerow(self.data)
    def populate(self,args):
        #here args is a dict defined as  
        #{'src_port':2 , 'dst_port':3, 'seq':4, 'ack':0, 'doff':0, 'tcph_len':0,'h_size':0, 'data_size':0, 'is_proxy':0}
        self.data=args
    def close(self):
        self.csvfile.close()

class PacketData:
    def __init__(self):
        self.ip_header=0
        self.src_port=0
        self.dst_port = 0
        self.seq = 0
        self.ack =0 
        self.doff = 0
        self.tcph_len = 0
        self.h_size = 0
        self.data_size = 0
        self.is_proxy = 0
        self.ver_ihl = 0
        self.ihl = 0
        self.iph_len= 0
        self.ttl = 0
        self.protocol = 0
        self.src_addr = 0
        self.dst_addr = 0
  
        
        
        
    # this function is meant to work with sockets     
    def strip_packet(pack,is_proxy):
        #type  = 0 non proxy , 1 proxy 
        packet = pack[0]
        self.ip_header = packet[0:20]
        self.iph = struct.unpack('!BBHHHBBH4s4s',self.ip_header)
        self.ver_ihl = self.iph[0]
        self.ver = self.ver_ihl>>4
        self.ihl = self.ver_ihl & 0xF
        self.iph_len = self.ihl* 4
        self.ttl = self.iph[5]
        self.protocol= self.iph[6]
        self.src_addr = socket.inet_ntoa(self.iph[8]) 
        self.dst_addr = socket.inet_ntoa(self.iph[9])
        tcp_header = packet[20:40]
        tcph = struct.unpack('!HHLLBBHHH', tcp_header)
        self.src_port = tcph[0]
        self.dst_port= tcph[1]
        self.seq = tcph[2]
        self.ack_num = tcph[3]
        self.doff = tcph[4]
        self.tcph_len = self.doff>>4
        
        self.h_size = self.iph_len + self.tcp_length * 4
        self.data_size = len(packet) - self.h_size
        #self.flag_types = {TCP:}
        self.fields_dict = {'version':self.ver,'protocol':self.protocol,'ttl':self.ttl,'src_addr':self.src_addr,
                            'dst_addr':self.dst_addr,'src_port':self.src_port,'dst_port':self.dst_port,
                            'seq_num':self.seq_num,'ack_num':self.ack_num,'flag':0,'data_size':self.data_size,'service':"HTTP",'is_proxy':is_proxy}
    
        print(str(self.fields_dict))
    
    def writer_init(self):
        self.fields = ['version','protocol','ttl','src_addr','dst_addr','src_port','dst_port','seq_num','ack_num','flag','data_size','service','is_proxy']
        self.csv_writer = DataWriter('ipfile.csv',fields)
       
    # for pydivert
    def resolve_protocol(packet):
    if packet.protocol[0]==pydivert.Protocol.TCP:
        print("src_port" + str(packet.tcp.src_port))
        print("dest_port" + str(packet.tcp.dst_port))
        if packet.tcp.ack:
            return (packet.tcp.ack_num,packet.tcp.seq_num)
        else:
            return 0
    def write_divert_packet(self,packet):
        
        
        ver=0
        if packet.address_family == socket.AF_INET:
            ver=0
        elif  packet.address_family == socket.AF_INET6:
            ver=1
        else:
            ver=0
        
        
        #detect protocol , 1 if TCP
        protocol=0
        if resolve_protocol(packet)!=1:
            protocol=1
        
        
            
            
            
            
            
            
        self.fields_dict = {'version':ver,'protocol':protocol,'ttl':self.ttl,'src_addr':self.src_addr,
                            'dst_addr':self.dst_addr,'src_port':self.src_port,'dst_port':self.dst_port,
                            'seq_num':self.seq_num,'ack_num':self.ack_num,'flag':0,'data_size':self.data_size,'service':"HTTP",'is_proxy':is_proxy}
        
        
        
    #['version','protocol','ttl','src_addr','dst_addr','src_port','dest_port','seq_num','ack_num','flag','data_size','service','is_proxy']




if __name__ == "__main__":
    fields = ['version','protocol','ttl','src_addr','dst_addr','src_port','dest_port','seq_num','ack_num','flag','data_size','service','is_proxy']
    writer = DataWriter('ipfile.csv',fields)
    stripper=PacketData()
    
    
    
    
    with pydivert.WinDivert() as w:
        for packet in w:
            stripper.write_divert_packet(packet)
    
    
            
    
    
    
    
    
    
    s= socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP)
    s.listen(20)
    
    try:
        s= socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP)
    except socket.error:
        print('could not create')
        sys.exit()
    #s.bind(('',0))
    s.listen()
    packet = s.recv(1024)
    stripper.writer_init()
    stripper.strip_packet(packet,0)
    stripper.csv_writer.write_data()
      
        
    
        
    
    