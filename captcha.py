#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import urllib
print "Content-Type: text/html"
print "Access-Control-Allow-Origin: *"
print
f = cgi.FieldStorage()
for i in f.keys():
	if i == "url":
		url = "https://"+urllib.unquote(f[i].value)
		url = url.replace("questionmark","?")
		url = url.replace("aaronand", "&")
	else:
		print i
import deathbycaptcha
import lxml.html
from lxml.etree import tostring
import requests
import re
from StringIO import StringIO
from PIL import Image
headers = {
	"Cache-Control":"max-age=0",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
	"Accept-Language":"en-US,en;q=0.8",
	"Connection":"keep-alive",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
r = requests.get(url,stream=True, headers = headers)
#no need to decode as requests does it for you
i = Image.open(StringIO(r.content))
i.save("./IMAGE.jpg")
client = deathbycaptcha.SocketClient("Archetype123", "Impossible123")
while True:
	try:
		captcha = client.decode("IMAGE.jpg",30)
		if captcha:
			print captcha["text"]
			break
		else:
			continue
	except:
		continue
