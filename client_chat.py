import socket
import json
import time
import threading

def receive_messages(clientUDPSocket):
    while True:
        encoded_line, serverAddress = clientUDPSocket.recvfrom(1024)
        if encoded_line.decode() == "!q":
            clientUDPSocket.close()
            break
        print("\n" + encoded_line.decode())
    return


def chat_client(HOST, PORT, username):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    clientSocket.sendall(b"CHAT")
    time.sleep(0.3) # Allows the server to open udpsocket

    clientUDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #============ GETTING CHAT HISTORY =============
    clientUDPSocket.sendto("GETHISTORY".encode(), (HOST, PORT+1))

    chat_history, serverAddress = clientUDPSocket.recvfrom(1024)
    chat_history = chat_history.decode()
    print("Retrieving messages for you...")
    print(chat_history)

    threading.Thread(target=receive_messages, args = [clientUDPSocket], daemon = True).start()
    #Daemon ensures that the thread stops when the socket is closed

    while True:
        message = input("["+username+"]: ")

        line_to_send = "["+username+"]: " + message.strip() + "\n"
        clientUDPSocket.sendto(line_to_send.encode(), serverAddress)
        if message == "!q":
            print("THE CHAT HAS BEEN CLOSED")
            break

    return



