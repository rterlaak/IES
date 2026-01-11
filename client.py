import socket
import os
import json
import struct

LOCAL_DIR = "sample_files" #

def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError
        data += part
    return data

def login(HOST, PORT):
    succes = False
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    attempts_left = 3

    clientSocket.send("LOGIN".encode())
    clientSocket.recv(1024).decode()  # Ready

    while attempts_left > 0:
        username = input("Please enter your username: ")
        entered_password = input("Please enter your password: ")

        clientSocket.send(username.encode())
        actual_password = clientSocket.recv(1024).decode()
        if actual_password == "UNKNOWN USERNAME":
            print("This username is unknown. Please try again.")
            #Password was not incorrect, so we don't take an attempt

        elif actual_password == entered_password:
            succes = True
            break

        else:
            attempts_left -= 1
            print("Wrong password. Please try again. \n You have " + str(attempts_left) + " attempts left.")

    clientSocket.send("EXIT LOGIN".encode())
    clientSocket.close()
    return succes

def menu(HOST, PORT, LOCAL_DIR = LOCAL_DIR):
    while True:
        print("Please make your choice:")
        print("1  -  View files")
        print("2  -  Download files")
        print("3  -  Upload files")
        print("4  -  Chat")
        print("5  -  logout")
        choice = input("User choice: ")


# ===== LOCAL FILES =====
        if choice == "1":
            if not os.path.isdir(LOCAL_DIR):
                print("Local folder not found")
            else:
                files = [
                    f for f in os.listdir(LOCAL_DIR)
                    if os.path.isfile(os.path.join(LOCAL_DIR, f))
                    ]
            print("Local files:")
            for f in files:
                print(f)

# ===== SERVER FILES =====
        elif choice == "2":
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((HOST, PORT))

            # ask server for file list
            clientSocket.sendall(b"LIST")
            files_json = clientSocket.recv(8192).decode()
            files = json.loads(files_json)

            print("Server files:")
            for f in files:
                print(f)

            filename = input("Which file do you want to download: ").strip()
            clientSocket.sendall(filename.encode())

            size = struct.unpack("!Q", recvall(clientSocket, 8))[0]

            if size == 0:
                print("File not found on server")
                clientSocket.close()
                exit()

            with open("downloaded_" + filename, "wb") as f:
                remaining = size
                while remaining > 0:
                    chunk = clientSocket.recv(4096 if remaining >= 4096 else remaining)
                    if not chunk:
                        raise ConnectionError
                    f.write(chunk)
                    remaining -= len(chunk)

            print("Download complete")
            clientSocket.close()

        elif choice == "3":
            #code voor Upload
            filename = input("Enter the filename to upload: ")
            filepath = os.path.join(LOCAL_DIR, filename)

            if os.path.exists(filepath):
                try:
                    # Connect to server
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clientSocket.connect((HOST, PORT))

                    # Send UPLOAD command
                    clientSocket.send("UPLOAD".encode())

                    # Server acknowledgement
                    response = clientSocket.recv(1024).decode()
                    if response == "READY":
                        # Send Filename
                        clientSocket.send(filename.encode())

                        # filename is received
                        clientSocket.recv(1024)

                        # Send File Size
                        filesize = os.path.getsize(filepath)
                        clientSocket.send(struct.pack("!Q", filesize))

                        # Send File Contents
                        with open(filepath, "rb") as f:
                            while True:
                                bytes_read = f.read(4096)
                                if not bytes_read:
                                    break
                                clientSocket.sendall(bytes_read)

                        print(f"Successfully uploaded {filename}")
                    else:
                        print("Server rejected upload request.")

                    clientSocket.close()

                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print(f"File {filename} not found in {LOCAL_DIR}")

        elif choice == "4":
            pass #code voor Chat

        elif choice == "5":
            print("User logout")
            break

        else:
            print("Invalid choice")

HOST = "localhost"
PORT = 12000
LOCAL_DIR = "sample_files"

authentication = login(HOST, PORT)

if authentication:
    menu(HOST, PORT, LOCAL_DIR)
