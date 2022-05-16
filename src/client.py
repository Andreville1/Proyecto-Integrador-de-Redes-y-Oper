
import argparse
import json
import random
import socket
import sys

from pip import main

TIMEOUT = 2

# Lee desde consola los argumentos de manera desordenada
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', type=str)
parser.add_argument('-p', '--password', type=str,)
args = parser.parse_args()

class Client:
	def __init__(self, address, port):
		self.ip = address
		self.address_port = (address, port)
		self.UDP_socket = socket.socket(
			family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.buffer_size = 128
		# TODO: put random values for numSeq and numAck
		seq = random.randint(0, 100)
		self.ack = 0
		self.fin = True

	def validate_user_permissions(self, can_write):
		rep = True
		while(rep):
			permission = input("¿Que necesita?: -r = read, -w = write y -q = exit")

			if (permission == '-w'):
				if(can_write == True):
					# print("llama a metodo de André")
					self.send_operation(self)
					rep = False
				else:
					print("Permiso denegado: Usted no cuenta con permisos de escritura")

			elif(permission == '-r'):
				index = permission = input("Digite el numero de pagina que desee conocer")
				#LEEE DEL DOCUMENTO
				rep = False
			elif(permission == '-q'):
				self.option_quit(self)
			else:
				print("Comando invalido")

	def authentication(self, user, password):

		self.seq = self.seq + 1 # 2
		data_json = {"seq":self.seq,"type":"login","fin":True,"username":user,"password":password}
		# encrypt
		data_json_cifrado = self.cifrado_cesar(json.dumps(data_json), 3)
		bytesToSend = str.encode(data_json_cifrado)
		# Envia el login
		self.UDP_socket.sendto(bytesToSend, self.address_port)

		# msg_to_send = str(json_to_send)
		# self.UDP_socket.sendto(str.encode(data_json_cifrado), self.address_port)

		no_stop = True
		while no_stop:
			self.UDP_socket.settimeout(TIMEOUT)
			try:
				# Recibe la confirmacion del servidor
				json_msg = self.recv_json(self)

				# Copia la confirmacion y la direccion
				# confirmation_msg, addr = self.UDP_socket.recvfrom(1024)
				# json_confirmation_msg = json.loads(confirmation_msg)

				while(json_msg["seq"] != self.ack_expected): # 12 != 12
					json_msg = self.recv_json(self)
				self.ack = json_msg["seq"] # 12
				self.ack_expected = self.ack + 1 # 13


				# Recibe la validation
				json_msg = self.recv_json(self)

				# validation_msg, addr = self.UDP_socket.recvfrom(1024)
				#json_validation_msg = json.loads(validation_msg)
				
				while(json_msg["seq"] != self.ack_expected): # 13 != 13
					json_msg = self.recv_json(self)
				self.ack = json_msg["seq"] # 13
				self.ack_expected = self.ack + 1 # 14
				

				no_stop = False

			except:
				data_json = {"seq":seq,"type":"login","fin":True,"username":user,"password":password}
				#encrypt
				data_json_cifrado = self.cifrado_cesar(json.dumps(data_json), 3) 
				bytesToSend = str.encode(data_json_cifrado)
				# send to server
				self.UDP_socket.sendto(bytesToSend, self.address_port) 
				
				# msg_to_send = str(json_to_send)
				# self.UDP_socket.sendto(str.encode(msg_to_send), self.address_port)

		if (json_msg["validated"] == True):
			self.seq = self.seq + 1 # 3
			data_json = {"type":"ack","ack":self.ack_expected,"seq":self.seq}
			# encrypt
			data_json_cifrado = self.cifrado_cesar(json.dumps(data_json), 3)
			bytesToSend = str.encode(data_json_cifrado)
			# Envia la confirmacion de que le llego ser aceptado
			self.UDP_socket.sendto(bytesToSend, self.address_port)

			# msg_to_server = str(msg_to_server)
			# self.UDP_socket.sendto(str.encode(msg_to_server), self.address_port)

			self.validate_user_permissions(self, json_msg["canWrite"])
		else:
			print("[Cerrando conexion]: Usuario o contraseña invalida")
			ack = int(json_msg["seq"]) + 1
			seq += 1
			msg_to_server = {"type":"ack","ack":ack,"seq":seq}
			msg_to_server = str(msg_to_server)
			# Envia la confirmacion de que le llego no ser aceptado
			self.UDP_socket.sendto(str.encode(msg_to_server), self.address_port)
			self.UDP_socket.close()

	def send_json(self, data_json):
		# encrypt
		data_json_cifrado = self.cifrado_cesar(json.dumps(data_json), 3) # json_string = json.dump(data_json)
		bytesToSend = str.encode(data_json_cifrado) # self.cifrado_cesar(json_string, 3)
		# json_to_send = str.encode(json_string)
		# Envia el json
		self.UDP_socket.sendto(bytesToSend, self.address_port) # self.UDP_socket.sendto(json_to_send, self.address_port)

	def recv_json(self): 
		bytes_recv = self.UDP_socket.recvfrom(1024)
		message_recv = bytes_recv[0]
		addr = bytes_recv[1]
		# decrypt
		msg = message_recv.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt)
		
		return json_msg

	def option_quit(self):
		data_json = {"seq": self.seq, "type": "disconnect"}
		self.send_json(data_json)
		
		no_stop = True
		while no_stop:
			self.UDP_socket.settimeout(TIMEOUT)
			try:
				self.verify(self)
				no_stop = False
				self.UDP_socket.close()
			except:
				self.send_json(data_json)

	def send_request(self):

		self.validate_user_permissions(self, True)

	def send_verification(self):
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		self.send_json(data_json)

	def receive_verification(self):
		#TODO: refactor this:
		valid = False

		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		serverAddressPort = bytes_recv[1]
		# decrypt
		msg = message_recv.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt) # verification_json = json.loads(verification)

		if json_msg["type"] == "ack":
			if json_msg["ack"] == self.seq + 1: # 5 = 5 | 6 = 6
				if json_msg["seq"] == self.ack_expected: # 14 = 14 | 15 = 15
					self.ack = json_msg["seq"] # 14 | 15
					self.ack_expected = self.ack + 1 # 15 | 16

					valid = True
				else:
					print("Seq erroneo")
			else:
				print("Ack erroneo")
		else:
			print("Ack erroneo")

		return valid

	def verify(self): # Verifica que le llega el paquete que es
		valid = self.receive_verification(self)	
		while (valid != True):	
			valid = self.receive_verification(self)

	def send_operation(self):
		self.seq = self.seq + 1 # 4 | 5
		operation = input("Ingrese la operacion: ")
		data_json = {"seq": self.seq, "type": "request",
                    "fin": self.fin, "request": "write", "operation": operation}
		
		json_string = json.dumps(data_json)
		
		if (len(json_string.encode('utf-8')) <= 128): # Lo envia de una vez
			self.send_json(data_json)

			no_stop = True
			while no_stop :
				self.UDP_socket.settimeout(TIMEOUT)
				try:
					self.verify(self)

					no_stop = False
				except :
					self.send_json(data_json)

			self.recv_operation(self)

		else: # Lo envia por partes
			self.fin = False
			data_json_1 = {"seq": self.seq, "type": "request",
                    "fin": self.fin, "request": "write"}
			self.send_json(data_json_1)
			self.verify()

			data_json_2 = {"operation": operation}
			self.send_json(data_json_2)
			self.verify()

	def recv_operation(self):

		# recv from server
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		# decrypt
		msg = message_recv.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt)

		#TODO: Refactor this:
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size) # msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0] # operation = msg_from_server[0].decode()
		serverAddressPort = bytes_recv[1].decode() # serverAddressPort = msg_from_server[1].decode()
		# encrypt
		msg = message_recv.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt) # operation_json = json.loads(operation) 
		if json_msg["seq"] == self.ack_expected: # 16 = 16 | 17 = 17
			if json_msg["type"] == "request":
				if json_msg["fin"] == True:
					if json_msg["request"] == "write":
						self.ack = json_msg["seq"] # 16 | 17
						self.ack_expected = self.ack + 1 # 17 | 18
						self.seq = self + 1 # 6 | 7

						print(json_msg["result"])
						# Envia la verificacion que le llego bien el resultado
						self.send_verification()
						
						self.send_request(self, json_msg)
					else:
						print("Request erroneo")
				else:
					print("DEBE ESPERAR LO FRACCIONADO") # OJOOO
			else:
				print("Type erroneo")
		else:
			print("Seq erroneo")

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

	def handshake(self):
		# create message syn
		data_json = {"type": "syn", "seq": self.seq} #seq = 0
		# encrypt
		data_json_cifrado = self.cifrado_cesar(json.dumps(data_json), 3)
		bytesToSend = str.encode(data_json_cifrado)
		# send to server
		self.UDP_socket.sendto(bytesToSend, self.address_port)
		print("sent syn to server")
		print(self.seq, self.ack, self.ack_expected)

		# recv from server
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = msg_from_server[0]
		# decrypt
		msg = message_recv.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt)

		# self.ack = server.seq
		self.ack = json_msg["seq"] # 10
		# self.ack_exp = server.seq + 1
		self.ack_expected = json_msg["seq"] + 1 # 11

		print(self.seq, self.ack, self.ack_expected)

		#create messagr ack
		self.seq = self.seq + 1 # 1
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		# encrypt
		data_json_cifrado = self.cifrado_cesar(json.dumps(data_json), 3)
		bytesToSend = str.encode(data_json_cifrado)
		# send to server
		self.UDP_socket.sendto(bytesToSend, self.address_port)
		print("sent ack to server")

		# recv from server
		bytes_recv = self.UDP_socket.recvfrom(self.buffer_size)
		message_recv = bytes_recv[0]
		# decrypt
		msg = message_recv.decode()
		msg_decrypt = self.cifrado_cesar(msg, 26-3)
		json_msg = json.loads(msg_decrypt)
		print(json_msg)
		# check if server_seq = ack_expected
		if int(json_msg["seq"]) == self.ack_expected:
			# port = server_port
			self.address_port = (self.ip, json_msg["port"])
			self.ack = json_msg["seq"] # 11
			self.ack_expected = self.ack + 1 # 12
			print("recv ack with port from server")

		else:
			print("couldnt establish connection")
			self.UDP_socket.close()



	def main(self, user, password):
		while(True):
			self.handshake()
			self.authentication(self, user, password)
			# self.send_operation()
			# if (self.receive_verification()):
			#	self.receive_operation()


if __name__ == "__main__":
	client = Client("127.0.0.1", 8080)
	client.main(args.user, args.password)
