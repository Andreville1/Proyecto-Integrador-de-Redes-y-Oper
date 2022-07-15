import socket
import json
from  datetime import datetime

class Server(object):
    def __init__(self, address, port):
        self.address_port = (address, port) # Contiene la direccion ip y puerto a conectar

        # Encabezados
        self.mimetype = "" # Content-Type
        self.ContentLength = 0 # Content-Length
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

    def authentication(self, username, password):
        valid_user = False
        with open('users.json') as file:
            data = json.load(file)
            for users in data['users']:
                if (users['username'] == username[1]):
                    if (users['password'] == password[1]):
                        valid_user = True
        
        return valid_user
    
    def serve_home_page(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<meta charset=\"ascii\"/>\n"
        body += "<title> Calculator </title>\n"
        body += "<style>body {font-family: monospace}</style>\n"
        body += "<h1> Calculator </h1>\n"
        body += "<form method=\"get\" action=\"/calculate\">\n"
        
        body += "<label for=\"username\">Username</label>\n"
        body += "<input type=\"text\" name=\"username\" required/>\n"

        body += "<label for=\"password\">Password</label>\n"
        body += "<input type=\"text\" name=\"password\" required/>\n"

        body += "<label for=\"operation\">Operation</label>\n"
        body += "<input type=\"text\" name=\"operation\" required/>\n"
        body += "<button type=\"submit\">Calculate</button>\n"

        body += "</form>\n"
        body += "</html>\n"

        return body

    def valid_request(self, operation, result):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<meta charset=\"ascii\"/>\n"
        body += "<title> Result </title>\n"
        body += "<style>body {font-family: serif} .err {color: yellow}</style>\n"
        body += "<h1> Result of operation "
        body += str(operation)
        body += "</h1>\n"
        body += "<p>"
        body += str(result)
        body += "</p>\n"
        body += "<hr><p><a href=\"/\">Back</a></p>\n"
        body += "</html>\n"

        return body
    
    def invalid_authentication(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<meta charset=\"ascii\"/>\n"
        body += "<title> Authentication </title>\n"
        body += "<style>body {font-family: monospace} .err {color: red}</style>\n"
        body += "<h1 class=\"err\"> Invalid authentication </h1>\n"
        body += "<p> Try again </p>\n"
        body += "<hr><p><a href=\"/\">Back</a></p>\n"
        body += "</html>\n"

        return body

    def invalid_page(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<title> Error 404 (Not Found) </title>\n"
        body += "<style>body {font-family: monospace} .err {color: red}</style>\n"
        body += "<h1 class=\"err\"> Error 404: Not Found </h1>\n"
        body += "<p>Page not found</p>\n"
        body += "<hr><p><a href=\"/\">Back</a></p>\n"
        body += "</html>\n"

        return body

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
            print("request", request)

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

            # Booleano para saber si es 404
            can_continue = True

            # Si no escribe la operacion de primeras, muestra la pantalla principal
            is_empty = False
            if(requesting_operation == '/'):
                is_empty = True
            else :
                try:
                    # Separa los datos que recibe (/calculate?username=username, password=password, operation=operation)
                    string_operation = requesting_operation.split('&')
                    # Separa el username (/calculate?username, username)
                    username = string_operation[0].split('=')
                    # Separa el paswword (password, password)
                    password = string_operation[1].split('=')
                    # Separa la operacion (operation, operation)
                    operation = string_operation[2].split('=')
                    
                    #Verificacion para 404
                    username[0] += "="
                    password[0] = "&" + password[0] + "="
                    operation[0] = "&" + operation[0] + "="
                    #print("Client request:", string_operation)
                    #print(username, password, operation)

                    # Convierte en bytes la operacion
                    self.ContentLength = len(operation[1])
                    #print(self.ContentLength)

                    # Error 404     
                    if (username[0] != "/calculate?username=") or (password[0] != "&password=") or (operation[0] != "&operation="):
                        header = 'HTTP/1.1 404 Not Found\n\n'
                        response = self.invalid_page()
                        can_continue = False
                        is_empty = True
                    # Validacion
                    elif self.authentication(username, password) == False:
                        header = 'HTTP/1.1 400 Bad Request\n\n'
                        response = self.invalid_authentication()
                        can_continue = False
                except Exception as exception404: # Error 404
                    header = 'HTTP/1.1 404 Not Found\n\n'
                    response = self.invalid_page()
                    can_continue = False

                             
            if can_continue == True:
                # Calcula la operacion
                if is_empty == False:
                    operation[1] = operation[1].replace("%2B", "+")
                    operation[1] = operation[1].replace("%2F", "/")
                    result = eval(operation[1])
                    response = self.valid_request(operation[1], result)
                    #print(response)
                else: # Abre la pagina principal
                    response = self.serve_home_page()
                
                
                # Indica que la conexion funciono
                header = 'HTTP/1.1 200 OK\n'
                # Establece que se va a mostrar un html
                self.mimetype = 'text/html'
                # Agrega que lo que se va a mostrar es un html
                header += 'Content-Type: ' + str(self.mimetype) + '\n\n'

                # Llama a la funcion que guarda la bitacora
                if self.ContentLength != 0:
                    self.ContentLength = str(self.ContentLength)
                    self.save_bin()

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