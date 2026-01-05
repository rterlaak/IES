import socket
import struct

host = "localhost"
port = 12000

def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError
        data += part
    return data

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

clientSocket.sendall(b"LIST")
files_json = clientSocket.recv(1024).decode()
files = json.loads(files_json)

for i, name in enumerate(files, 1):
    print(f"{i}. {name}")

filename = input("Which file would you like to download: ")
clientSocket.send(filename.encode())

size = struct.unpack("!Q", recvall(clientSocket, 8))[0]

if size == 0:
    print("File not found")
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

clientSocket.close()
print("Download complete")

def menu():
    while True:
        print("please choose from the following options:")
        print("1. View files")
        print("2. Download files")
        print("3. Upload files")
        print("4. Chat")
        print("5. Logout")
        choice = input("User input: ")
        if choice == "1":
            #code voor funtie

        elif choice == "2":
            # code voor funcite

        elif choice == "3":
            #code voor functie

        elif choice == "4":
            #code voor functie

        elif choice == "5":
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    menu()