import argparse
import json
import random
import socket

# Lee desde consola los argumentos de manera desordenada
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', type=str)
parser.add_argument('-p', '--password', type=str,)
args = parser.parse_args()

class Client:
	def __init__(self, address, port):
		self.socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ip = address
		self.address_port = (address, port)
		
		self.buffer_size = 128
		self.seq = random.randint(0, 100) #0
		self.ack = 0
		self.ack_expected = 0
		self.fin = True

	def option_quit(self):
		data_json = {"seq": self.seq, "type": "disconnect"}
		self.send_json(data_json)
		self.socket_TCP.close()
	
	def send_request(self):
		self.validate_user_permissions(True)

	def send_verification(self):
		data_json = {"type": "ack", "ack": self.ack_expected, "seq": self.seq}
		self.send_json(data_json)

	def recv_operation(self):
		#TODO: Refactor this:
		# Recibe el resultado
		bytes_recv = self.socket_TCP.recv(self.buffer_size) 
		message_recv = bytes_recv
		serverAddressPort = bytes_recv[1]
		msg = message_recv.decode()
		json_msg = json.loads(msg)

		if json_msg["type"] == "request":
			if json_msg["fin"] == True:
				if json_msg["request"] == "write":
					print(json_msg["result"])

					# Envia la verificacion que le llego bien el resultado
					self.send_verification()
					
					# Envia la solicitud
					self.send_request()
				else:
					print("Request erroneo")
			else:
				print("DEBE ESPERAR LO FRACCIONADO") # OJOOO
		else:
			print("Type erroneo")

	def send_json(self, data_json):
		bytesToSend = str.encode(json.dumps(data_json))
		# Envia el json
		self.socket_TCP.sendall(bytesToSend)

	def send_operation(self):
		operation = input("Ingrese la operacion: ")
		data_json = {"seq": self.seq, "type": "request",
                    "fin": self.fin, "request": "write", "oper": operation}
		
		json_string = json.dumps(data_json)
		
		if (len(json_string.encode('utf-8')) <= 128): # OJOO
			# Envia la solicitud
			self.send_json(data_json)

			# Recibe la operacion
			self.recv_operation()

	def validate_user_permissions(self, can_write):
		rep = True
		while(rep):
			permission = input("¿Que necesita?: -r = read, -w = write y q = exit \n")

			if (permission == '-w'):
				if(can_write == True):
					self.send_operation()
					rep = False
				else:
					print("Permiso denegado: Usted no cuenta con permisos de escritura")

			elif(permission == '-r'):
				index = permission = input("Digite el numero de pagina que desee conocer")
				#LEEE DEL DOCUMENTO
				rep = False
			elif(permission == 'q'):
				rep = False
				self.option_quit()
			else:
				print("Comando invalido")

	def authentication(self, user, password):
		valid_user = False
		can_write = False

		with open('users.json') as file:
			data = json.load(file)
			for users in data['users']:
				if (users['username'] == user):
					if (users['password'] == password):
						can_write = users['canWrite']
						valid_user = True
					
		if (valid_user == True):
			# Pregunta que quiere hacer el usuario
			self.validate_user_permissions(can_write)
		else:
			print("[Cerrando conexion]: Usuario o contraseña invalida")
			self.socket_TCP.close()
	
	def main(self, user, password):
		self.socket_TCP.connect(self.address_port)
		try:
			self.authentication(user, password)
		finally:
			self.socket_TCP.close()


if __name__ == "__main__":
	client = Client("127.0.0.1", 50000) 
	client.main(args.user, args.password) 
