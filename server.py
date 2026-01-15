import struct
import os
import socket
import json
from server_download import download_server
from server_upload import upload_server
from server_login import login_server

# Create a folder for server files if it doesn't exist

SERVER_DIR = "server_files"
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

passwords = {"admin": "admin", "ADMIN": "ADMIN", "username": "password"}

#----------------------------------------------------------------------------------------

HOST = "localhost"
PORT = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))

serverSocket.listen()
print("The server is listening...")

while True:
    connectedClient, clientAddress = serverSocket.accept()
    print(f"Connected to: {clientAddress[0]} : {clientAddress[1]}")

    try:
        # Receive the initial command or string
        header = connectedClient.recv(1024).decode()

        # === UPLOAD LOGIC ===
        if header == "UPLOAD":
            upload_server(connectedClient, SERVER_DIR)


        elif header == "DOWNLOAD":
            download_server(connectedClient, SERVER_DIR )


        elif header == "LOGIN":
            login_server(connectedClient, clientAddress, SERVER_DIR)

        elif header == "LIST":
            files = [
                f for f in os.listdir(SERVER_DIR)
                if os.path.isfile(os.path.join(SERVER_DIR, f))
            ]
            connectedClient.sendall(json.dumps(files).encode())
            connectedClient.close()

        else:
            connectedClient.send("INVALID COMMAND OR FILE FORMAT".encode())

        connectedClient.close()


    except Exception as e:
        print(f"Error handling client: {e}")