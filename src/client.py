from http import client
import json
import random
from socket import socket

from pip import main


class Client:
	def __init__(self, address, port):
		self.address_port = (address, port)
		self.UDP_socket = socket.socket(
			family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.buffer_size = 128
		# TODO: put random values for numSeq and numAck
		self.seq = 0
		self.ack = 0
		self.fin = True

	def send_json(self, data_json):
		json_string = json.dump(data_json)
		# Se encripta
		json_to_send = str.encode(json_string)

		# Envia la solicitud de desconexion
		self.UDP_socket.sendto(json_to_send, self.address_port)

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

	def send_operation(self):
		operation = input("Ingrese la operacion: ")
		data_json = {"seq": self.seq, "type": "request",
                    "fin": self.fin, "request": "write", "operation": operation}
		self.send_json(data_json)

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

	def receive_verification(self):
		#TODO: refactor this:
		msg_from_server = self.UDP_socket.recvfrom(self.buffer_size)
		verification = msg_from_server[0].decode()
		serverAddressPort = msg_from_server[1].decode()
		verification_json = json.loads(verification)

		if verification_json["type"] == "ack":
			if verification_json["ack"] == self.ack:
				if verification_json["seq"] == self.seq:
					self.receive_operation()

				else:
					print("Seq erroneo")
			else:
				print("Ack erroneo")
		else:
			print("Ack erroneo")

	def main(self):
		while(True):
			self.send_operation()
			self.receive_verification()


if __name__ == "__main__":
	client = Client("127.0.0.1", 8080)
	client.main()
