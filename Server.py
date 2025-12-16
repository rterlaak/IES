import socket

host = "localhost"
port = 12000

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((host, port))
print(f"socket bound to port: {port}")

serverSocket.listen(1)
print("Socket is listening...")

while True:
     connectedClient, clientAddress = serverSocket.accept()
     print(f"Connected to: {clientAddress[0]} : {clientAddress[1]}")
     decodedString = (connectedClient.recv(1024).decode())

     if decodedString[-4:] == ".txt":
          to_send = "The received file is: "+ decodedString + "\n The files in the server directory are:"
     else:
          to_send = "INVALID FILE FORMAT"

     connectedClient.send(to_send.encode())
     connectedClient.close()