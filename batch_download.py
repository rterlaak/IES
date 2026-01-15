import socket
import json
import os
import struct
import time

def recvall(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError("error in recvall")
        data += part
    return data

def download_batch(HOST, PORT, LOCAL_DIR, files_to_download = None):

    #start a timer
    start_time = time.time()
    try:
        #get list of files
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((HOST, PORT))
        clientSocket.sendall(b"LIST")
        files_json = clientSocket.recv(1024).decode()
        available_files = json.loads(files_json)
        clientSocket.close()
        print(f"Available files on server: {available_files}")

        #which files to download
        if files_to_download is None:
            files_to_download = available_files
        #download each file
        for filename in files_to_download:
            if filename not in available_files:
                print(f"File '{filename}' not found on server, skipping...")
                continue

            file_path = os.path.join(LOCAL_DIR, filename)
            if os.path.exists(file_path):
                print(f"Skipping {filename}, already exists locally")
                continue
            print(f"Downloading '{filename}'...")

            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((HOST, PORT))

            #request the files
            clientSocket.sendall(b"DOWNLOAD")
            clientSocket.recv(1024)  # Receive file list again
            clientSocket.sendall(filename.encode())

            #Receive file size
            size = struct.unpack("!Q", recvall(clientSocket, 8))[0]

            if size == 0:
                print(f"File '{filename}' not found on server")
                continue

            # save file to local directory
            file_path = os.path.join(LOCAL_DIR, filename)
            with open(file_path, "wb") as f:
                remaining = size
                while remaining > 0:
                    chunk_size = 1024 if remaining >= 1024 else remaining
                    chunk = clientSocket.recv(chunk_size)
                    if not chunk:
                        print(f"Error: Connection lost while downloading {filename}")
                        break
                    f.write(chunk)
                    remaining -= len(chunk)

                f.flush()
                os.fsync(f.fileno())
                print(f"✓ Downloaded {filename} ({size} bytes)")

            clientSocket.close()

    except Exception as e:
        print(f"Error during batch download: {e}")

    elapsed_time = time.time() - start_time
    print(f"Total download time: {elapsed_time:.3f} seconds")


