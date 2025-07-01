# simClient.py

import sys
import socket
import time
import credentials
import zlib
import chacha20 as cc20
import random

HOST = '127.0.0.1'  # Dirección del servidor (localhost)
PORT = 30002        # Puerto del servidor

#scr_file = 'raw_messages_4008f9.txt'
#scr_file = 'raw_messages.txt'
#id_enabled = True
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
    
    
def connect_client(scr_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Conectado al servidor")
        
        msg_buffer = []
        id_enabled = False
        msg_counter = random.randint(20, 100)
        
        with open('client_log.txt', 'w') as l:
            l.write("msg\tTS\n")

        with open(scr_file, 'r') as f:
            for line in f:
                msg = line.strip()

                client_socket.sendall(msg.encode())
                
                with open('client_log.txt', 'a') as l:
                    l.write(str(msg) + "\t" + str(int(time.time() * 1000)) + "\n")
                    
                time.sleep(0.2)
                
                if len(msg_buffer) < MAX_MSG:
                    msg_buffer.append(msg)
                
                if len(msg_buffer) == MAX_MSG:
                    
                    if id_enabled:
                        id_msg = create_id_msg(msg_buffer)
                        client_socket.sendall(id_msg.encode())
                        
                        with open('client_log.txt', 'a') as l:
                            l.write(str(id_msg) + "\t" + str(int(time.time() * 1000)) + "\n")
                            
                        time.sleep(0.2)
                    
                    msg_buffer.clear()
                
                msg_counter -= 1
                if msg_counter == 0:
                    msg_buffer.clear()
                    id_enabled = not id_enabled
                    msg_counter = random.randint(20, 100)

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Usage: simClient.py <file>")
    else:
        connect_client(sys.argv[1])