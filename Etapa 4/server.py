import socket

class Server(object):
    def __init__(self, address, port):
        self.address_port = (address, port) # Contiene la direccion ip y puerto a conectar
    
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
            # Tipo de metodo (GET/POST)
            method = request_list[0]
            # Lo que solicita el cliente
            requesting_operation = request_list[1]
            print("method and requesting_operation:", method, requesting_operation)

            # Limpia la solicitud para que solo quede la operacion (si la hay)
            operation = requesting_operation.split('?')[0]
            operation = operation.lstrip('/')
            print("Client request:",operation)
            
            # Si no escribe la operacion de primeras, muestra la pantalla principal
            if(operation == ''):
                operation = 'homepage.html'

            try:
                # Calcula la operacion
                response = eval(operation)
                print(response)
                
                #Indica que la conexion funciono
                header = 'HTTP/1.1 200 OK\n'
                # Establece que se va a mostrar un html
                mimetype = 'text/html'
                # Agrega que lo que se va a mostrar es un html
                header += 'Content-Type: '+str(mimetype)+'\n\n'

            except Exception as exception404:
                print("ACA VA EL ERROR 404")

            # Codifica lo que se va a enviar
            final_response = header.encode('utf-8')
            # Agrega la respuesta para enviarla
            final_response += str(response).encode('utf-8')
            # Envia el header y la respuesta
            connection.send(final_response)
            # Cierra la conexion
            connection.close()

def main():
    server = Server('127.0.0.1', 8888)
    server.run()

if __name__ == "__main__":
    main()