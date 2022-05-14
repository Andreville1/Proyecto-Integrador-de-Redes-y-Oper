from http import client
import json
import random
from socket import socket
from socketserver import UDPServer
from urllib import request

from pip import main


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

	def receiveOperation(self):
		json_to_recv = self.UDP_socket.recvfrom(self.buffer_size)
		operation = json_to_recv[0]
		server_address_port = json_to_recv[1]

		oper = operation.decode()

		operation_json = json.loads(oper)

		if operation_json["seq"] == self.seq:
			if operation_json["type"] == "request":
				if operation_json["fin"] == True:
					if operation_json["request"] == "write":
						operation = ""
						print("CONVERTIR LA OPERACION")
						result = 0

						self.send_verification(server_address_port)

						self.send_result(server_address_port, result, operation)

						self.recv_verification()
					else:
						print("Request erroneo")
				else:
					print("TIENE QUE HACERSE FRACCIONADO")
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

	def receive_request(self):
		json_to_recv = UDPServer.recvfrom(self.buffer_size)
		request = json_to_recv[0]
		server_address_port = json_to_recv[1]
		req = request.decode()

		request_json = json.loads(req)

		if request_json["type"] == "disconnect":
			self.UDP_socket.close()
		else:
			print("RECIBE OPERACION")

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
