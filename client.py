import socket
import os
import json
import struct


HOST = "localhost"
PORT = 12000
LOCAL_DIR = "local_files"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

sendMsg = input("Please provide the filename of the file you wish to send: ")

clientSocket.send(sendMsg.encode())
receivedMsg = clientSocket.recv(1024).decode()
print("Server response:")
print(receivedMsg)
clientSocket.close()

def Menu():
    while True:
        print("Please make your choice:")
        print("1  -  View files")
        print("2  -  Download files")
        print("3  -  Upload files")
        print("4  -  Chat")
        print("5  -  logout")

        choice = input("User choice: ")
        if choice == "1":
            #code voor view
        elif choice == "2":
            #code voor dowload

        elif choice == "3":
            #vode voor Upload

        elif choice == "4":
            #code voor Chat

        elif choice == "5":
            print("User logout")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    Menu()
def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError
        data += part
    return data

print("1 - Show local files")
print("2 - Show server files")
choice = input("Choose option: ").strip()

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

else:
    print("Invalid choice")
