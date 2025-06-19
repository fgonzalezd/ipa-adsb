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
untrusted_senders = []

"""
Codigo seleccionado para nuevo mensaje de identificacion
Se selecciono 0 porque no tiene asignacion
Ref: https://mode-s.org/1090mhz/content/ads-b/1-basics.html
"""
ID_TYPE_CODE = 0

"""
retura el hash descifrado
msg_hash: un mensaje de 56-bit encriptado
"""
def decrypt_hash(msg_hash):
    #TODO: por ahora solo retorne el mismo hash
    #TODO: pendiente implementar descifrado usando un certificado
    return msg_hash

"""
calcula el hash a partir de los mensajes en el bufer
buff_msg: un bufer con mensajes de 56 bits
"""
def calculate_hash(buff_msg):
    #TODO: por ahora solo se hace un XOR a todos los mensajes
    #TODO: pendiente implementar el algoritmo de hash
    aux = 0xFFFFFFFFFF # valor semilla, 56 bits en 1
    for msg in buff_msg:
        aux ^= msg
    return aux
        

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
                    
                    # descrifrar el hash desde adsb_raw_msg
                    rx_hash = 123
                    # calcular el hash a partir de los datos en el bufer
                    calc_hash = calculate_hash(msg_buffer)
                    print("calc_hash: " + str(calc_hash))
                    
                    # limpiar el buffer
                    msg_buffer.clear()
                    
                    if rx_hash == calc_hash:
                        print("trusted sender")
                        if sender not in trusted_senders:
                            trusted_senders.append(sender)
                        if sender in untrusted_senders:
                            untrusted_senders.remove(sender)
                    else:
                        print("untrusted sender")
                        if sender in trusted_senders:
                            trusted_senders.remove(sender)
                        if sender not in untrusted_senders:
                            untrusted_senders.append(sender)
                    print("trusted_senders: " + str(trusted_senders))
                    print("untrusted_senders: " + str(untrusted_senders))
                    
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
