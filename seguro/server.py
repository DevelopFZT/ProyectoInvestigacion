import socket
import threading
from cryptography.fernet import Fernet

KEYWORDS = ["clave1", "clave2", "clave3"]
keyword_counts = {keyword: 0 for keyword in KEYWORDS}

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def handle_client(client_socket):
    global keyword_counts
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if encrypted_message:
                message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
                print(f"Cliente (encriptado): {encrypted_message}")
                print(f"Cliente (desencriptado): {message}")
                for keyword in KEYWORDS:
                    if keyword in message:
                        keyword_counts[keyword] += 1
                        print(f"La palabra clave '{keyword}' ha sido escrita {keyword_counts[keyword]} veces.")
                response = input("Servidor: ")
                print(f"Servidor (desencriptado): {response}")
                encrypted_response = cipher_suite.encrypt(response.encode('utf-8'))
                print(f"Servidor (encriptado): {encrypted_response}")
                client_socket.send(encrypted_response)
            else:
                break
        except:
            break
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Servidor escuchando en el puerto 5555")
    print(f"Clave de encriptación: {key.decode()}")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión aceptada de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()