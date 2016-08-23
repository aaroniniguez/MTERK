#!/usr/bin/env python
import helper
import time
if __name__ == "__main__":
    #assuming data is a list with 1 item
    data = helper.getArgs()[0]
    with open("/hitlog.txt", "a+") as display:
        if not any(data == line.rstrip() for line in display):
            display.write(data+"\n")
        else: 
            print "not found"
    print "Access-Control-Allow-Headers: Content-type, Status"
    print "Content-Type: text/html; charset="
    print "Access-Control-Allow-Origin: *"
    print
    print "True"
