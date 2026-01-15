import os
import struct

def upload_server(connectedClient, SERVER_DIR):
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
            if not chunk:
                break
            f.write(chunk)
            remaining -= len(chunk)

        f.flush()
        os.fsync(f.fileno())
        print(f"File {filename} received and saved.")
    connectedClient.close()
    return