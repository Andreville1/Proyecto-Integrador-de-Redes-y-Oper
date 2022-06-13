import json
import random
import socket

class Server:
	def __init__(self, address, port):
		self.ip = address # OJO
		self.address_port = (address, port)
		self.buffer_size = 128
		self.seq = seq = random.randint(0, 100) #10
		self.ack_expected = 0
		self.ack = 0
		self.fin = True

		self.graph = []
		self.lines = 0
		self.source = ''

	def recv_verification(self, connection):
		bytes_recv = connection.recv(self.buffer_size)
		message_recv = bytes_recv[0] # verification = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = bytes_recv.decode()
		json_msg = json.loads(msg) # verification_json = json.loads(veri)

		self.recv_request(connection)

	def send_result(self, address, result, operation, connection):
		data_json = {"seq": self.seq, "type": "request", "fin": self.fin,
				"request": "write", "result": result, "operation": operation}
		bytesToSend = str.encode(json.dumps(data_json))
		# Envia el resultado
		connection.sendall(bytesToSend)

	def Bellman_Ford(self, source):
		dist = [float("Inf")] * self.lines
		dist[source] = 0

		for _ in range(self.lines - 1):
			for u, v, w in self.graph:
				print(u, v, w)
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w
		
		for u, v, w in self.graph:
			if dist[u] != float("Inf") and dist[u] + w < dist[v]:
				print("Graph contains negative weight cycle")
				return
		
		print("Nodo	Distancia desde el nodo principal")
		for index in range(self.lines):
			print("{0}\t\t{1}".format(chr(index+65), dist[index]))

	def calc_operation(self, operation_json, address, connection):
		operation = operation_json["operation"]
		operation = operation.replace("**", "^")
		result = eval(operation)
		
		file = open('topologia.csv', 'r')
		for line in file:
			self.lines = self.lines + 1

			# Remueve salto de linea
			line = line.rstrip()

			separator = ','
			# Convierte la linea en un arreglo
			list = line.split(',')

			if (self.lines == 1):
				self.source = ord(list[0])-65

			#print(lines)
			#print(list[0] + "/" + list[1] + "/" + list[2] + "/" + list[3] + "/" + list[4]
			#+ "/" + list[5] + "/" + list[6])

			# Agregue aristas
			self.graph.append([ord(list[0])-65, ord(list[3])-65, int(list[6])])
		
		#print(self.graph)
		#print(self.source)

		self.Bellman_Ford(self.source)
		

		# Envia el resultado
		self.send_result(address, result, operation, connection)

		self.recv_verification(connection)
	
	def recv_request(self, connection):
		
		# Recibe la solicitud
		bytes_recv = connection.recv(self.buffer_size)
		message_recv = bytes_recv[0] # request = json_to_recv[0]
		address = bytes_recv[1] # server_address_port = json_to_recv[1]
		msg = bytes_recv.decode()
		json_msg = json.loads(msg)

		if json_msg["type"] == "disconnect":
			connection.close()
		else:
			self.calc_operation(json_msg, address, connection)

	def recv_json(self, connection):
		# recv from client
		msg_from_server = connection.recv(self.buffer_size)
		message_recv = msg_from_server[0] # operation = json_to_recv[0]
		address = msg_from_server[1] # server_address_port = json_to_recv[1]
		msg = msg_from_server.decode()
		json_msg = json.loads(msg) # operation_json = json.loads(oper)
		return json_msg, address

	def main(self):
		while True:
			self.socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket_TCP.bind(self.address_port)
			self.socket_TCP.listen(2)
			connection, client_address = self.socket_TCP.accept()

			self.recv_request(connection)

if __name__ == "__main__":
	server = Server("127.0.0.1", 8080)
	server.main()
