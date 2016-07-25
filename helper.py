#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import urllib

import sys
import codecs
def getArgs():
	arglist = []
	f = cgi.FieldStorage()
	f = cgi.FieldStorage()
	print f
	for i in f.keys():
		data = urllib.unquote(f[i].value)
		data = data.replace("aaronsemicolon",":")
		data = data.replace("aarondot", ".")
		data = data.replace("questionmark","?")
		data = data.replace("aaronhash","#")
		data = data.replace("aaronequals","=")
		data = data.replace("aaronand", "&")
		data = data.replace("googlepercent", "%")
		arglist.append(data)
	return arglist
def correctCoding(r):
	#when printing go from unicode to bytstring, have to specify the 
	#conversion type, default for printing to termianl is utf8, 
	#all other defaults are ascii
	if r.encoding is not None:
		UTF8Writer = codecs.getwriter(r.encoding)
	else:
		UTF8Writer = codecs.getwriter("UTF-8")
	sys.stdout = UTF8Writer(sys.stdout)
