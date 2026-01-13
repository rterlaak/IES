


passwords = {"admin": "admin", "ADMIN": "ADMIN", "username": "password"}

def login_server(connectedClient, clientAddress, SERVER_DIR):
    connectedClient.send("READY".encode())  # Tell client we are ready
    while True:
        username = connectedClient.recv(1024).decode()

        try:
            actual_password = passwords[username]
        except KeyError:
            if username == "EXIT LOGIN":
                print(f"Connection to: {clientAddress[0]} : {clientAddress[1]} has been closed")
                connectedClient.close()
                break
            else:
                actual_password = "UNKNOWN USERNAME"
        connectedClient.send(actual_password.encode())