import sys
import socket
import json

# Inicio del envio de la operacion
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
port = 8080
seq = 0
ack = 0
fin = True
while True: 
    bufferSize = 1024
    serverAddressPort = ("127.0.0.1", port)

    operation = input("Ingrese la operacion: ")
    dataJson = {"seq":seq,"type":"request","fin":fin,"request":"write","operation":"operation"}
    jsonString = json.dump(dataJson)
    # Se encripta
    jsonToSend = str.encode(jsonString)

    # Envia la operacion
    UDPClientSocket.sendto(jsonToSend, serverAddressPort)
    
    #Recibe la veirificacion de que recibio el producto
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    verification = msgFromServer[0].decode()
    serverAddressPort = msgFromServer[1].decode()

    verificationJson = json.loads(verification)

    if verificationJson["type"] == "ack":
        if verificationJson["ack"] == ack:
            if verificationJson["seq"] == seq:

                
                # Recibe la operacion
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                operation = msgFromServer[0].decode()
                serverAddressPort = msgFromServer[1].decode()

                operationJson = json.loads(operation)
                
                if verificationJson["seq"] == seq:
                    if verificationJson["type"] == "request":
                        if verificationJson["fin"] == True:
                            if verificationJson["request"] == "write":
                                print(verificationJson["result"])


                                dataJson = {"type":"ack","ack":ack,"seq":seq}
                                jsonString = json.dumb(dataJson)
                                # Se encripta
                                jsonToSend = str.encode()

                                # Envia la verificacion que recibio el resultado
                                UDPClientSocket.sendto(jsonToSend, serverAddressPort)
                            else:
                                print("Request erroneo")
                        else:
                            print("DEBE ESPERAR LO FRACCIONADO")
                    else:
                        print("Type erroneo")
                else:
                    print("Seq erroneo")

            else:
                print("Seq erroneo")
        else: 
            print("Ack erroneo")
    else:
        print("Ack erroneo")




def encryption() :
    print("HOLA MUNDO")

def log_in(argv):

    if sys.argv[1] == "-u":
        username = sys.argv[2]
        print(username)
    else:
        print ("-u incorrecto")
    
    if sys.argv[3] == "-p": 
        password = sys.argv[4]
        print(password)
    else:
        print ("-p incorrecto")
    

def casting_forever() :
    print("HOLA MUNDO")

def stop_listening():
    print("HOLA MUNDO")

def send_messasge():
    print("HOLA MUNDO")