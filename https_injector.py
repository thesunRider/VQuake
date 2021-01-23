from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.net.http.http1.assemble import assemble_request
from bs4 import BeautifulSoup
import threading,asyncio,time,Levenshtein,pandas


from scapy.all import *
from scapy.layers.http import HTTPRequest # import HTTP packet
from mitmproxy.utils import strutils
from mitmproxy import ctx
from mitmproxy import tcp
from mitmproxy import http

class Addon(object):
	def __init__(self):
		self.num = 1

	def request(self, flow):
		self.num += 1
		#for every 5 requests do a probbing
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
		soup.title.string

	def list_filtering(self,filter_param):
		#url filter
		if len(url_blocked[url_blocked['url']==filter_param.request.pretty_url].index.tolist()) > 0:
			print('Found Blacklisted URL,Blocking')
			return [True,"Blacklisted URL Breach..",5545]


		#eppol namak ip address kitti eni matte sanam load cheyth compare cheyka
		ipint = int(ipaddress.IPv4Address(filter_param.server_conn.ip_address))
		if self.checkifipisproxy(ipint):
			print('Found Blacklisted IP,Blocking')
			return [True,"Blacklisted IP Breach..",5546]

		#tor exitnodefilter
		if len(tor_blocked[tor_blocked['tor_exitnodes']==filter_param.request.pretty_url].index.tolist()) > 0:
			print('Found Blacklisted Tor URL node')
			return [True,"Privacy breach (Tor Exit node)..",5547]


		#the connection is going to a tor client
		if filter_param.find('/tor/server/') != -1:
			url_blocked.loc[len(df)] = [filter_param]
			url_blocked.to_csv('db/url_filter.csv', mode='a', header=False)
			return [True,"Privacy breach (Tor Exit node)..",5547]

		return [False,"",0]

	def checkifipisproxy(self,ipint):
		#here do the checking
		return True
		

	def return_htmlerror(self,errorcode,errordescrp):
		rep = error_html.replace('errorcode',str(errorcode)).replace('errordescription',str(errordescrp))
		return rep.encode()

	def tcp_message(self,flow:tcp.TCPFlow):
		message = flow.messages[-1]
		print(message)

# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
	asyncio.set_event_loop(loop)  # This is the key.
	m.run_loop(loop.run_forever)


if __name__ == "__main__":
	url_blocked = pandas.read_csv('db/url_filter.csv')
	tor_blocked = pandas.read_csv('db/tor_filter.csv')
	ip_blocked = pandas.read_csv('db/ip_filter.csv')
	error_html = open('GUI/error.html').read()


	options = Options(listen_host='0.0.0.0', listen_port=8080, http2=True,client_certs='certs/')
	m = DumpMaster(options, with_termlog=False, with_dumper=False)
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