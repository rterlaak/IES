import os
import json
import struct
import socket

def download_server(connectedClient, SERVER_DIR):
    files = [#list all files in server
        f for f in os.listdir(SERVER_DIR)
        if os.path.isfile(os.path.join(SERVER_DIR, f))
    ]
    connectedClient.send(json.dumps(files).encode())
    #filename that client wants to download
    filename = connectedClient.recv(1024).decode().strip()
    filepath = os.path.join(SERVER_DIR, filename)
    #checks if file exist
    if not os.path.exists(filepath):
        connectedClient.send(struct.pack("!Q", 0))
    else:
        filesize = os.path.getsize(filepath)
        connectedClient.sendall(struct.pack("!Q", filesize))
        #sends file to the client
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    f.close()
                    break
                connectedClient.sendall(chunk)


    connectedClient.close()
    return
