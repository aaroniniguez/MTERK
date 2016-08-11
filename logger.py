#!/usr/bin/env python
import helper
import time
if __name__ == "__main__":
	data = helper.getArgs()
	data.reverse()
	with open("/logger.txt", "a") as display:
		display.write(time.strftime("%Y/%m/%d  %I:%M:%S  "))
		for item in data:
			display.write(item+"  ")
		display.write("\n")
		display.close()
	print "Access-Control-Allow-Headers: Content-type, Status"
	print "Content-Type: text/html; charset="
	print "Access-Control-Allow-Origin: *"
	print
	print "True"
