from dataclasses import dataclass
from http import client
import json
import random
from socket import socket
from socketserver import UDPServer
from urllib import request
import socket
from pip import main
from math import sqrt

TIMEOUT = 300


class Server:
	
	def __init__(self, address, port):
		self.ip = address
		self.address_port = (address, port)
		self.UDP_socket = socket.socket(
			family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDP_socket_paso_mensajes = socket.socket(
                    family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.buffer_size = 128
		# TODO: put random values for numSeq and numAck
		self.seq = 10 #seq = random.randint(0, 100)
		self.ack_expected = 0
		self.ack = 0
		self.fin = True

# taken from: https://www.pythonpool.com/caesar-cipher-python/
	def cifrado_cesar(self, message, shift):
		encryp_str = ""
		for element in message:
			if element.isupper():
				temp = 65 + ((ord(element) - 65 + shift) % 26)
				encryp_str = encryp_str + chr(temp)
			elif element.islower():
				temp = 97 + ((ord(element) - 97 + shift) % 26)
				encryp_str = encryp_str + chr(temp)
			else:
				encryp_str = encryp_str + element
		return encryp_str

	
	def credential_validation(self, user, password):
		valid_user = False
		can_write = False
		with open('C:/Users/Jaffet A/Desktop/users.json') as file:
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

		# Recibe el login
		#print("ENTRE AL LOGIN SERVER")
		json_msg, address = self.recv_json()
		#print("ESTO ES EL LOGIN SERVER")
		print("seq y ack expected: ", json_msg["seq"], self.ack_expected)
		while json_msg["seq"] != self.ack_expected: # 2 = 2
			json_msg, address = self.recv_json()
		self.ack = json_msg["seq"] # 2
		self.ack_expected = self.ack + 1 # 3
		self.seq = self.seq + 1 # 12

		validated, can_write = self.validation(json_msg)

		# Envia la confirmacion de que le llego el login
		self.send_verification(address)

		self.seq = self.seq + 1 # 13
		#print("ESTO ES EL LOGIN SERVER ANTES DE MANDAR SI ES VALIDO LA CONTRASEÑA")
		#print("seq que se manda y validated: ", self.seq , validated)
		data_json = {"seq":self.seq,"type":"login","fin":True,"username":"user","password":"pass","validated":validated, "canWrite":can_write}
		# encrypt
		msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3) # smg_to_send = str(smg_to_send)
		bytesToSend = str.encode(msg_to_send)
		# Envia que si fue validado o no
		self.UDP_socket.sendto(bytesToSend, address) # self.UDP_socket.sendto(str.encode(smg_to_send), address)

		# Recibe la verificaion de que le llego el validado
		json_msg, address = self.recv_json()
		
		#print("ESTO ES EL LOGIN SERVER ANTES DEL WHILE")
		#print("seq y ack expected: ", json_msg["seq"], self.ack_expected)
		while json_msg["seq"] != self.ack_expected: # 3 = 3
			json_msg, address = self.recv_json()
		self.ack = json_msg["seq"] # 3
		self.ack_expected = self.ack + 1 # 4

	def recv_operation(self):
		operation_json, server_address_port = self.recv_json()

		if operation_json["seq"] == self.ack_expected: # 4 = 4 | 5 = 5
			if operation_json["type"] == "request":
				if operation_json["request"] == "write":
					if operation_json["fin"] == True:
						self.ack = operation_json["seq"] # 4 | 5
						self.ack_expected = self.ack + 1 # 5 | 6
						self.seq = self.seq + 1 # 14 | 15

						self.send_verification(server_address_port)
						
						self.seq = self.seq + 1 # 16 | 17
						operation = operation_json["operation"]
						operation = operation.replace("**", "^")
						result = eval(operation)

						self.send_result(server_address_port, result, operation)

						self.recv_verification()
					else:
						#Caso en que se fracciona el msg
						self.send_verification(server_address_port)
						operation_json, server_address_port = self.recv_json()
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

	def send_verification(self, address):
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		# encrypt
		msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3) # json_string = json.dump(data_json)
		bytesToSend = str.encode(msg_to_send) # json_to_send = str.encode(json_string)
		# send to client	
		self.UDP_socket.sendto(bytesToSend, address) # json_to_send, serverAddressPort

	def send_result(self, address, result, operation):
		data_json = {"seq": self.seq, "type": "request", "fin": self.fin,
				"request": "write", "result": result, "operation": operation}
		# encrypy
		msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3) # json_string = json.dump(data_json)
		bytesToSend = str.encode(msg_to_send) # json_to_send = str.encode(json_string)
		# Envia el resultado
		self.UDP_socket.sendto(bytesToSend, address) # self.UDP_socket.sendto(json_to_send, serverAddressPort)

	def recv_verification(self):
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size) # json_to_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0] # verification = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = message_recv.decode() # veri = verification.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt) # verification_json = json.loads(veri)

		if json_msg["type"] == "ack":
			if json_msg["ack"] == self.seq + 1: # 17 = 17 | 18 = 18
				if json_msg["seq"] == self.ack_expected: # 6 = 6 | 7 = 7
					self.ack = json_msg["seq"] # 6 | 7
					self.ack_expected = self.ack + 1 # 7 | 8

					self.recv_request()
				else:
					print("Seq erroneo")
			else:
				print("Ack erroneo")
		else:
			print("Type erroneo")

	def recv_request(self):
		self.UDP_socket.settimeout(TIMEOUT)
		while True:
			try:
				bytes_recv = self.UDP_socket.recvfrom(self.buffer_size) # json_to_recv = UDPServer.recvfrom(self.buffer_size)
				message_recv = bytes_recv[0] # request = json_to_recv[0]
				address = bytes_recv[1] # server_address_port = json_to_recv[1]
				msg = message_recv.decode() # req = request.decode()
				msg_decrypt = self.cifrado_cesar(msg, 26-3)
				json_msg = json.loads(msg_decrypt) # request_json = json.loads(req)

				self.ack = json_msg["seq"]
				self.ack_expected = self.ack + 1 # 9
				self.seq = self.seq + 1 # 18

				data_json = {"type":"ack","ack":self.ack_expected,"seq":self.seq}
				# encrypt
				msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3)
				bytesToSend = str.encode(msg_to_send)
				# Envia la confirmacion de que va a cerrar
				self.UDP_socket.sendto(bytesToSend, address)

				if json_msg["type"] == "disconnect":
					self.UDP_socket.close()
					break
				else:
					print("RECIBE OPERACION") #OJOOO
			
			except:
				print("Se agoto el tiempo de espera del servidor")
				break

	def recv_json(self):
		# recv from client
		#print("ESTOY EN RECIV JSON")
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		#bytes_recv = self.UDP_socket.recvfrom(self.buffer_size) # json_to_recv = self.UDP_socket.recvfrom(self.buffer_size)
		#print("RECIVI EL RECIV JSON")
		message_recv = msg_from_server[0] # operation = json_to_recv[0]
		address = msg_from_server[1] # server_address_port = json_to_recv[1]
		msg = message_recv.decode() # oper = operation.decode()
		#print("DECODE EL RECIV JSON")
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt) # operation_json = json.loads(oper)
		#print("ESTOY SALIENDO RECIV JSON")
		return json_msg, address

	def handshake(self):
		#recv from client
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		address = bytes_recv[1]
		msg = message_recv.decode()
		msg_decrypt = self.decypher(msg)
		print(msg_decrypt)
		json_msg = json.loads(msg_decrypt)

		print("recv syn from client")
		# numACK = clientSeq
		self.ack = int(json_msg["seq"])
		self.ack_expected = self.ack + 1

		# armar mensaje ack
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		# encrypt
		msg_to_send = self.cypher(json.dumps(data_json))

		bytesToSend = str.encode(msg_to_send)
		# send to client
		self.UDP_socket.sendto(bytesToSend, address)
		print("sent ack to client")

		#recv from client
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		address = bytes_recv[1]
		msg = message_recv.decode()
		msg_decrypt = self.decypher(msg)
		json_msg = json.loads(msg_decrypt)

		if int(json_msg["seq"]) == self.ack_expected:
			self.ack = json_msg["seq"]
			self.ack_expected = self.ack + 1
			self.seq = self.seq + 1
			#send to client
			# armar mensaje ack
			data_json = {"type": "ack", "ack": self.ack_expected,
                            "seq": self.seq, "port": address[1]}
			#encrypt
			msg_to_send = self.cypher(json.dumps(data_json))
			bytesToSend = str.encode(msg_to_send)
			# send to client
			self.address_port = address
			print(self.address_port)
			print(address)
			self.UDP_socket.sendto(bytesToSend, self.address_port)
			print("sent ack with port to client")
			self.UDP_socket_paso_mensajes.bind(self.address_port)
		else:
			print("No se pudo establecer conexión")
			self.UDP_socket.close()

	def main(self):
		while True:
			self.handshake()
			#print("SALIO DEL HAND")
			self.login()
			self.recv_operation()


if __name__ == "__main__":
	server = Server("127.0.0.1", 8080)
	server.main()

