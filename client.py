import os
from client_login import login_client
from batch_download import download_batch
from client_chat import chat_client
from client_download import download_files_client
from view_files import view_files_client
from client_upload import upload_client


def menu(HOST, PORT, LOCAL_DIR, username):
    #menu shown to user
    while True:
        print("Please make your choice:")
        print("1  -  View files")
        print("2  -  Download files")
        print("3  -  Upload files")
        print("4  -  Chat")
        print("5  -  Log out")
        print("6  -  Batch download")
        choice = input("User choice: ")

        if choice == "1": #opens view files
            view_files_client(HOST, PORT, LOCAL_DIR)

        elif choice == "2": #opens download
            download_files_client(HOST, PORT, LOCAL_DIR)

        elif choice == "3": #opends upload
            upload_client(HOST, PORT, LOCAL_DIR)

        elif choice == "4": #opens chat
            chat_client(HOST, PORT, username)

        elif choice == "6": #starts batch download
            download_batch(HOST, PORT, LOCAL_DIR)

        elif choice == "5": #closes client
            print("User Log out")
            break


        else:
            print("Invalid choice")

HOST = "localhost"
PORT = 12000
LOCAL_DIR = "local_files" #file for local files
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

authentication, username = login_client(HOST, PORT)

if authentication: #if login is correct, starts menu
    menu(HOST, PORT, LOCAL_DIR, username)