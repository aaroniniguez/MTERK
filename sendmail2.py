import smtplib
import helper
data = helper.getArgs()
message = data[0]
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
n = 133
messages = message.split("urllink")
newmessages = []
for x in messages: 
	newmessages.extend([x[i:i+n] for i in range(0, len(x), n)])
server.login("aaroniniguez1@gmail.com", "Impossible123foryou")
print newmessages
for x in newmessages:
	server.sendmail("aaroniniguez1@gmail.com", "9165178775@messaging.sprintpcs.com", x.replace(":",""))
server.quit()
print "Access-Control-Allow-Headers: Content-type, Status"
print "Access-Control-Allow-Origin: *"
print
print message
