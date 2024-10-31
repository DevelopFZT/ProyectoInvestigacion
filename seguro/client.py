import socket
import threading
from cryptography.fernet import Fernet

key = input("Ingrese la clave de encriptación: ").encode()
cipher_suite = Fernet(key)

def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if encrypted_message:
                message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
                print(f"Servidor: {message}")
            else:
                break
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input("Cliente: ")
        encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
        client.send(encrypted_message)

if __name__ == "__main__":
    main()