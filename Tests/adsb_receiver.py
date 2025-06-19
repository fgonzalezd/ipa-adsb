"""
Nombre              :   adsb_receiver.py

Descripcion         :   simula el procesamiento de mensajes de ADS-B 
                        provenientes de diferentes fuentes. Define una lista de 
                        fuentes confiables a partir del campo Type Code.
                        Este script es una prueba de concepto para un metodo 
                        propuesto para transmision segura de mensajes ADS-B
                
Autor               :   Fernando Gonzalez

Fecha               :   18-Junio-2025

Ultima modificacion :   18-Junio-2025
"""

import socket
import threading
import pyModeS as pms

HOST = '0.0.0.0'
PORT = 30002

trusted_senders = []

"""
Codigo seleccionado para nuevo mensaje de identificacion
Se selecciono 0 porque no tiene asignacion
Ref: https://mode-s.org/1090mhz/content/ads-b/1-basics.html
"""
ID_TYPE_CODE = 0

def handle_client(conn, addr):
    print(f"Conectado: {addr}")
    
    first_id_rx = False
    msg_buffer = []
    
    with conn:
        while True:
            data = conn.recv(1024)
            
            if not data:
                print(f"Cliente desconectado: {addr}")
                break
                
            adsb_raw_msg = data.decode()            
            type_code = pms.adsb.typecode(adsb_raw_msg)
            sender = pms.adsb.icao(adsb_raw_msg)
            
            print("----------------")
            print("raw       : "+adsb_raw_msg)
            print("type code : "+str(type_code))
            print("sender    : "+sender)
            
            
            if first_id_rx:
                if type_code == ID_TYPE_CODE:
                    
                    # decrypt hash from adsb_raw_msg
                    rx_hash = 123
                    # calculate hash from buffer
                    calc_hash = 123
                    
                    # limpiar el buffer
                    msg_buffer.clear()
                    
                    if rx_hash == calc_hash:
                        if sender not in trusted_senders:
                            trusted_senders.append(sender)
                    else:
                        if sender in trusted_senders:
                            trusted_senders.remove(sender)
                    print("trusted_senders: " + str(trusted_senders))
                    
                else:
                    msg_buffer.append(adsb_raw_msg)
                    print("msg_buffer: " + str(msg_buffer))
            else:
                if type_code == ID_TYPE_CODE:
                    first_id_rx = True
                    print("first_id_rx: " + str(first_id_rx))
            
            print("----------------")    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor escuchando en {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
