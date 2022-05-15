from http import client
import argparse
import json
import random
from socket import socket
import sys

from pip import main

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
		self.seq = 0
		self.ack = 0
		self.fin = True

	def validate_user_permissions(self, json_validation_message):
		rep = True
		while(rep):
			permission = input("¿Que tipo de permiso necesita?: -r = read y -w = write")

			if (permission == '-w'):
				if(json_validation_message["canWrite"] == True):
					print("llama a metodo de André")
					#LLAMA A METODO DE OPERACION
					rep = False
				else:
					print("Permiso denegado: Usted no cuenta con permisos de escritura")

			elif(permission == '-r'):
				index = permission = input("Digite el numero de pagina que desee conocer")
				#LEEE DEL DOCUMENTO
				rep = False
			else:
				print("Comando invalido")

	def authentication(self, user, password):

		seq = random.randint(0, 100)
		json_to_send ={"seq":seq,"type":"login","fin":True,"username":user,"password":password}
		msg_to_send = str(json_to_send)
		# Se encripta
		self.UDP_socket.sendto(str.encode(msg_to_send), self.address_port)

		# Recibe la confirmacion del servidor
		# Copia la confirmacion y la direccion
		confirmation_msg, addr = self.UDP_socket.recvfrom(1024)
		json_confirmation_msg = json.loads(confirmation_msg)

		while(json_confirmation_msg["ack"] != (seq+1)):
			confirmation_msg, addr = self.UDP_socket.recvfrom(1024)
			json_confirmation_msg = json.loads(confirmation_msg)
		
		# Recibe la validation
		validation_msg, addr = self.UDP_socket.recvfrom(1024)
		json_validation_msg = json.loads(validation_msg)


		if (json_validation_msg["validated"] == True):
			ack = int(json_validation_msg["seq"]) + 1
			seq += 1
			msg_to_server = {"type":"ack","ack":ack,"seq":seq}
			msg_to_server = str(msg_to_server)
			# Envia la confirmacion de que le llego ser aceptado
			self.UDP_socket.sendto(str.encode(msg_to_server), self.address_port)
			self.validate_user_permissions(json_validation_msg)
		else:
			print("[Cerrando conexion]: Usuario o contraseña invalida")
			ack = int(json_validation_msg["seq"]) + 1
			seq += 1
			msg_to_server = {"type":"ack","ack":ack,"seq":seq}
			msg_to_server = str(msg_to_server)
			# Envia la confirmacion de que le llego no ser aceptado
			self.UDP_socket.sendto(str.encode(msg_to_server), self.address_port)
			self.UDP_socket.close()

	def send_json(self, data_json):
		
		json_string = json.dump(data_json)
		self.cifrado_cesar(json_string, 3)
		# Se encripta
		json_to_send = str.encode(json_string)

		# Envia la solicitud de desconexion
		self.UDP_socket.sendto(json_to_send, self.address_port)

	def recv_json(self): 
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		json_server = msg_from_server[0].decode()
		json_server = self.cifrado_cesar(json_server, 26-3)
		print(json_server)
		return json_server

	def option_quit(self):
		data_json = {"seq": self.seq, "type": "disconnect"}
		self.send_json(data_json)
		self.UDP_socket.close()

	def send_request(self):
		opcion = input("Ingrese una opcion: ")

		if opcion[0] == "-" and opcion[1] == "q":
			self.option_quit()
		else:
			print("HACE OTRA OPERACION")

	def send_verification(self):
		data_json = {"type": "ack", "ack": self.ack, "seq": self.seq}
		self.send_json(data_json)

		self.send_request()

	def receive_verification(self):
		#TODO: refactor this:
		valid = False
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		verification = msg_from_server[0].decode()
		serverAddressPort = msg_from_server[1].decode()
		verification_json = json.loads(verification)

		if verification_json["type"] == "ack":
			if verification_json["ack"] == self.ack:
				if verification_json["seq"] == self.seq:
					valid = True

				else:
					print("Seq erroneo")
			else:
				print("Ack erroneo")
		else:
			print("Ack erroneo")

		return valid

	def verify(self):
		valid = self.receive_verification(self)	
		while (valid != True):	
			valid = self.receive_verification(self)

	def send_operation(self):
		operation = input("Ingrese la operacion: ")
		data_json = {"seq": self.seq, "type": "request",
                    "fin": self.fin, "request": "write", "operation": operation}
		json_string = json.dump(data_json)
		
		if (len(json_string.encode('utf-8')) <= 128):
			self.send_json(data_json)
		else:
			self.fin = False
			data_json_1 = {"seq": self.seq, "type": "request",
                    "fin": self.fin, "request": "write"}
			self.send_json(data_json_1)
			self.verify()

			data_json_2 = {"operation": operation}
			self.send_json(data_json_2)
			self.verify()

				
		

	def recieve_operation(self):
		#TODO: Refactor this:
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		operation = msg_from_server[0].decode()
		serverAddressPort = msg_from_server[1].decode()

		operation_json = json.loads(operation)

		if operation_json["seq"] == self.seq:
			if operation_json["type"] == "request":
				if operation_json["fin"] == True:
					if operation_json["request"] == "write":
						print(operation_json["result"])
						self.send_verification()
					else:
						print("Request erroneo")
				else:
					print("DEBE ESPERAR LO FRACCIONADO")
			else:
				print("Type erroneo")
		else:
			print("Seq erroneo")

	def receive_operation(self):
		#TODO: refactor this:
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		operation = msg_from_server[0].decode()
		serverAddressPort = msg_from_server[1].decode()

		operation_json = json.loads(operation)

		if operation_json["seq"] == self.seq:
			if operation_json["type"] == "request":
				if operation_json["fin"] == True:
					if operation_json["request"] == "write":
						print(operation_json["result"])
						self.send_verification()

					else:
						print("Request erroneo")
				else:
					print("DEBE ESPERAR LO FRACCIONADO")
			else:
				print("Type erroneo")
		else:
			print("Seq erroneo")

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

	
	def handshake(self):
		data_json = {"type": "syn", "seq": self.seq}
		self.send_json(data_json)
		
		json_server = self.recv_json()
	
		self.ack = json_server["seq"] 
		self.seq += 1
	
		data_json = {"type": "ack", "ack": self.ack, "seq": self.seq}
		self.send_json(data_json)

		self.ack = json_server["seq"]
		self.seq += 1

		json_server = self.recv_json()
		self.ack = json_server["seq"]
		self.address_port = (self.ip, json_server["port"])
		


	def main(self):
		while(True):
			self.handshake()
			self.send_operation()
			if (self.receive_verification()):
				self.receive_operation()


if __name__ == "__main__":
	client = Client("127.0.0.1", 8080)
	client.main()
