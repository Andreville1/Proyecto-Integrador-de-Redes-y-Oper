from http import client
import json
import random
from socket import socket
from socketserver import UDPServer
from urllib import request

from pip import main
from math import sqrt

TIMEOUT = 300


class Server:
	
	def __init__(self, address, port):
		self.ip = address
		self.address_port = (address, port)
		self.UDP_socket = socket.socket(
			family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.buffer_size = 128
		# TODO: put random values for numSeq and numAck
		self.seq = 0
		self.ack = 0
		self.fin = True

# taken from: https://www.geeksforgeeks.org/caesar-cipher-in-cryptography/
	def cifrado_cesar(self, message, shift):
		result = ""

		for index in range(len(message)):
			char = message[index]

			# Encrypt uppercase characters
			if (char.isupper()):
				result += chr((ord(char) + shift-65) % 26 + 65)

			# Encrypt lowercase characters
			else:
				result += chr((ord(char) + shift - 97) % 26 + 97)

		return result
	
	def credential_validation(self, user, password):
		valid_user = False
		can_write = False
		with open('ruta_del_archivo/nombre.json') as file:
			data = json.load(file)
			for users in data['users']:
				if (users['username'] == user):
					if (users['password'] == password):
						can_write = users['canWrite']
						valid_user = True

		return valid_user, can_write

	def validation(self, json_msg):
		#abro el archivo json y compruebo
		user = json_msg["username"]
		password = json_msg["password"]
		validations = self.credential_validation(user, password)
		return validations
	
	def login(self):
		# Vincula la direccion e IP
		UDPServerSocket.bind((host, port))
		seq = random.randint(0, 100)
		while True:
			# Recibe el login
			bytesAddressPair = UDPServerSocket.recvfrom(1024)
			message = bytesAddressPair[0]
			address = bytesAddressPair[1]

			msg = str.decode(message)

			json_msg = json.loads(msg)
			validated, can_write= self.validation(json_msg)

			# Envia la confirmacion de que le llego el login
			self.send_verification(address)

			# Envia que si fue validado o no
			my_seq += 1
			smg_to_send = {"seq":my_seq,"type":"login","fin":True,"username":"user","password":"pass","validated":validated, "canWrite":can_write}
			smg_to_send = str(smg_to_send)

			UDPServerSocket.sendto(str.encode(smg_to_send), address)

	def verify_package(self):
		operation_json, server_address_port = self.receive_package()

		if operation_json["seq"] == self.seq:
			if operation_json["type"] == "request":
				if operation_json["request"] == "write":
					if operation_json["fin"] == True:

						self.send_verification(server_address_port)
						
						operation = operation_json["operation"]
						operation = operation.replace("**", "^")
						result = eval(operation)

						self.send_result(server_address_port, result, operation)

						self.recv_verification()
					else:
						#Caso en que se fracciona el msg
						self.send_verification(server_address_port)
						operation_json, server_address_port = self.receive_package()
						self.send_verification(server_address_port)

						operation = operation_json["operation"]
						operation = operation.replace("**", "^")
						result = eval(operation)
						
						self.send_result(server_address_port, result, operation)
						self.recv_verification()
				else:
					print("Request erroneo")
			else:
				print("Type erroneo")
		else:
			print("Numero de secuencia erroneo")

	def send_verification(self, serverAddressPort):
		data_json = {"type": "ack", "ack": self.ack, "seq": self.seq}
		json_string = json.dump(data_json)
		# Se encripta
		json_to_send = str.encode(json_string)

		self.UDP_socket.sendto(json_to_send, serverAddressPort)

	def send_result(self, serverAddressPort, result, operation):
		data_json = {"seq": self.seq, "type": "request", "fin": self.fin,
				"request": "write", "result": result, "operation": operation}
		json_string = json.dump(data_json)
		# Se encripta
		json_to_send = str.encode(json_string)

		self.UDP_socket.sendto(json_to_send, serverAddressPort)

	def recv_verification(self):
		json_to_recv = self.UDP_socket.recvfrom(self.buffer_size)
		verification = json_to_recv[0]
		server_address_port = json_to_recv[1]

		veri = verification.decode()

		verification_json = json.loads(veri)

		if verification_json["type"] == "ack":
			if verification_json["ack"] == self.ack:
				if verification["seq"] == self.seq:
					self.recv_request()
				else:
					print("Seq erroneo")
			else:
				print("Ack erroneo")
		else:
			print("Type erroneo")

	def recv_request(self):
		UDPServer.settimeout(TIMEOUT)
		while True:
			try:
				json_to_recv = UDPServer.recvfrom(self.buffer_size)
				request = json_to_recv[0]
				server_address_port = json_to_recv[1]
				req = request.decode()

				request_json = json.loads(req)

				if request_json["type"] == "disconnect":
					self.UDP_socket.close()
					break
				else:
					print("RECIBE OPERACION") #OJOOO
			
			except:
				printf("Se agoto el tiempo de espera del servidor")
				break

	def receive_package(self):
		json_to_recv = self.UDP_socket.recvfrom(self.buffer_size)
		operation = json_to_recv[0]

		server_address_port = json_to_recv[1]
		oper = operation.decode()
		operation_json = json.loads(oper)

		return operation_json, server_address_port


	def main(self):
		while True:
			self.handshake()
			self.recv_operation()


if __name__ == "__main__":
	server = Server("127.0.0.1", 8080)
	server.main()


# Inicio del recibimiento del producto
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
port = 8080
bufferSize = 1024
ack = 0
seq = 0
fin = True
host = "127.0.0.1"
UDPServerSocket.bind((host, port))
