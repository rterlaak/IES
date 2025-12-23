import socket
import struct

host = "127.0.0.1"
port = 12000

def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError("Connection closed early")
        data += part
    return data

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.connect((host, port))

filename = input("Enter the filename: ")
clientSocket.send(filename.encode())

size = struct.unpack("!Q", recvall(clientSocket, 8))[0]

if size == 0:
    print("File not found on server")
    clientSocket.close()
    exit()

with open("downloaded_" + filename, "wb") as f:
    remaining = size

