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
        self.data = {'version':0,'protocol':0,'ttl':0,'src_addr':0,
                            'dst_addr':0,'src_port':0,'dst_port':0,
                            'seq_num':0,'ack_num':0,'flag':0,'data_size':0,'service':"HTTP",'is_proxy':0}
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
  
        
        
        
    # this function is meant to work with sockets; but shows error in windows    
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
    def resolve_protocol(self,packet):
        if packet.protocol[0]==pydivert.Protocol.TCP:
            print("src_port" + str(packet.tcp.src_port))
            print("dest_port" + str(packet.tcp.dst_port))
        if packet.tcp.ack:
            return (packet.tcp.ack_num,packet.tcp.seq_num)
        else:
            return 0
    
    
    def write_divert_packet(self,packet,is_proxy):
        
        
        
        src_addr= packet.src_addr
        dst_addr = packet.dst_addr
        
        ver=0
        if packet.address_family == socket.AF_INET:
            ver=0
            ttl=packet.ipv4.ttl
            data_size = packet.ipv4.packet_len - packet.ipv4.header_len
            
        elif  packet.address_family == socket.AF_INET6:
            ver=1
            return 
        else:
            return
        
        
        #detect protocol , 1 if TCP
        protocol=0
        
        if self.resolve_protocol(packet)!=1:
            protocol=1
            src_port = packet.tcp.src_port
            dst_port = packet.tcp.dst_port
            seq_num = packet.tcp.seq_num
            ack_num = packet.tcp.ack_num
            flag_data = {'ns':0,'cwr':0,'ece':0,'urg':0,'ack':0,'psh':0,'rst':0,'syn':0,'fin':0}
            flag_data_num=0
            if packet.tcp.ns:
                flag_data['ns']=1
                flag_data_num^=(1<<1)
            if packet.tcp.cwr:
                flag_data['cwr']=1
                flag_data_num^=(1<<2)
            if packet.tcp.ece:
                flag_data['ece']=1
                flag_data_num^=(1<<3)
            if packet.tcp.urg:
                flag_data['urg']=1
                flag_data_num^=(1<<4)
            if packet.tcp.ack:
                flag_data['ack']=1
                flag_data_num^=(1<<5)
            if packet.tcp.psh:
                flag_data['psh']=1
                flag_data_num^=(1<<6)
            if packet.tcp.rst :
                flag_data['rst']=1
                flag_data_num^=(1<<7)
            if packet.tcp.syn:
                flag_data['syn']=1
                flag_data_num^=(1<<8)
            if packet.tcp.fin :
                flag_data['fin']=1
                flag_data_num^=(1<<9)
            
    #service = 0 mean http 
        
        self.fields_dict = {'version':ver,'protocol':protocol,'ttl':ttl,'src_addr':src_addr,
                            'dst_addr':dst_addr,'src_port':src_port,'dst_port':dst_port,
                            'seq_num':seq_num,'ack_num':ack_num,'flag':flag_data_num,'data_size':data_size,'service':0,'is_proxy':is_proxy}
        
        
        self.csv_writer.data=self.fields_dict
        
    #['version','protocol','ttl','src_addr','dst_addr','src_port','dest_port','seq_num','ack_num','flag','data_size','service','is_proxy']




if __name__ == "__main__":
    fields = ['version','protocol','ttl','src_addr','dst_addr','src_port','dst_port','seq_num','ack_num','flag','data_size','service','is_proxy']
    analyser=PacketData()
    analyser.writer_init()
    
    
    
    
    with pydivert.WinDivert('tcp.DstPort == 80 and tcp.PayloadLength > 0') as w:
        for packet in w:
            analyser.write_divert_packet(packet,0)
            analyser.csv_writer.write_data()
    
    
            
    
    
    
    
    
    

        
    
        
    
    