import socket
import json
from  datetime import datetime
from math import *
names = {'sqrt': sqrt}

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

    def get_code404(self):
        return 'HTTP/1.1 404 Not Found\n\n'

    def get_code200(self):
         # Indica que la conexion funciono
        header = 'HTTP/1.1 200 OK\n'
        # Establece que se va a mostrar un html
        self.mimetype = 'text/html'
        # Agrega que lo que se va a mostrar es un html
        header += 'Content-Type: ' + str(self.mimetype) + '\n\n' 

        return header 

    def get_parameters(self, method, request_list):
        if method == "GET":
            requesting_operation = request_list[1]
            #print("requesting_operation", requesting_operation)
            return requesting_operation
        elif method == "POST":
            requesting_operation = request_list[len(request_list)-1]
            requesting_operation = requesting_operation.replace("?1\r\n\r\n", "")
            #print("requesting_operation", requesting_operation)
            return requesting_operation

    def serve_home_page(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<meta charset=\"ascii\"/>\n"
        body += "<title> Calculator </title>\n"
        body += "<style>body {background: gray; color: white}</style>\n"
        body += "<h1> Calculator </h1>\n"
        body += "<body><form method=\"POST\" action=\"/calculate\">\n"
        
        body += "<label for=\"username\">Username</label>\n"
        body += "<input type=\"text\" name=\"username\" required/>\n"

        body += "<label for=\"password\">Password</label>\n"
        body += "<input type=\"text\" name=\"password\" required/>\n"
        body += "<button type=\"submit\">Login</button>\n"

        body += "</form></body>\n"
        body += "</html>\n"

        return body

    def serve_calculate_page(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<meta charset=\"ascii\"/>\n"
        body += "<title> Calculator </title>\n"
        body += "<style>body {background: gray; color: white}</style>\n"
        body += "<h1> Calculator </h1>\n"
        body += "<form method=\"GET\" action=\"/calculate\">\n"

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
        body += "<style>body {background: gray; color: white} .err {color: yellow}</style>\n"
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
        body += "<style>body {background: gray; color: white} .err {color: red}</style>\n"
        body += "<h1 class=\"err\"> Invalid authentication </h1>\n"
        body += "<p> Try again </p>\n"
        body += "<hr><p><a href=\"/\">Back</a></p>\n"
        body += "</html>\n"

        return body

    def invalid_page(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<title> Error 404 (Not Found) </title>\n"
        body += "<style>body {background: gray; color: white} .err {color: red}</style>\n"
        body += "<h1 class=\"err\"> Error 404: Not Found </h1>\n"
        body += "<p>Page not found</p>\n"
        body += "<hr><p><a href=\"/\">Back</a></p>\n"
        body += "</html>\n"

        return body
    
    def invalid_operation(self):
        body = "<!DOCTYPE html>\n"
        body += "<html lang=\"en\">\n"
        body += "<title> Error 400 (Bad Request) </title>\n"
        body += "<style>body {background: gray; color: white} .err {color: red}</style>\n"
        body += "<h1 class=\"err\"> Error 400: Bad Request </h1>\n"
        body += "<p>Operation not valid</p>\n"
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
            print("request=", request)

            # Guarda lo que recibe en un arreglo
            request_list = request.split(' ')
            #print(request_list)

            # Tipo de metodo (GET/POST)
            method = request_list[0]
            #print("method=", method, "\n")

            # Guarda lo que escribe el cliente (parametros)
            requesting_operation = self.get_parameters(method, request_list)

            # Host del server
            self.Host = request_list[3].split("\r", 1)[0]
            # Fecha del server
            self.Date = str(datetime.now())
            #print("method, requesting_operation, host and date:", method, requesting_operation, self.Host, self.Date)
            
            if method == "GET":
                if(requesting_operation == '/'):
                    # Indica que la conexion funciono
                    header = self.get_code200()
                    #print("Header", header)
                    response = self.serve_home_page()
                else: # Calcule la operacion
                    #print("requesting_operation=", requesting_operation, "\n") # calculate?operation=1%2B1 
                    try: 
                        link_operation = requesting_operation.split('?') # calculate, operation=1%2B1 
                        #print("link_operation=", link_operation, "\n")
                    except:
                        pass

                    if link_operation[0] != "/calculate": # Valida link (404)
                        header = self.get_code404()
                        response = self.invalid_page()

                    else: # Todo correcto

                        # Separa la operacion (operation, operation)
                        operation = requesting_operation.split('=') # /calculate?operation, 1%2B1
                        operation[0] += "=" # # /calculate?operation=, 1%2B1
                        #print("operation=", operation)

                        if (operation[0] == "/calculate?operation="): # URL correcto
                            # Convierte en bytes la operacion
                            self.ContentLength = len(operation[1])
                            #print(self.ContentLength)

                            # Remplaza para calcular la operacion
                            operation[1] = operation[1].replace("%2B", "+")
                            operation[1] = operation[1].replace("%2F", "/")
                            operation[1] = operation[1].replace("%28", "(")
                            operation[1] = operation[1].replace("%29", ")")


                            try:
                                #print(operation[1])
                                result = eval(operation[1], names)
                                #print("OPERATION", operation[1])
                                #print("RESULT", result)
                                response = self.valid_request(operation[1], result)
                                #print("RESPONSE ",response)
                            except Exception as exception400: # Error 400
                                #print("ERROR del 400")
                                header = 'HTTP/1.1 400 Bad Request\n\n'
                                response = self.invalid_operation()
                                #body = str(response).encode('utf-8')

                            # Llama a la funcion que guarda la bitacora
                            if self.ContentLength != 0:
                                self.ContentLength = str(self.ContentLength)
                                self.save_bin()
                        else: # Error 404
                            header = self.get_code404()
                            response = self.invalid_page()
            elif method == "POST":
                # Booleano para saber si es 404
                can_continue = True  
                try:
                    #print("requesting_operation=", requesting_operation, "\n")
                    # Separa los datos que recibe (/calculate?username=username, password=password, operation=operation)
                    string_operation = requesting_operation.split('&')
                    # Separa el username (/calculate?username, username)
                    username = string_operation[0].split('=')
                    # Separa el paswword (password, password)
                    password = string_operation[1].split('=')


                    
                    #Verificacion para 404
                    username[0] += "="
                    password[0] = "&" + password[0] + "="
                    #print("Client request:", string_operation)
                    #print(username, password)

                    if self.authentication(username, password) == False: # Valida autenticacion (400)
                        header = 'HTTP/1.1 401 Unauthorized\n\n'
                        response = self.invalid_authentication()
                        can_continue = False
                    else: # Todo correcto
                        response = self.serve_calculate_page()

                except Exception as exception404: # Error 404
                    #print("ERROR del except")
                    header = self.get_code404()
                    response = self.invalid_page()
                    can_continue = False
      
                if can_continue == True:
                    # Validacion correcta y procede a mandar a la pagina de la calculadora
                    header = self.get_code200() 
                    #print("Header", header) 

            # Codifica lo que se va a enviar
            final_response = header.encode('utf-8')
            # Agrega la respuesta para enviarla
            final_response += str(response).encode('utf-8')
            #print('Final response de get es: ', final_response)
            # Envia el header y la respuesta
            connection.send(final_response)
            # Cierra la conexion
            connection.close()

def main():
    server = Server('127.0.0.1', 8888)
    server.run()

if __name__ == "__main__":
    main()