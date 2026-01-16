import os
#passwords = {"admin": "admin", "ADMIN": "ADMIN", "username": "password"}

CREDENTIALS_FILE = "server_files\credentials.txt"

def load_credentials(path: str) -> dict[str, str]:
    account= {}
    if not os.path.exists(path):
        return account
    #reads accounts from credentials.txt
    with open(path) as file:
        for raw in file:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            user, pw = line.split(":")
            account[user.strip()] = pw.strip()
    return account


def login_server(connectedClient, clientAddress,):
    credentials = load_credentials(CREDENTIALS_FILE)
    connectedClient.send(b"READY")  # Tell client we are ready
    while True:
        username = connectedClient.recv(1024).decode().strip()
        if username == "EXIT LOGIN":
            print(f"Connection to: {clientAddress[0]} : {clientAddress[1]} has been closed")
            connectedClient.close()
            break
        connectedClient.send(b"PASSWORD")
        entered_password = connectedClient.recv(1024).decode().strip()
        #checks if username and/or password is correct
        if username not in credentials:
            connectedClient.send(b"UNKNOWN USERNAME")
        elif credentials[username] == entered_password:
            connectedClient.send(b"OK")
        else:
            connectedClient.send(b"WRONG PASSWORD")