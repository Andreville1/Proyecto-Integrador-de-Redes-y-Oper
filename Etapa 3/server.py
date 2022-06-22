import json
import random
import socket
import threading
import sys

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
		self.graph = {}
		self.lines = 0
		self.source = ''
		self.distanceNeigh = []
		self.node = ""
		self.prev = ""
		self.node_data = {}

		self.can_continue = False
		self.neigh_ip = {}
		self.neigh_port = {}

		self.can_listen = True

		self.cola_de_entrada = []
		self.cola_de_salida = {}

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

	"""def Bellman_Ford(self):
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
		
		#print("Nodo	Distancia desde el nodo principal") # A:
		for index in range(self.lines):
			#print("{0}\t\t{1}".format(chr(index+65), dist[index]))
			self.node = chr(index+65)
			if (dist[index] == float("Inf")):
				self.distanceNeigh[self.node] = -1
			else:
				self.distanceNeigh[self.node] = dist[index]
		
		print(self.distanceNeigh)
	"""

	def Bellman_Ford_update(self, graph):
		inf = sys.maxsize
		for i in range(len(graph)- 1):
			#print('Iteration '+str(i))
			for itr in graph:
				for neighbor in graph[itr]:
					print(neighbor, graph[itr])
					cost = self.node_data[itr]['cost'] + graph[itr][neighbor]
					if cost < self.node_data[neighbor]['cost']:
						self.node_data[neighbor]['cost'] = cost
						if self.node_data[neighbor]['cost'] == inf:
							self.node_data[neighbor]['pred'] = self.node_data[itr]['pred'] + [itr]
						else:
							self.node_data[neighbor]['pred'].clear()
							self.node_data[neighbor]['pred'] = self.node_data[itr]['pred'] + [itr]
		
			#print("Original", self.node_data)
		
		for neighbor in graph:
			if (self.node_data[neighbor]['cost'] > 10):
				data = {"target":neighbor,"weight":-1}
				self.distanceNeigh.append(data)
			else:
				data = {"target":neighbor,"weight":self.node_data[neighbor]['cost']}
				self.distanceNeigh.append(data)

		# print(self.distanceNeigh)
		#print("Actualizado", self.node_data)

	def Bellman_Ford(self, graph):
		inf = sys.maxsize
		self.node_data = graph.copy()
		data = {'cost':inf,'pred':[]}
	
		for index in graph:
			self.node_data[index] = data.copy()

		self.node_data[self.source]['cost'] = 0
		for i in range(len(graph)- 1):
			#print('Iteration '+str(i))
			for itr in graph:
				for neighbor in graph[itr]:
					cost = self.node_data[itr]['cost'] + graph[itr][neighbor]
					if cost < self.node_data[neighbor]['cost']:
						self.node_data[neighbor]['cost'] = cost
						if self.node_data[neighbor]['cost'] == inf:
							self.node_data[neighbor]['pred'] = self.node_data[itr]['pred'] + [itr]
						else:
							self.node_data[neighbor]['pred'].clear()
							self.node_data[neighbor]['pred'] = self.node_data[itr]['pred'] + [itr]
		
			#print("Original", self.node_data)
		
		for neighbor in graph:
			if (self.node_data[neighbor]['cost'] > 10):
				data = {"target":neighbor,"weight":-1}
				self.distanceNeigh.append(data)
			else:
				data = {"target":neighbor,"weight":self.node_data[neighbor]['cost']}
				self.distanceNeigh.append(data)

		# print(self.distanceNeigh)
		print("Original", self.node_data)
		
	def calc_operation(self, operation_json, address, connection):
		#operation = operation_json["oper"]
		#operation = operation.replace("**", "^")
		#result = eval(operation)
		data_json = {"seq": self.seq, "type": "request", "fin": self.fin,
					"request": "write", "oper": operation_json["oper"]}
		self.send_json(data_json, connection)
		# Envia el resultado
		#self.send_result(address, result, operation, connection)

		self.recv_verification(connection)
	
	def compare_tables(self, conn):
		cont = 0
		for neighboor in self.node_data:
			if (self.node_data[neighboor]['cost'] > conn[cont]["weight"] and conn[cont]["weight"] !=0):
				self.node_data[neighboor]['cost'] = conn[cont]["weight"]
			cont += 1
		
		#print("Modificado", self.node_data)


	def recv_request(self, connection, client_address):
		# Recibe la solicitud
		bytes_recv = connection.recv(1024)
		message_recv = bytes_recv[0] # request = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = bytes_recv.decode()
		json_msg = json.loads(msg)

		if json_msg["type"] == "disconnect": # Caso en que el cliente se quiere desconectar
			connection.close()
		elif json_msg["type"] == "vector": # Caso en que le llega un vector de un nodo
			# print(json_msg["conn"])
			# Compare tabla de vectores
			self.compare_tables(json_msg["conn"])
			self.Bellman_Ford_update(self.graph)
		elif json_msg["type"] == "operation": # Caso en que recibe una operacion de un nodo
			if (json_msg["destination"] == self.source):
				self.cola_de_entrada.append(json_msg["operation"])
				print("Estoy recibiendo un fragmento de operacion", self.cola_de_entrada)
				# ESTA PARTE LE TOCA A LUCIA Y ADRIAN
			else:
				self.cola_de_salida.update({json_msg["destination"]:json_msg["operation"]}) # A: 5+5
				print("Estoy guardando un fragmento de operacion", self.cola_de_salida)
				# ENVIAR A LOS OTROS NODOS
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
				# print("Escuchando en", self.address_port)
				socket_TCP.bind(self.address_port)
				socket_TCP.listen(7)
				socket_TCP.settimeout(5)
				try:
					connection, client_address = socket_TCP.accept()
					threading.Thread(target = self.recv_request, args = (connection,client_address)).start()
					socket_TCP.close()
				except: 
					self.can_listen = False
					socket_TCP.close()

			else: # Se pone a conectar con un nodo vecino
				socket_TCP_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket_TCP_connect.settimeout(2)
				try:
					# Agregar vector de vecinos
					new_address = (self.neigh_ip[cont], self.neigh_port[cont])
					# print("Conectando en", new_address)
					socket_TCP_connect.connect(new_address)
					cont = cont + 1
					if (cont == len(self.neigh_ip)):
						cont = 0
						self.can_listen = True
					"""
					if (table_vector == TRUE): #YA SE TERMINO EL RECORRIDO DE LAS TABLAS
						# ENVIA OPERACION
					ELSE: # NO SE HA TEMRINADO EL RECORRIDO
							data_json = {"type": "vector", "node": self.source, "conn": self.distanceNeigh}
					"""
					data_json = {"type": "vector", "node": self.source, "conn": self.distanceNeigh}
					#print(data_json)
					self.send_json(data_json, socket_TCP_connect)
				except:
					cont = cont + 1
					if (cont == len(self.neigh_ip)):
						cont = 0
						self.can_listen = True
					socket_TCP_connect.close()
		
	def calc_table(self):
		self.source = sys.argv[1]
		self.prev = self.source
		cont = 0
		neigh = {}
		file = open('topologia2.csv', 'r')
		for line in file:
			self.lines = self.lines + 1

			# Remueve salto de linea
			line = line.rstrip()

			# Convierte la linea en un arreglo
			list = line.split(',')

			#print(lines)
			#print(list[0] + "/" + list[1] + "/" + list[2] + "/" + list[3] + "/" + list[4]
			#+ "/" + list[5] + "/" + list[6])
			
			# Agregue aristas
			if (self.prev == list[0]): # A == B
				neigh[list[3]] = int(list[6])
				#neigh.update({list[3]:list[6]}) 
				self.graph[list[0]] = neigh
				#print(self.graph)
			else: 
				neigh = {}
				#neigh.clear()
				neigh[list[3]] = int(list[6])
				#neigh.update({list[3]:list[6]}) 
				self.graph[list[0]] = neigh
				#self.graph.update({list[0]:neigh})
				#print(self.graph)

			self.prev = list[0]
			#self.graph.append([ord(list[0])-65, ord(list[3])-65, int(list[6])])
			#print(self.source)

			# Guarda la IP y puertos de sus vecinos
			if (list[0] == self.source): 
				self.address_port = (str(list[1]), int(list[2]))
				self.neigh_ip[cont] = str(list[4])
				self.neigh_port[cont] = int(list[5])
				cont = cont + 1
		
		neigh = {}
		temp = ord(self.prev)
		self.graph[chr(temp+1)] = neigh
		# print(self.graph)
		# print("HOla", self.graph)

		self.Bellman_Ford(self.graph)
		self.can_continue = True

def set_address():
	source = sys.argv[1]
	file = open('topologia2.csv', 'r')
	enter = True
	for line in file:

		# Remueve salto de linea
		line = line.rstrip()

		separator = ','
		# Convierte la linea en un arreglo
		list = line.split(',')
		#print(list)
		if(source == list[0] and enter == True):
			address_port = (str(list[1]), int(list[2]))
			enter = False
	
	return address_port, source

def main():
	tuple = set_address()
	server = Server(tuple[0], tuple[1])
	server.calc_table()
	server.listen()

if __name__ == "__main__":
	main()

