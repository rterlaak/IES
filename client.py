import socket

host = "localhost"
port = 12000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

sendMsg = input("Please provide the filename of the file you wish to send: ")

clientSocket.send(sendMsg.encode())
receivedMsg = clientSocket.recv(1024).decode()
print("Server response:")
print(receivedMsg)
clientSocket.close()