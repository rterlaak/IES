import socket
def login_client(HOST, PORT):
    succes = False
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    attempts_left = 3

    clientSocket.send("LOGIN".encode())
    clientSocket.recv(1024).decode()  # Ready

    while attempts_left > 0:
        username = input("Please enter your username: ")
        entered_password = input("Please enter your password: ")

        clientSocket.send(username.encode())
        actual_password = clientSocket.recv(1024).decode()
        if actual_password == "UNKNOWN USERNAME":
            print("This username is unknown. Please try again.")
            #Password was not incorrect, so we don't take an attempt

        elif actual_password == entered_password:
            succes = True
            break

        else:
            attempts_left -= 1
            print("Wrong password. Please try again. \n You have " + str(attempts_left) + " attempts left.")

    clientSocket.send("EXIT LOGIN".encode())
    clientSocket.close()
    return succes, username