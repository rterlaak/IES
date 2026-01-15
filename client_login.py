import socket
def login_client(HOST, PORT):
    succes = False
    username = None
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    attempts_left = 3

    clientSocket.sendall(b"LOGIN")
    clientSocket.recv(1024).decode()  # Ready

    while attempts_left > 0:
        username = input("Please enter your username: ").strip()
        entered_password = input("Please enter your password: ").strip()

        clientSocket.sendall(username.encode())

        actual_password = clientSocket.recv(1024).decode().strip()
        if actual_password == "PASSWORD":
            clientSocket.sendall(entered_password.encode())
            result = clientSocket.recv(1024).decode().strip()

            if result == "UNKWNOWN USERNAME":
                print("wrong username, please try again.")
                # Password was not incorrect, so we don't take an attempt
            elif result == "OK":
                succes = True
                break
            else:
                attempts_left -= 1
                print("Wrong password. Please try again. \n You have " + str(attempts_left) + " attempts left.")
        else:
            attempts_left -= 1
            print("Unexpected server response. Please try again.")

    clientSocket.send(B"EXIT LOGIN")
    clientSocket.close()
    return succes, username