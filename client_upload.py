import os
import socket
import struct

def upload_client(HOST, PORT, LOCAL_DIR):
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

