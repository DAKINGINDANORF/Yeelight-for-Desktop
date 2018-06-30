import json
import socket
import time

class Server_Connector:

    def __init__(self, IP_address, port):
        print('Creating socket')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_address = IP_address
        self.port = port
        self.s.connect((self.IP_address, self.port))
        print('Succesfully connected to: ', self.IP_address)

    def send(self, data):
        message = {'type': 'sent', 'data': data}
        print(type(message))
        jsonmessage = json.dumps(message)
        print(jsonmessage)
        self.s.sendall(jsonmessage.encode())

    def receive(self):
        receivedmessage = self.s.recv(1024)
        print(receivedmessage)
        return json.loads(receivedmessage)

    def printData(self,id):
        message = {'type': 'sent', 'data': id}
        jsonmessage = json.dumps(message)
        self.s.sendall(jsonmessage.encode())
        receivedmessage = self.s.recv(1024).decode()
        print(receivedmessage)
