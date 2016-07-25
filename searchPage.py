#!/usr/bin/env python
import os
import sys
sys.path.insert(0,'/data/proxies')
import cgi
import urllib
print "Content-Type: text/html"
print "Access-Control-Allow-Origin: *"
print

#f = cgi.FieldStorage()
#for i in f.keys():
#       if i == "url":
#               url = "http://"+urllib.unquote(f[i].value)
#       else:
#               print i

import Browse
import lxml.html
from lxml.etree import tostring
from tld import get_tld
import re

twitterlist = []
pinterestlist = []
instagramlist = []
youtubelist = []
facebooklist = []
emaillist = []
rellinks = []

def lookSocial(url):
	print "searching "+url
	mytld = get_tld(url, as_object=True)
	searchfor = mytld.domain
	r = Browse.Browse(url, searchfor)
	doc = lxml.html.document_fromstring(r.text)
	selector  = "a"
	global pinterestlist
	global facebooklist
	global emaillist
	global twitterlist
	global youtubelist
	global instagramlist
	for a in doc.cssselect(selector):
			if a.get("href"):
				if "mailto:" in a.get("href"):
					emaillist.append(a.get("href").replace("mailto:", ""))
				if "facebook.com/" in a.get("href"):
					facebooklist.append(a.get("href"))
				if "twitter.com/" in a.get("href"):
					if "?" not in a.get("href"):
						twitterlist.append(a.get("href"))
				elif "instagram.com/" in a.get("href"):
					if "?" not in a.get("href"):
						instagramlist.append(a.get("href"))
				elif "pinterest.com/" in a.get("href"):
					if "?" not in a.get("href"):
						pinterestlist.append(a.get("href"))
				elif "youtube.com/" in a.get("href"):
					if "?" not in a.get("href"):
						youtubelist.append(a.get("href"))
url = "http://theclothes.blogspot.com/"
rellinks.append(url)
print rellinks
mytld = get_tld(url, as_object=True)
print mytld
searchfor = mytld.domain
r = Browse.Browse(url, searchfor)
doc = lxml.html.document_fromstring(r.text)
selector  = "a"
for a in doc.cssselect(selector):
	if a.get("href"):
		if a.get("href")[0] is "/":
			if ".com" not in a.get("href"):
				rellinks.append("http://www."+str(mytld)+a.get("href"))	
		elif str(mytld) in a.get("href"):
			rellinks.append(a.get("href"))
for a in rellinks:
	lookSocial(a)
selector = "a.addthis_button_twitter_follow"
for a in doc.cssselect(selector):
	print "https://twitter.com/"+a.get("addthis:userid")
selector = "a.addthis_button_pinterest_follow"
for a in doc.cssselect(selector):
	print "https://www.pinterest.com/"+a.get("addthis:userid")
selector = "a.addthis_button_instagram_follow"
for a in doc.cssselect(selector):
	print "https://instagram.com/"+a.get("addthis:userid")
print list(set(twitterlist))
print list(set(pinterestlist))
print list(set(instagramlist))
print list(set(youtubelist))
print list(set(facebooklist))
print list(set(emaillist))
