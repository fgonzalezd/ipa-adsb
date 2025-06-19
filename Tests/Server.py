# tcp_server_multiclient.py
import socket
import threading

HOST = '0.0.0.0'
PORT = 30002

def handle_client(conn, addr):
    print(f"Conectado: {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"Cliente desconectado: {addr}")
                    break
                print(f"[{addr}] {data.decode()}")
                conn.sendall(b"Mensaje recibido\n")
            except:
                break
        conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor escuchando en {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
