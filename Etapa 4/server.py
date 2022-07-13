import socket
import json
from  datetime import datetime

class Server(object):
    def __init__(self, address, port):
        self.address_port = (address, port) # Contiene la direccion ip y puerto a conectar

        # Encabezados
        self.mimetype = "" # Content-Type
        self.ContentLength = "" # Content-Length
        self.Host = "" # Host
        self.Date = "" # Date

        # Bitacora
        self.bin = {} # Diccionario para guardar la bitacora
        self.bin['Bitacora'] = [] # Crea en el diccionario una key para la bitacora

    def save_bin(self):
        # Crea el json de la bitacora
        data_json = {"Content-Type": self.mimetype, "Content-Length": self.ContentLength, "Host": self.Host,
				     "Date": self.Date}

        # Guarda el json en la key de bitacora
        self.bin['Bitacora'].append(data_json)

        # Guarda el diccionario de la bitacora en un archivo .json
        with open('bitacora.json', 'w') as file:
            json.dump(self.bin, file, indent=4)

    def run(self):
        # TOdo el proceso de creacion de sockets
        socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_TCP.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
        socket_TCP.bind(self.address_port)
        socket_TCP.listen(1)
        print('Escuchando en', self.address_port)

        while True:
            # Acepta y establece conexion con el cliente
            connection , address = socket_TCP.accept()
            request = connection.recv(1024).decode('utf-8')
            #print("request", request)

            # Guarda lo que recibe en un arreglo
            request_list = request.split(' ')
            #print(request_list)

            # Tipo de metodo (GET/POST)
            method = request_list[0]
            # Lo que solicita el cliente
            requesting_operation = request_list[1]
            # Host del server
            self.Host = request_list[3].split("\r", 1)[0]
            # Fecha del server
            self.Date = str(datetime.now())
            #print("method, requesting_operation, host and date:", method, requesting_operation, self.Host, self.Date)

            # Limpia la solicitud para que solo quede la operacion (si la hay)
            operation = requesting_operation.split('?')[0]
            operation = operation.lstrip('/')
            #print("Client request:",operation)

            # Convierte en bytes la operacion
            self.ContentLength = str(len(operation))
            #print(self.ContentLength)
            
            # Si no escribe la operacion de primeras, muestra la pantalla principal
            is_empty = False
            if(operation == ''):
                operation = 'homepage.html'
                is_empty = True

            try:
                # Calcula la operacion
                if is_empty == False:
                    response = eval(operation)
                    #print(response)
                else: # Abre la pagina principal
                    file = open(operation, 'rb')
                    response = file.read()
                    file.close()
                
                
                #Indica que la conexion funciono
                header = 'HTTP/1.1 200 OK\n'
                # Establece que se va a mostrar un html
                self.mimetype = 'text/html'
                # Agrega que lo que se va a mostrar es un html
                header += 'Content-Type: ' + str(self.mimetype) + '\n\n'

                # Llama a la funcion que guarda la bitacora
                self.save_bin()
            except Exception as exception404:
                print("ACA VA EL ERROR 404")

            # Codifica lo que se va a enviar
            final_response = header.encode('utf-8')
            # Agrega la respuesta para enviarla
            if is_empty == False:
                final_response += str(response).encode('utf-8')
            else:
                final_response += response

            # Envia el header y la respuesta
            connection.send(final_response)
            # Cierra la conexion
            connection.close()

def main():
    server = Server('127.0.0.1', 8888)
    server.run()

if __name__ == "__main__":
    main()