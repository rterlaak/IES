import os
import client_login
from client_download import download_files_client
from view_files import view_files_client
from client_upload import upload_client


def menu(HOST, PORT, LOCAL_DIR):
    while True:
        print("Please make your choice:")
        print("1  -  View files")
        print("2  -  Download files")
        print("3  -  Upload files")
        print("4  -  Chat")
        print("5  -  logout")
        choice = input("User choice: ")

        if choice == "1":
            view_files_client(HOST, PORT, LOCAL_DIR)

        elif choice == "2":
            download_files_client(HOST, PORT, LOCAL_DIR)

        elif choice == "3":
            upload_client(HOST, PORT, LOCAL_DIR)

        elif choice == "4":
            print("chat")
            #code voor Chat

        elif choice == "5":
            print("User logout")
            break


        else:
            print("Invalid choice")

HOST = "localhost"
PORT = 12000
LOCAL_DIR = "local_files"
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

authentication = login.login_client(HOST, PORT)

if authentication:
    menu(HOST, PORT, LOCAL_DIR)