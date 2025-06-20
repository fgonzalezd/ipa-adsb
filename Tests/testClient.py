# tcp_client.py
import socket
import pyModeS as pms
from fastavro import reader
import time

HOST = '127.0.0.1'  # Dirección del servidor (localhost)
PORT = 30002        # Puerto del servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
    client_socket.connect((HOST, PORT))
    print("Conectado al servidor")

    messages = [
        "8d4008f999059a90c09719d7b430",
        "8d3c646b58b501677afdb8f50b23",
        "8d4b7fab00982b52197953000000", #first ID
        "8f406a9a5913d2d51fbe8ab14fdf",
        "8d4ca8af58bf015971cdbe000000",
        "8d400fe299414387c85415000000",
        "8d3c649158b9734255706a000000",
        "8d7502930109d48f100423000000", # second ID
        "8d4bcced90834188c76a392b2567",
        "8d3c64919914243ac00419000000",
        "8d3c49379011a4ca15b73f000000",
        "8d780a169941cf12480424dce54b"
    ]
    
    for msg in messages:
        client_socket.sendall(msg.encode())
        time.sleep(0.2) # 5 messages per second
