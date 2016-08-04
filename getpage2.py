#!/usr/bin/env python
import helper
import lxml.html
from lxml.etree import tostring
import requests
#data = ["clp.com/FAQs+1"]
def getIt(url):
	useragent = "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
	if ("www." not in url):
		url1 = url.split("//")[0]+"www."+"".join(url.split("//")[1:])
	headers = {
		"Cache-Control":"max-age=0",
		"User-Agent":useragent,
		"Accept-Language":"en-US,en;q=0.8",
		"Connection":"keep-alive",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	}
	try:
		s = requests.Session()
		r = s.get(url, headers = headers, verify=False, timeout=10)
		r.raise_for_status()
	except Exception, e:
		try:
			r = s.get(url1, headers = headers, verify=False, timeout=10)
			print r.request.headers
			r.raise_for_status()
		except Exception, e:
			r = "undefined"
	if r != "undefined":
		if ("traffic from your computer network" in r.text) or ("Please enter the text below" in r.text) or ("CGI-ODSC Taiga" in r.text) or ("To continue, please type the characters below:" in r.text) or ("403 Forbidden" in r.text ) or ("page not found" in r.text) or ("don't have permission to access" in r.text) or ("503 Service" in r.text) or ("MOE Denied Access Policy" in r.text) or ("IP has been automatically blocked" in r.text):
			r = "undefined"
	if r == "undefined":
		with open("/index2.html","w") as display:
			display.write("False")
			display.close()
	else:
		with open("/index2.html","w") as display:
			display.write(r.content)
			display.close()
	return r
if __name__ == "__main__":
	data = helper.getArgs()
	url = data[1]+"://"+data[0]
	webpage = getIt(url)
	print "Access-Control-Allow-Headers: Content-type, Status"
	print "Content-Type: text/html; charset="
	print "Access-Control-Allow-Origin: *"
	print
	if webpage == "undefined":
		print "False"
	else: 
		print "{"
		print "\"url\":"+"\""+webpage.url+"\""
		print "}"
