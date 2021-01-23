from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.net.http.http1.assemble import assemble_request
from bs4 import BeautifulSoup
import threading,asyncio,time,Levenshtein,pandas

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
		print("Probbing....")
		if self.url_filtering(flow.request.pretty_url):
			flow.response = http.HTTPResponse.make(
				200,  # (optional) status code
				self.return_htmlerror(5545,"Blacklisted Url breach"),  # (optional) content
				{"Content-Type": "text/html"}  # (optional) headers
				)

	def response(self, flow):
		netrequest = ssemble_request(flow.request).decode('utf-8')
		soup = BeautifulSoup(flow.response.content, "html.parser")
		soup.title.string

	def url_filtering(self,url):
		for index, row in url_blocked.iterrows():
			print('comparing',url,' ',row['url'])
			if url.find(row['url']) != -1:
				print('Found Blacklisted URL,Blocking')
				return True
		return False

	def return_htmlerror(self,errorcode,errordescrp):
		return "bad things happen".encode()

	def tcp_message(self,flow):
		message = flow.messages[-1]
		breakpoint()

# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
	asyncio.set_event_loop(loop)  # This is the key.
	m.run_loop(loop.run_forever)


if __name__ == "__main__":
	url_blocked = pandas.read_csv('db/url_filter.csv')



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