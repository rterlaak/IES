import struct
import os
import socket
import json

from server_download import download_server
from server_upload import upload_server
from server_login import login_server
from server_chat import chat_server

from threading import Thread

# Create a folder for server files if it doesn't exist

SERVER_DIR = "server_files"
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

#----------------------------------------------------------------------------------------

class ClientThread(Thread):
    def __init__(self, connectedClient, clientAddress, udpSocket, SERVER_DIR):
        Thread.__init__(self)
        self.connectedClient = connectedClient
        self.clientAddress = clientAddress
        self.udpSocket = udpSocket
        self.SERVER_DIR = SERVER_DIR

    def run(self):
        try:
            # Receive the initial command or string
            header = self.connectedClient.recv(1024).decode()
            print(f"HEADER RECEIVED: {repr(header)}")

            # === UPLOAD LOGIC ===
            if header == "UPLOAD":
                upload_server(self.connectedClient, SERVER_DIR)

            elif header == "DOWNLOAD":
                download_server(self.connectedClient, SERVER_DIR )

            elif header == "LOGIN":
                login_server(self.connectedClient, self.clientAddress, SERVER_DIR)

            elif header == "CHAT":
                chat_server(self.udpSocket, self.SERVER_DIR)

            else:
                self.connectedClient.send("INVALID COMMAND OR FILE FORMAT".encode())

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:
            if self.connectedClient is not None: #Should be handled in functions, but just in case
                self.connectedClient.close()
            return


HOST = "localhost"
PORT = 12000
passwords = {"admin": "admin", "ADMIN": "ADMIN", "username": "password"}

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind((HOST, PORT + 1))

threads = []

serverSocket.listen()
print("The server is listening...")

while True:
    connectedClient, clientAddress = serverSocket.accept()
    print(f"Connected to: {clientAddress[0]} : {clientAddress[1]}")

    newthread = ClientThread(connectedClient, clientAddress, udpSocket, SERVER_DIR)
    newthread.start()
    threads.append(newthread)

