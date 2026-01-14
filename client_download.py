import socket
import json
import os
import struct


def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError("error in recvall")
        data += part
    return data

def download_files_client(HOST, PORT, LOCAL_DIR):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))

    clientSocket.sendall(b"DOWNLOAD")
    files_json = clientSocket.recv(1024).decode()
    files = json.loads(files_json)
    print("Available", files)
    filename = input("Which file do you want to download: ").strip()
    clientSocket.sendall(filename.encode())
    #json_encoded_size = clientSocket.recv(1024).decode()
    size = struct.unpack("!Q", recvall(clientSocket, 8))[0]

    if size == 0:
        print("File not found on server")
        clientSocket.close()
        return
    file_path = os.path.join(LOCAL_DIR, filename)

    with open(file_path, "wb") as f:
        remaining = size
        while remaining > 0:
            chunk = clientSocket.recv(1024 if remaining >= 1024 else remaining)
            f.write(chunk)
            if len(chunk) < 1024:
                print('BREAK')
                f.close()
                break
            remaining -= len(chunk)

        print("Download complete")

    clientSocket.close()


