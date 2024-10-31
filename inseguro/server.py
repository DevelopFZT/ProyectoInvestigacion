import socket
import threading

# Lista de palabras clave y diccionario de contadores
KEYWORDS = ["clave1", "clave2", "clave3"]
keyword_counts = {keyword: 0 for keyword in KEYWORDS}

def handle_client(client_socket):
    global keyword_counts
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Cliente: {message}")
                for keyword in KEYWORDS:
                    if keyword in message:
                        keyword_counts[keyword] += 1
                        print(f"La palabra clave '{keyword}' ha sido escrita {keyword_counts[keyword]} veces.")
                response = input("Servidor: ")
                client_socket.send(response.encode('utf-8'))
            else:
                break
        except:
            break
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 7777))
    server.listen(5)
    print("Servidor escuchando en el puerto 7777")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión aceptada de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()