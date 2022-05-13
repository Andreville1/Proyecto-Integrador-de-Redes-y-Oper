import socket
import json

# Inicio del recibimiento del producto
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 8080
bufferSize = 1024

ack = 0
seq = 0
fin = True
UDPServerSocket.bind((host, port))

while True:
    # Recibe la operacion
    jsonToReceive = UDPServerSocket.recvfrom(bufferSize)
    operation = jsonToReceive[0]
    serverAddressPort = jsonToReceive[1]

    oper = operation.decode()

    operationJson = json.loads(oper)
    
    if operationJson["seq"] == 0: 
        if operationJson["type"] == "request":
            if operationJson["fin"] == True:
                if operationJson["request"] == "write":
                    operation = ""
                    print("CONVERTIR LA OPERACION")
                    result = 0

                    dataJson = {"type":"ack","ack":ack,"seq":seq}
                    jsonString = json.dump(dataJson)
                    # Se encripta
                    jsonToSend = str.encode(jsonString)

                    # Envia verificacion de que recibio el producto
                    UDPServerSocket.sendto(jsonToSend, serverAddressPort)


                    dataJson = {"seq":seq,"type":"request","fin":fin,"request":"write","result":result,"operation":operation}
                    jsonString = json.dump(dataJson)
                    # Se encripta
                    jsonToSend = str.encode(jsonString)

                    # Envia el resultado
                    UDPServerSocket.sendto(jsonToSend, serverAddressPort)


                    # Recibe la verificacion de que le llego el resultado
                    jsonToReceive = UDPServerSocket.recvfrom(bufferSize)
                    verification = jsonToReceive[0]
                    serverAddressPort = jsonToReceive[1]

                    veri = verification.decode()

                    operationJson = json.loads(veri)


                else:
                    print("Request erroneo")
            else:
                print("TIENE QUE HACERSE FRACCIONADO")
        else:
            print("Type erroneo")
    else:
        print("Numero de secuencia erroneo")


def authenticator() :
    print("HOLA MUNDO")

def listen_forever() :
    print("HOLA MUNDO")

def stop_listening() :
    print("HOLA MUNDO")

def bind_connections() :
    print("HOLA MUNDO")

def receive_message():
    print("HOLA MUNDO")