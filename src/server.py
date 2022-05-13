import socket
import json

def receiveOperation() :
    jsonToReceive = UDPServerSocket.recvfrom(bufferSize)
    operation = jsonToReceive[0]
    serverAddressPort = jsonToReceive[1]  

    oper = operation.decode()

    operationJson = json.loads(oper)

    if operationJson["seq"] == seq: 
        if operationJson["type"] == "request":
            if operationJson["fin"] == True:
                if operationJson["request"] == "write":
                    operation = ""
                    print("CONVERTIR LA OPERACION")
                    result = 0

                    sendVerification()

                    sendResult()

                    receiveVerification()
                else:
                    print("Request erroneo")
            else:
                print("TIENE QUE HACERSE FRACCIONADO")
        else:
            print("Type erroneo")
    else:
        print("Numero de secuencia erroneo")

def sendVerification() :
    dataJson = {"type":"ack","ack":ack,"seq":seq}
    jsonString = json.dump(dataJson)
    # Se encripta
    jsonToSend = str.encode(jsonString)

    UDPServerSocket.sendto(jsonToSend, serverAddressPort)

def sendResult() :
    dataJson = {"seq":seq,"type":"request","fin":fin,"request":"write","result":result,"operation":operation}
    jsonString = json.dump(dataJson)
    # Se encripta
    jsonToSend = str.encode(jsonString)

    UDPServerSocket.sendto(jsonToSend, serverAddressPort)

def receiveVerification() :
    jsonToReceive = UDPServerSocket.recvfrom(bufferSize)
    verification = jsonToReceive[0]
    serverAddressPort = jsonToReceive[1]

    veri = verification.decode()

    verificationJson = json.loads(veri)

    if verificationJson["type"] == "ack" :
        if verificationJson["ack"] == ack:
            if verification["seq"] == seq:
                receiveRequest()
            else:
                print("Seq erroneo")
        else:
            print("Ack erroneo")
    else :
        print("Type erroneo")

def receiveRequest() :
    jsonToReceive = UDPServerSocket.recvfrom(bufferSize)
    request = jsonToReceive[0]
    serverAddressPort = jsonToReceive[1]

    req = operation.decode()

    requestJson = json.loads(oper)

    if requestJson["type"] == "disconnect" :
        UDPServerSocket.close()
    else :
        print("RECIBE OPERACION")

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
    receiveOperation()

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