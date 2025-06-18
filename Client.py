# tcp_client.py
import socket
import pyModeS as pms
from fastavro import reader
import time

HOST = '127.0.0.1'  # Dirección del servidor (localhost)
PORT = 30002        # Puerto del servidor

avro_scr_file = "raw20150421_sample.avro"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Conectado al servidor")

    with open(avro_scr_file, 'rb') as f:
        avro_reader = reader(f)
        for record in avro_reader:
            message = record["rawMessage"]
            if pms.icao(message) == "4008f9": # send only one specific aircraft
                client_socket.sendall(message.encode())
                time.sleep(0.2) # 5 messages per second
                #data = client_socket.recv(1024)
                #print("Respuesta:", data.decode())
