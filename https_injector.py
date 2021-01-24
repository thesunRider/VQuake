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
import ipaddress,nmap,random

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



	def response(self,flow):
		#header analysis
		proxy_headers = ['HTTP_X_FORWARDED_FOR','HTTP_X_FORWARDED','HTTP_PROXY_AGENT','HTTP_VIA','HTTP_PROXY_CONNECTION','HTTP_CLIENT_IP']
		for i in flow.response.headers:
			if i in proxy_headers:
				soup = BeautifulSoup(self.return_htmlerror(5543,"Proxy Intrusion Detected.."))
				flow.response.text = str(soup).encode("utf8")


		netrequest = assemble_request(flow.request).decode('utf-8')
		print("Recieved requests:",netrequest)


		if flow.response.headers['Content-Type'] != 'text/html':
			return
		if not flow.response.status_code == 200:
			return
		#process every 10 requests
		if self.num % 10 == 0 :
			html = BeautifulSoup(flow.response.text, 'lxml')
			container = html.head or html.body
			if container:
				script = html.new_tag('script', type='text/javascript')
				script.string = injected_javascript
				container.insert(0, script)
				flow.response.text = str(html)

			

	def list_filtering(self,filter_param):
		#url filter
		if self.sqlread_exists("url_filter","url",filter_param.request.pretty_url):
			print('Found Blacklisted URL,Blocking')
			return [True,"Blacklisted URL Breach..",5545]


		#eppol namak ip address kitti eni matte sanam load cheyth compare cheyka
		if filter_param.server_conn.ip_address:
			if self.sqlread_exists("AI_filter","ip",filter_param.server_conn.ip_address[0]):
				print('Proxy found by AI....')
				return [True,"Stopping Breach,Heurestics Identified Proxy....",5544]

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



		if self.checknmap(filter_param.server_conn.ip_address[0],filter_param.server_conn.ip_address[1]):
			return [True,"Proxy detected by scanners...",5548]
		else:
			self.addtonmap(filter_param.server_conn.ip_address[0],filter_param.server_conn.ip_address[1])
			
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
		print("Trying adding to db",ip,port)
		hfl = cursor.execute("""SELECT COUNT(*) FROM nmap_processed WHERE processed = 0 AND ip = ?;""",[str(ip)])
		fkr = hfl.fetchone()[0]

		print("found",fkr)
		if fkr == 0:
			cursor.executemany("""INSERT INTO nmap_processed VALUES (?,?,0);""",[(str(ip),port)])
			conn.commit()

	def checknmap(self,ip,port):
		hfl = cursor.execute("""SELECT COUNT(*) FROM nmap_processed WHERE processed = 2 AND ip = ?;""",[str(ip)])
		fkr = hfl.fetchone()[0]
		print("Checking nmap database",fkr)
		ret = True if fkr != 0 else False
		return ret




def scan_callback(host, scan_result):
	print('_______________________________________________________________________')
	print(host,scan_result)
	time.sleep(5+random.randint(2,5))
	proxy_methods = ['polipo','squid-http','http-proxy']
	try:
		for i in scan_result['scan'][host]['tcp']:
			if scan_result['scan'][host]['tcp'][i]['name'] in proxy_methods:
				print("Proxy detected blocking")
				cursor.execute("""UPDATE nmap_processed SET processed = 2 WHERE ip = ?;""",[str(host)])
				conn.commit()
			
	except Exception as e:
		print("Scan error")

	cursor.execute("""UPDATE nmap_processed SET processed = 1 WHERE ip = ?;""",[str(host)])
	conn.commit()

	print('_______________________________________________________________________')


		

def nmap_parse():
	print("Started Thread")
	nm = nmap.PortScannerAsync()
	re_scan = nm.scan(hosts="127.0.0.1", arguments='--script http-open-proxy.nse -p8080', callback=scan_callback)
	
	while nm.still_scanning():
		print("Continuing on batch scan ...")

def nmap_parse():

	hfl = cursor.execute("""SELECT * FROM nmap_processed WHERE processed = 0;""")
	fkr = hfl.fetchall()
	nm = nmap.PortScannerAsync()
	for host in fkr:
		re_scan = nm.scan(hosts=host[0], arguments='--script http-open-proxy.nse -p' +str(host[1]), callback=scan_callback)

	
	while nm.still_scanning():
		print("Continuing on batch scan ...")
		nm.wait(2)



# see source mitmproxy/master.py for details
#def loop_in_thread(loop, m):
#	asyncio.set_event_loop(loop)  # This is the key.
#	m.run_loop(loop.run_forever)


if __name__ == "__main__":
	conn = sqlite3.connect('db/filtered.db',check_same_thread=False)
	cursor = conn.cursor()
	print(cursor)
	with open('leaker.js', 'r') as f:
		injected_javascript = f.read()

	error_html = open('GUI/error.html').read()
	threading.Timer(5, nmap_parse).start()

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