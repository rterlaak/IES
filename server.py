import struct
import os

# Create a folder for server files if it doesn't exist

SERVER_DIR = "server_files"
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

while True:
    connectedClient, clientAddress = serverSocket.accept()
    print(f"Connected to: {clientAddress[0]} : {clientAddress[1]}")

    try:
        # Receive the initial command or string
        header = connectedClient.recv(1024).decode()

        # === UPLOAD LOGIC ===
        if header == "UPLOAD":
            connectedClient.send("READY".encode())  # Tell client we are ready

            # Receive Filename
            filename = connectedClient.recv(1024).decode()
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
                    if not chunk: break
                    f.write(chunk)
                    remaining -= len(chunk)

            print(f"File {filename} received and saved.")

        # === EXISTING LOGIC (.txt check) ===
        elif header.endswith(".txt"):
            to_send = "The received file is: " + header + "\n The files in the server directory are: " + str(
                os.listdir(SERVER_DIR))
            connectedClient.send(to_send.encode())

        else:
            connectedClient.send("INVALID COMMAND OR FILE FORMAT".encode())

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        connectedClient.close()