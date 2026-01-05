import socket

host = "localhost"
port = 12000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

sendMsg = input("Please provide the filename of the file you wish to send: ")

clientSocket.send(sendMsg.encode())
receivedMsg = clientSocket.recv(1024).decode()
print("Server response:")
print(receivedMsg)
clientSocket.close()

def Menu():
    while True:
        print("Please make your choice:")
        print("1  -  View files")
        print("2  -  Download files")
        print("3  -  Upload files")
        print("4  -  Chat")
        print("5  -  logout")

        choice = input("User choice: ")
        if choice == "1":
            #code voor view
        elif choice == "2":
            #code voor dowload

        elif choice == "3":
            #vode voor Upload

        elif choice == "4":
            #code voor Chat

        elif choice == "5":
            print("User logout")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    Menu()