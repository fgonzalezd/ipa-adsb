# simClient.py

import socket
import time
import credentials
import zlib
import chacha20 as cc20

HOST = '127.0.0.1'  # Dirección del servidor (localhost)
PORT = 30002        # Puerto del servidor

#scr_file = 'raw_messages_4008f9.txt'
scr_file = 'raw_messages.txt'
id_enabled = True
MAX_MSG = 10

def create_id_msg(msg):
    aux = ""
    retMsg = msg[0][0:8]
    
    for m in msg:
        aux += m
        
    enc = cc20.chacha20_encrypt(credentials.key, credentials.nonce, aux.encode())
    cksum = zlib.crc32(enc)
    
    retMsg = retMsg + "000000" + hex(cksum)[2:] + "000000"
    
    return retMsg
    
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Conectado al servidor")
    
    msg_counter = 0
    msg_buffer = []

    with open(scr_file, 'r') as f:
        for line in f:
            msg = line.strip()

            client_socket.sendall(msg.encode())
            time.sleep(0.2)
            
            if id_enabled:
                
                if msg_counter < MAX_MSG:
                    msg_buffer.append(msg)
                    msg_counter += 1
                
                if msg_counter == MAX_MSG:
                    id_msg = create_id_msg(msg_buffer)
                    client_socket.sendall(id_msg.encode())
                    time.sleep(0.2)
                    print("buffer: \n" + str(msg_buffer))
                    print("id: "+id_msg)
                    msg_counter = 0
                    msg_buffer.clear()
