import gc
from greenlet import greenlet    
import gevent.monkey
gevent.monkey.patch_all()
from gevent.queue import Queue
from gevent import Greenlet
import requests
from gevent import Timeout
import time
import gevent
import traceback
import pprint
import helper
pp = pprint.PrettyPrinter(indent=4)
tasks = Queue()
threads = []
dead = False
errors = {
"totalips":0,
"tooslow": 0,
"connection":0,
"httpError":0,
"redirects":0,
"104":0,
"noheaders":0,
"wrongpage":0,
"success":0,
"blocked":0
}
def Browse(url):
	global threads
	global result
	global errors
	result = "undefined"
	f = open("/cgi-bin/allproxies.txt")
	for line in f:
		tasks.put(line.replace("\n", ""))
	f.close()

	errors["totalips"] = tasks.qsize()
	for x in range(100):
		if dead == False:
			threads.append(gevent.spawn(download,url))
	gevent.joinall(threads)
	if result == "undefined":
		with open("/index.html","w") as display:
			display.write("False")
			display.close()
	else:
		with open("/index.html","w") as display:
			display.write(result.content)
			display.close()
	return {"output":result,
	"errors":errors}
def download(url):
	global dead
	global threads
	global result
	global errors
	while not tasks.empty():
		ip = tasks.get()
		timeperiod =13
		timelist = []
		s = requests.Session()
		headers = {
			"Cache-Control":"max-age=0",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
			"Accept-Language":"en-US,en;q=0.8",
			"Connection":"keep-alive",
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		}
		while True:
			try:
				r = bytearray()
				text = "a"
				with Timeout(timeperiod,False):
					start = time.time()
					r = s.get(url,headers=headers, proxies={"https":"https://"+ip}, verify=False)
					end = time.time()
					text = r.text
					timelist.append(end-start)
				#too slow
				if not (len(text)):
					errors["tooslow"] = errors["tooslow"]+1
					s.close()
					break
				#4xx or 5xx response error raised
				r.raise_for_status()
				#sometimes using proxies causes a different page to load than the one you want, search for keyword, title
			except requests.ConnectionError:
				#catches error no 111, 113
			#	print traceback.format_exc()
				errors["connection"] = errors["connection"]+1
				s.close()
				break
			except requests.HTTPError:
				#print traceback.format_exc()
				errors["httpError"] = errors["httpError"]+1
				s.close()
				break
				#raise Exception("\tinvalid http response"+ str(r.status_code) +" on "+ ip)
			except requests.TooManyRedirects:
				s.close()
				errors["redirects"] = errors["redirects"]+1
				#print traceback.format_exc()
				break
			except Exception, e:
				#error 104
				errors["104"] = errors["104"]+1
				#print traceback.format_exc()
				s.close()
				break
			else:
				if (len(r.headers.keys())>0):
					if ("gRecaptchaCallback" not in r.text) and ("Invalid domain for site key" not in r.text) and ("traffic from your computer network " not in r.text) and ("Please enter the text below" not in r.text) and ("To continue, please type the characters below:" not in r.text) and ("has been blocked" not in r.text) and ("503 Service" not in r.text) and ("MOE Denied Access Policy" not in r.text) and ("IP has been automatically blocked" not in r.text):
						print "Success with ip: "+ip
						errors["success"] = errors["success"] +1
						s.close()
						dead = True
						result = r
						gevent.killall(threads)
						break
					else:
						errors["blocked"] = errors["blocked"]+1
						s.close()
						break
				#ip returned zero headers so this is a bad ip
				else:
					errors["noheaders"] = errors["noheaders"]+1
					s.close()
					break
if __name__ == "__main__":
	data = helper.getArgs()
	url = data[1]+"://"+data[0]
	#data = ["http://cosprings.craigslist.org/fb/cos/hss/5702396366"]
	#data = ["http://boston.craigslist.org/fb/bos/hss/5702634214"]
	#data = ["http://washingtondc.craigslist.org/fb/wdc/sks/5703390938"]
	#data = ["http://albuquerque.craigslist.org/fb/abq/hss/5703388147"]
	#data = ["http://victoriatx.craigslist.org/fb/vtx/hss/5703365758"]
	webpage = Browse(url)
	print "Access-Control-Allow-Headers: Content-type, Status"
	print "Content-Type: text/html; charset="
	print "Access-Control-Allow-Origin: *"
	print
	if webpage["output"] == "undefined":
		print "False"
	else: 
		print "{"
		print "\"url\":"+"\""+webpage["output"].url+"\""
		print "}"
	#urlList = []
	#urlList.append("http://seattle.craigslist.org/fb/sea/hss/5698956365")
	#urlList.append("http://miami.craigslist.org/fb/mia/hss/5701599465")
#	urlList.append("http://panamacity.craigslist.org/fb/pfn/hss/5701338855")
	#urlList.append("http://tucson.craigslist.org/fb/tus/sks/5701478846")
	#urlList.append("http://raleigh.craigslist.org/fb/ral/hss/5701730773")
	#urlList.append("http://orangecounty.craigslist.org/fb/orc/hss/5701466978")
	#urlList.append("http://nashville.craigslist.org/fb/nsh/hss/5701649323")
	#for url in urlList:
	#	re = Browse(url)
	#	if re["output"] != "undefined":
	#		print re["errors"]
	#		#print re["output"].text
	#	else:
	#		print re["errors"]
