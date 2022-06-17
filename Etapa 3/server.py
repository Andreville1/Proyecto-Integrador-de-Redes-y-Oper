import json
import random
import socket
import threading
import sys
from xmlrpc.client import TRANSPORT_ERROR

class Server(object):
	def __init__(self, address, port):
		self.ip = address # OJO
		self.address_port = (address, port)

		self.buffer_size = 128
		self.seq = seq = random.randint(0, 100) #10
		self.ack_expected = 0
		self.ack = 0
		self.fin = True

		# Bellman Ford
		self.graph = []
		self.lines = 0
		self.source = ''
		self.distanceNeigh = {}
		self.node = ""

		self.can_continue = False
		self.neigh_ip = {}
		self.neigh_port = {}

		self.can_listen = True

	def recv_verification(self, connection):
		bytes_recv = connection.recv(self.buffer_size)
		message_recv = bytes_recv[0] # verification = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = bytes_recv.decode()
		json_msg = json.loads(msg) # verification_json = json.loads(veri)

		self.recv_request(connection, self.address_port)

	def send_result(self, address, result, operation, connection):
		data_json = {"seq": self.seq, "type": "request", "fin": self.fin,
				"request": "write", "result": result, "oper": operation}
		bytesToSend = str.encode(json.dumps(data_json))
		# Envia el resultado
		connection.sendall(bytesToSend)

	def Bellman_Ford(self):
		dist = [float("Inf")] * self.lines
		dist[ord(self.source)-65] = 0

		for _ in range(self.lines - 1):
			for u, v, w in self.graph:
				#print(u, v, w)
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w
		
		for u, v, w in self.graph:
			if dist[u] != float("Inf") and dist[u] + w < dist[v]:
				print("Graph contains negative weight cycle")
				return
		
		#print("Nodo	Distancia desde el nodo principal")
		for index in range(self.lines):
			#print("{0}\t\t{1}".format(chr(index+65), dist[index]))
			self.node = chr(index+65)
			if (dist[index] == float("Inf")):
				self.distanceNeigh[self.node] = -1
			else:
				self.distanceNeigh[self.node] = dist[index]
		
		print(self.distanceNeigh)

	def calc_operation(self, operation_json, address, connection):
		operation = operation_json["oper"]
		operation = operation.replace("**", "^")
		result = eval(operation)

		# LO NUEVO COMIENZA ACA
		#print(data_json)
		# LO NUEVO TERMINA ACA

		# Envia el resultado
		self.send_result(address, result, operation, connection)

		self.recv_verification(connection)
	
	def recv_request(self, connection, client_address):
		
		# Recibe la solicitud
		bytes_recv = connection.recv(self.buffer_size)
		message_recv = bytes_recv[0] # request = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = bytes_recv.decode()
		json_msg = json.loads(msg)

		if json_msg["type"] == "disconnect": # Caso en que el cliente se quiere desconectar
			connection.close()
		elif json_msg["type"] == "vector": # Caso en que le llega un vector de un nodo
			self.cola_de_entrada.append(json_msg["conn"])
			print("Estoy recibiendo un vector", self.cola_de_entrada)
		elif json_msg["type"] == "operation": # Caso en que recibe una operacion de un nodo
			if (json_msg["destination"] == self.source):
				self.cola_de_entrada.append(json_msg["operation"])
				print("Estoy recibiendo un fragmento de operacion", self.cola_de_entrada)
			else:
				self.cola_de_salida.append(json_msg["operation"])
				print("Estoy guardando un fragmento de operacion", self.cola_de_salida)
		else: # Caso en que recibe un paquete del cliente
			self.calc_operation(json_msg, address, connection)


	def recv_json(self, connection):
		# recv from client
		msg_from_server = connection.recv(self.buffer_size)
		message_recv = msg_from_server[0]
		address = msg_from_server[1] # server_address_port = json_to_recv[1]
		msg = msg_from_server.decode()
		json_msg = json.loads(msg)
		return json_msg, address

	def send_json(self, data_json, socket_TCP_connect):
		bytes_to_send = str.encode(json.dumps(data_json))
		socket_TCP_connect.sendall(bytes_to_send)

	def listen(self):
		cont = 0
		while True:
			if (self.can_listen == True): # Se pone a esuchar por conexiones
				socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket_TCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				socket_TCP.bind(self.address_port)
				print("Escuchando")
				socket_TCP.listen(7)
				socket_TCP.settimeout(5)
				try:
					connection, client_address = socket_TCP.accept()
					threading.Thread(target = self.recv_request, args = (connection,client_address)).start()
				except: 
					self.can_listen = False
					socket_TCP.close()

			else: # Se pone a conectar con un nodo vecino
				socket_TCP_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket_TCP_connect.settimeout(2)
				try:
					print("Conectando")
					new_address = (self.neigh_ip[cont], self.neigh_port[cont])
					
					socket_TCP_connect.connect(new_address)
					cont = cont + 1
					if (cont == len(self.neigh_ip)):
						cont = 0
						self.can_listen = True
					data_json = {"type": "vector", "node": chr(self.source+65), "conn": self.distanceNeigh}
					self.send_json(data_json, socket_TCP_connect)
				except:
					cont = cont + 1
					if (cont == len(self.neigh_ip)):
						cont = 0
						self.can_listen = True
				
		
	def calc_table(self):
		self.source = sys.argv[1]
		cont = 0
		file = open('topologia.csv', 'r')
		for line in file:
			self.lines = self.lines + 1

			# Remueve salto de linea
			line = line.rstrip()

			separator = ','
			# Convierte la linea en un arreglo
			list = line.split(',')

			#print(lines)
			#print(list[0] + "/" + list[1] + "/" + list[2] + "/" + list[3] + "/" + list[4]
			#+ "/" + list[5] + "/" + list[6])

			# Agregue aristas
			self.graph.append([ord(list[0])-65, ord(list[3])-65, int(list[6])])

			#print(self.source)

			# Guarda la IP y puertos de sus vecinos
			if (list[0] == self.source): 
				self.neigh_ip[cont] = str(list[4])
				self.neigh_port[cont] = int(list[5])
				cont = cont + 1
		
		#print(self.graph)
		#print(self.source)

		self.Bellman_Ford()
		self.can_continue = True

def main():
	server = Server("127.0.0.1", 8080)
	server.calc_table()
	server.listen()

if __name__ == "__main__":
	main()

