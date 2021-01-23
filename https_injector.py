from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.net.http.http1.assemble import assemble_request
from bs4 import BeautifulSoup
import threading,asyncio,time,Levenshtein,pandas,sqlite3
from scapy.all import *
from scapy.layers.http import HTTPRequest # import HTTP packet
from mitmproxy.utils import strutils
from mitmproxy import ctx
from mitmproxy import http
import ipaddress,nmap

class Addon(object):
	num=1

	def request(self, flow):
		self.num += 1
		#for every 5 requests do a probbing
		print('probs')
		print(self.num)
		filtered = self.list_filtering(flow)
		if filtered[0]:
			flow.response = http.HTTPResponse.make(
				400,  # (optional) status code
				self.return_htmlerror(filtered[2],filtered[1]),  # (optional) content
				{"Content-Type": "text/html"}  # (optional) headers
				)

	def response(self, flow):
		netrequest = assemble_request(flow.request).decode('utf-8')
		soup = BeautifulSoup(flow.response.content, "html.parser")
		soup.title

	def list_filtering(self,filter_param):
		#url filter
		if self.sqlread_exists("url_filter","url",filter_param.request.pretty_url):
			print('Found Blacklisted URL,Blocking')
			return [True,"Blacklisted URL Breach..",5545]


		#eppol namak ip address kitti eni matte sanam load cheyth compare cheyka

		if filter_param.server_conn.ip_address:
			ipint = int(ipaddress.IPv4Address(filter_param.server_conn.ip_address[0]))
			if self.sqlcheck_ip(ipint):
				print('Found Blacklisted IP,Blocking')
				return [True,"Blacklisted IP Breach..",5546]

		#tor exitnodefilter
		if self.sqlread_exists("tor_filter","tor_exitnodes",filter_param.request.pretty_url):
			print('Found Blacklisted Tor URL node')
			return [True,"Privacy breach (Tor Exit node)..",5547]


		#the connection is going to a tor client
		if filter_param.request.pretty_url.find('/tor/server/') != -1:
			return [True,"Privacy breach (Tor Exit node)..",5547]

		self.addtonmap(filter_param.server_conn.ip_address[0],filter_param.server_conn.ip_address[1])
		#addtonmapprocess(filter_param.server_conn.ip_address)
			
		return [False,"",0]
		

	def return_htmlerror(self,errorcode,errordescrp):
		rep = error_html.replace('errorcode',str(errorcode)).replace('errordescription',str(errordescrp))
		return rep.encode()

	def sqlcheck_ip(self,ipint):
		hfl = cursor.execute("""SELECT COUNT(*) FROM blacklisted WHERE ? BETWEEN first AND last;""", [ipint])
		ret = hfl.fetchone()[0]
		print("Returning ip range check=",ret)
		return ret

	def sqlread_exists(self,table,idm,value):
		hfl = cursor.execute("""SELECT COUNT(*) FROM """ +str(table) +""" WHERE """+str(idm)  +""" = ?;""", [str(value)])
		ret = hfl.fetchone()[0]
		print(table," ",idm," ",value,"=",ret)
		return ret

	def addtonmap(self,ip,port):
		hfl = cursor.execute("""SELECT COUNT(*) FROM nmap_processed WHERE processed = 0 AND ip = ?;""",[str(ip)])
		fkr = hfl.fetchone()[0]
		if fkr == 0:
			cursor.executemany("""INSERT INTO nmap_processed VALUES (?,?,0);""",[(str(ip),port)])



def nmap_parse():
	hfl = cursor.execute("""SELECT * FROM nmap_processed WHERE processed = 0;""")
	fkr = hfl.fetchall()
	nm = nmap.PortScanner()
	for host in fkr:
		re_scan = nm.scan(hosts=host[0], arguments='--script http-open-proxy.nse -p' +str(host[1]))
	print("Launching nmap with:",hosts)



# see source mitmproxy/master.py for details
#def loop_in_thread(loop, m):
#	asyncio.set_event_loop(loop)  # This is the key.
#	m.run_loop(loop.run_forever)


if __name__ == "__main__":
	conn = sqlite3.connect('db/filtered.db')
	cursor = conn.cursor()
	print(cursor)

	error_html = open('GUI/error.html').read()


	options = Options(listen_host='0.0.0.0', listen_port=8080, http2=True,client_certs='certs/')
	m = DumpMaster(options, with_termlog=True, with_dumper=False)
	config = ProxyConfig(options)
	m.server = ProxyServer(config)
	m.addons.add(Addon())

	# run mitmproxy in backgroud, especially integrated with other server
	loop = asyncio.get_event_loop()
	asyncio.set_event_loop(loop)  # This is the key.
	m.run_loop(loop.run_forever)

	#t = threading.Thread( target=loop_in_thread, args=(loop,m) )
	#t.start()

	print('going to shutdown mitmproxy')
	m.shutdown()