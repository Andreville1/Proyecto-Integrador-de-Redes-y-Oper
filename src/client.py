import sys
import socket
import json

def sendOperation() :
    operation = input("Ingrese la operacion: ")

    dataJson = {"seq":seq,"type":"request","fin":fin,"request":"write","operation":"operation"}
    jsonString = json.dump(dataJson)
    # Se encripta
    jsonToSend = str.encode(jsonString)

    # Envia la operacion
    UDPClientSocket.sendto(jsonToSend, serverAddressPort)

def receiveVerification() :
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    verification = msgFromServer[0].decode()
    serverAddressPort = msgFromServer[1].decode()

    verificationJson = json.loads(verification)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    verification = msgFromServer[0].decode()
    serverAddressPort = msgFromServer[1].decode()

    verificationJson = json.loads(verification)

    if verificationJson["type"] == "ack":
        if verificationJson["ack"] == ack:
            if verificationJson["seq"] == seq:

                receiveOperation()

            else:
                print("Seq erroneo")
        else: 
            print("Ack erroneo")
    else:
        print("Ack erroneo")

def receiveOperation() :
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    operation = msgFromServer[0].decode()
    serverAddressPort = msgFromServer[1].decode()

    operationJson = json.loads(operation)

    if operationJson["seq"] == seq:
        if operationJson["type"] == "request":
            if operationJson["fin"] == True:
                if operationJson["request"] == "write":
                    print(operationJson["result"])

                                
                    sendVerification()
                else:
                    print("Request erroneo")
            else:
                print("DEBE ESPERAR LO FRACCIONADO")
        else:
            print("Type erroneo")
    else:
        print("Seq erroneo")

def sendVerification() :
    dataJson = {"type":"ack","ack":ack,"seq":seq}
    jsonString = json.dump(dataJson)
    # Se encripta
    jsonToSend = str.encode()

    # Envia la verificacion que recibio el resultado
    UDPClientSocket.sendto(jsonToSend, serverAddressPort)

    sendRequest()

def sendRequest() :
    opcion = input("Ingrese una opcion: ")

    if opcion[0] == "-" and opcion[1] == "q" :
        dataJson = {"seq":seq,"type":"disconnect"}
        jsonString = json.dump(dataJson)
        # Se encripta
        jsonToSend = str.encode(jsonString)

        # Envia la solicitud de desconexion
        UDPClientSocket.sendto(jsonToSend, serverAddressPort)
        UDPClientSocket.close()
    else :
        print("HACE OTRA OPERACION")

# Inicio del envio de la operacion
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
port = 8080
bufferSize = 1024
seq = 0
ack = 0
fin = True
serverAddressPort = ("127.0.0.1", port)

while True: 
    sendOperation()
    receiveVerification()


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