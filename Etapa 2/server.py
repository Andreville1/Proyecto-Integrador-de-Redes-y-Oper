from dataclasses import dataclass
from http import client
import json
import random
from socket import socket
from socketserver import UDPServer
from urllib import request
import socket
from math import sqrt

TIMEOUT = 300


class Server:
	
	def __init__(self, address, port):
		self.ip = address
		self.address_port = (address, port)
		self.buffer_size = 128
		# TODO: put random values for numSeq and numAck
		self.seq = seq = random.randint(0, 100) #10
		self.ack_expected = 0
		self.ack = 0
		self.fin = True

		self.new_address_port = (0,0)
	
	def credential_validation(self, user, password):
		valid_user = False
		can_write = False
		with open('users.json') as file:
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
		json_msg, address = self.recv_json()
		while json_msg["seq"] != self.ack_expected: # 2 = 2
			json_msg, address = self.recv_json()
		self.ack = json_msg["seq"] # 2
		self.ack_expected = self.ack + 1 # 3
		self.seq = self.seq + 1 # 12

		validated, can_write = self.validation(json_msg)

		# Envia la confirmacion de que le llego el login
		self.send_verification(address)

		self.seq = self.seq + 1 # 13
		data_json = {"seq":self.seq,"type":"login","fin":True,"username":"user","password":"pass","validated":validated, "canWrite":can_write}
		# encrypt
		msg_to_send = self.cypher(json.dumps(data_json)) # msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3)
		bytesToSend = str.encode(msg_to_send)
		# Envia que si fue validado o no
		self.UDP_socket_paso_mensajes.sendto(bytesToSend, address)

		# Recibe la verificaion de que le llego el validado
		json_msg, address = self.recv_json()
		
		while json_msg["seq"] != self.ack_expected: # 3 = 3
			json_msg, address = self.recv_json()
		self.ack = json_msg["seq"] # 3
		self.ack_expected = self.ack + 1 # 4

	def recv_operation(self, operation_json, address):
		# operation_json, server_address_port = self.recv_json()
		if operation_json["type"] == "request":
			if operation_json["request"] == "write":
				if operation_json["fin"] == True:
					# self.ack = operation_json["seq"] # 4 | 5
					# self.ack_expected = self.ack + 1 # 5 | 6
					# self.seq = self.seq + 1 # 14 | 15

					# self.send_verification(server_address_port)
					self.seq = self.seq + 1 # 16 | 17
					operation = operation_json["operation"]
					operation = operation.replace("**", "^")
					result = eval(operation)

					self.send_result(address, result, operation)

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

	def send_verification(self, address):
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		# encrypt
		msg_to_send = self.cypher(json.dumps(data_json)) # msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3) 
		bytesToSend = str.encode(msg_to_send) # json_to_send = str.encode(json_string)
		# send to client	
		self.UDP_socket_paso_mensajes.sendto(bytesToSend, address) # json_to_send, serverAddressPort

	def send_result(self, address, result, operation):
		data_json = {"seq": self.seq, "type": "request", "fin": self.fin,
				"request": "write", "result": result, "operation": operation}
		# encrypy
		msg_to_send = self.cypher(json.dumps(data_json)) # msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3)
		bytesToSend = str.encode(msg_to_send) # json_to_send = str.encode(json_string)
		# Envia el resultado
		self.UDP_socket_paso_mensajes.sendto(bytesToSend, address)

	def recv_verification(self):
		bytes_recv = self.UDP_socket_paso_mensajes.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0] # verification = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = message_recv.decode() # veri = verification.decode()
		msg_decrypt = self.decypher(msg) # msg_decrypt = self.cifrado_cesar(msg, 26-3)
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
		self.UDP_socket_paso_mensajes.settimeout(TIMEOUT)
		no_stop = True
		while no_stop :
			try:
				bytes_recv = self.UDP_socket_paso_mensajes.recvfrom(self.buffer_size) # json_to_recv = UDPServer.recvfrom(self.buffer_size)
				message_recv = bytes_recv[0] # request = json_to_recv[0]
				address = bytes_recv[1] # server_address_port = json_to_recv[1]
				msg = message_recv.decode() # req = request.decode()
				msg_decrypt = self.decypher(msg) # msg_decrypt = self.cifrado_cesar(msg, 26-3)
				json_msg = json.loads(msg_decrypt) # request_json = json.loads(req)

				self.ack = json_msg["seq"]
				self.ack_expected = self.ack + 1 # 9

				self.seq = self.seq + 1 # 18
				data_json = {"type":"ack","ack":self.ack_expected,"seq":self.seq}
				# encrypt
				msg_to_send = self.cypher(json.dumps(data_json)) # msg_to_send = self.cifrado_cesar(json.dumps(data_json), 3)
				bytesToSend = str.encode(msg_to_send)
				# Envia la confirmacion de que va a cerrar
				self.UDP_socket_paso_mensajes.sendto(bytesToSend, address)
				no_stop = False
			except:
				print("Se agoto el tiempo de espera del servidor")
				no_stop = False

		if json_msg["type"] == "disconnect":
			self.UDP_socket_paso_mensajes.close()
		else:
			self.recv_operation(json_msg, address)
	
	def recv_json(self):
		# recv from client
		msg_from_server = self.UDP_socket_paso_mensajes.recvfrom(self.buffer_size)
		message_recv = msg_from_server[0] # operation = json_to_recv[0]
		address = msg_from_server[1] # server_address_port = json_to_recv[1]
		msg = message_recv.decode() # oper = operation.decode()
		msg_decrypt = self.decypher(msg) # msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt) # operation_json = json.loads(oper)
		return json_msg, address
	
	# taken from: https://stackoverflow.com/questions/58616651/struggling-with-ascii-loop-for-caesar-cipher
	def cypher(self, string):
		offset_value = 3
		range_ = list(range(ord('\0'), ord('}')+1))
		min_val, max_val = range_[0], range_[-1]
		diff_plus_1 = (max_val - min_val) + 1
		result = ""
		for i in range(len(string)):
			char = string[i]
			result += chr((((ord(char) - min_val) + offset_value) %
                            diff_plus_1) + min_val)
		return result

	def decypher(self, string):
		offset_value = -3
		range_ = list(range(ord('\0'), ord('}')+1))
		min_val, max_val = range_[0], range_[-1]
		diff_plus_1 = (max_val - min_val) + 1
		result = ""
		for i in range(len(string)):
			char = string[i]
			result += chr((((ord(char) - min_val) + offset_value) %
                            diff_plus_1) + min_val)
		return result

	def handshake(self):
		self.UDP_socket = socket.socket(
			family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDP_socket_paso_mensajes = socket.socket(
                    family=socket.AF_INET, type=socket.SOCK_DGRAM)
		print("Recibo desde", self.address_port)
		# Vincula direccion e IP
		self.UDP_socket.bind(self.address_port)

		#recv from client
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		address = bytes_recv[1]
		msg = message_recv.decode()
		msg_decrypt = self.decypher(msg)
		json_msg = json.loads(msg_decrypt)
		# print("recv syn from client")
		print("Recibo", json_msg)

		# numACK = clientSeq
		self.ack = int(json_msg["seq"])
		self.ack_expected = self.ack + 1

		# armar mensaje ack
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		print("\nRecibo/Envio desde", address)
		print("Envio", data_json)
		# encrypt
		msg_to_send = self.cypher(json.dumps(data_json))
		bytesToSend = str.encode(msg_to_send)
		# send to client
		self.UDP_socket.sendto(bytesToSend, address)
		# print("sent ack to client")
		
		#recv from client
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		address = bytes_recv[1]
		# decrypt
		msg = message_recv.decode()
		msg_decrypt = self.decypher(msg)
		json_msg = json.loads(msg_decrypt)
		print("\nRecibo", address)
		print("Recibo", json_msg)

		if int(json_msg["seq"]) == self.ack_expected:
			new_port = 4040
			self.ack = json_msg["seq"]
			self.ack_expected = self.ack + 1

			self.seq = self.seq + 1
			#send to client
			# armar mensaje ack
			data_json = {"type": "ack", "ack": self.ack_expected,
                            "seq": self.seq, "port": new_port} #address[1]
			print("\nRecibo/Envio desde", address)
			print("Envio", data_json)
			#encrypt
			msg_to_send = self.cypher(json.dumps(data_json))
			bytesToSend = str.encode(msg_to_send) # self.address_port = address NUEVO
			# send to client
			self.UDP_socket.sendto(bytesToSend, address) # self.address_port
			
			# print("sent ack with port to client")
			self.new_address_port = (self.ip, new_port) # address[1]
			new_port = new_port + 1
			self.UDP_socket.close()
			self.UDP_socket_paso_mensajes.bind(self.new_address_port)
			
		else:
			print("No se pudo establecer conexi??n")
			self.UDP_socket.close()

	def main(self):
		while True:
			self.handshake()
			self.login()
			self.recv_request()# self.recv_operation()


if __name__ == "__main__":
	server = Server("127.0.0.1", 8080)
	server.main()

