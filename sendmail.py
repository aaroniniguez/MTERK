import smtplib
import helper
data = helper.getArgs()
message = data[0]
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("aaroniniguez1@gmail.com", "Impossible123foryou")
server.sendmail("aaroniniguez1@gmail.com", "aaroniniguez1@gmail.com", message.replace(":",""))
server.quit()
print "Access-Control-Allow-Headers: Content-type, Status"
print "Access-Control-Allow-Origin: *"
print
print message
