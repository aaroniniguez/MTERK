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
		url = "http://"+urllib.unquote(f[i].value)
with open("/cgi-bin/errors.txt","a") as errorfile:
	errorfile.write(url+"\n")
	errorfile.close()
