#!/usr/bin/env python
import os 
import sys
import helper
sys.path.insert(0,'/data/proxies')
import urllib
import lxml.html
from lxml.etree import tostring
from tld import get_tld
import re
import requests
#data = ["clp.com/FAQs+1"]
def getIt(data1):
	useragent1 = "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
	useragent2 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36"
	url = "http://"+data1
	url2 = "https://"+data1
	if ("www." not in data1):
		url1 = "http://www."+data1
		url3 = "https://www."+data1
	else:
		url1 = url2.replace("www.", "")
		url3 = url2.replace("www.", "")
	headers = {
		"Cache-Control":"max-age=0",
		"User-Agent":useragent2,
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
			try:
				r = s.get(url2, headers = headers, verify=False, timeout=10)
				print r.request.headers
				r.raise_for_status()
			except Exception, e:
				try:
					r = s.get(url3, headers = headers, verify=False, timeout=10)
					print r.request.headers
					r.raise_for_status()
				except Exception, e:
					r = "undefined"
	if r != "undefined":
		if ("traffic from your computer network" in r.text) or ("Please enter the text below" in r.text) or ("CGI-ODSC Taiga" in r.text) or ("To continue, please type the characters below:" in r.text) or ("403 Forbidden" in r.text ) or ("page not found" in r.text) or ("don't have permission to access" in r.text) or ("503 Service" in r.text) or ("MOE Denied Access Policy" in r.text) or ("IP has been automatically blocked" in r.text):
			r = "undefined"
	failed = 0
	if "undefined" not in r:
		helper.correctCoding(r)
		if r.encoding is None:
			r.encoding = "UTF-8"
		else:
			encoding = r.encoding
		return r
	else:
		return False
if __name__ == "__main__":
	data = helper.getArgs()
	webpage = getIt(data[0])
	if (webpage):
		print "Access-Control-Allow-Headers: Content-type, Status"
		print "Content-Type: text/html; charset="+webpage.encoding
		print "Access-Control-Allow-Origin: *"
		print
		print webpage.text
	else:
		print "Access-Control-Allow-Headers: Content-type, Status"
		print "Content-Type: text/html; charset="
		print "Access-Control-Allow-Origin: *"
		print
		print "False"
