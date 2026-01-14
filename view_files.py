import os
import socket
import json
import struct


def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError
        data += part
    return data

def send_msg(sock, payload: bytes):
    sock.sendall(struct.pack("!Q", len(payload)))
    sock.sendall(payload)

def recv_msg(sock) -> bytes:
    n = struct.unpack("!Q", recvall(sock, 8))[0]
    return recvall(sock, n)


def view_files_client(HOST, PORT, LOCAL_DIR):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    print("1 - Show local files")
    print("2 - Show server files")
    sort = input("Choose option: ").strip()

    if sort == "1":
        if not os.path.isdir(LOCAL_DIR):
            print("Local folder not found")
            exit()

        files = [
            f for f in os.listdir(LOCAL_DIR)
            if os.path.isfile(os.path.join(LOCAL_DIR, f))
        ]

        print("Local files:")
        for f in files:
            print(f)

    # ===== SERVER FILES =====
    elif sort == "2":

        # ask server for file list
        send_msg(clientSocket, b"LIST")
        files = json.loads(recv_msg(clientSocket).decode)

        print("Server files:")
        for f in files:
            print(f)