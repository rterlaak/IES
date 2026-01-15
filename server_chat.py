import json
import socket
import os

def chat_server(udpSocket, SERVER_DIR):
    print("UDP socket ready to receive...")

    filepath = os.path.join(SERVER_DIR, "chatlog.txt")
    clientsList = []

    while True:
        encoded_line, clientAddress = udpSocket.recvfrom(1024)
        received_line = encoded_line.decode()

        if clientAddress not in clientsList: #Add new chat users to the list
            clientsList.append(clientAddress)

        if received_line == "GETHISTORY":
            #This means it is the first message of this client, so the history must be printed.
            with open(filepath, "r") as chatlog:
                udpSocket.sendto(chatlog.read().encode(), clientAddress)

        elif received_line[-3:] == "!q\n": #The client wishes to close the chat
            udpSocket.sendto("!q".encode(), clientAddress)
            clientsList.remove(clientAddress)
            if len(clientsList) == 0:  # No active users left
                break

        else:
            with open(filepath, "a") as chatlog:
                chatlog.write(received_line) #Add to the chatlog

            for client in clientsList: #Send message to the other users
                if client != clientAddress:
                    print(received_line.encode())
                    udpSocket.sendto(received_line.encode(), client)

    return
