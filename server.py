import json
import struct
import os
import socket
from email.header import Header

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

while True:
    connectedClient, clientAddress = serverSocket.accept()
    print(f"Connected to: {clientAddress[0]} : {clientAddress[1]}")

    try:
        # Receive the initial command or string
        header = connectedClient.recv(1024).decode().strip()

        # === UPLOAD LOGIC ===
        if header == "UPLOAD":
            connectedClient.send("READY".encode())  # Tell client we are ready

            # Receive Filename
            filename = connectedClient.recv(1024).decode().strip()
            connectedClient.send("ACK".encode())  # Acknowledge filename received

            # Receive File Size (8 bytes)
            data_size = connectedClient.recv(8)
            filesize = struct.unpack("!Q", data_size)[0]

            # path to save the file
            save_path = os.path.join(SERVER_DIR, filename)

            # Receive File Content loop
            with open(save_path, "wb") as f:
                remaining = filesize
                while remaining > 0:
                    # Receive 4096 bytes or whatever is left
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = connectedClient.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)

            print(f"File {filename} received and saved.")

        elif header == "LIST":
            files = [
                f for f in os.listdir(SERVER_DIR)
                if os.path.isfile(os.path.join(SERVER_DIR, f))
            ]
            connectedClient.send(json.dumps(files).encode())

            filename = connectedClient.recv(1024).decode().strip()
            filepath = os.path.join(SERVER_DIR, filename)

            if not os.path.exists(filepath):
                connectedClient.sendall(struct.pack("!Q", 0))
            else:
                filesize = os.path.getsize(filepath)
                connectedClient.sendall(struct.pack("!Q", filesize))

                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        connectedClient.sendall(chunk)

        # === EXISTING LOGIC (.txt check) ===
        elif header.endswith(".txt"):
            to_send = "The received file is: " + header + "\n The files in the server directory are: " + str(
                os.listdir(SERVER_DIR))
            connectedClient.send(to_send.encode())

        elif header == "LOGIN":
            connectedClient.send("READY".encode())  # Tell client we are ready
            while True:
                username = connectedClient.recv(1024).decode()

                try:
                    actual_password = passwords[username]
                except KeyError:
                    if username == "EXIT LOGIN":
                        break
                    else:
                        actual_password = "UNKNOWN USERNAME"
                connectedClient.send(actual_password.encode())


        else:
            connectedClient.send("INVALID COMMAND OR FILE FORMAT".encode())



    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        connectedClient.close()