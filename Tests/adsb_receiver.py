"""
Nombre              :   adsb_receiver.py

Descripcion         :   simula el procesamiento de mensajes de ADS-B 
                        provenientes de diferentes fuentes. Define una lista de 
                        fuentes confiables a partir del campo Type Code.
                        Este script es una prueba de concepto para un metodo 
                        propuesto para transmision segura de mensajes ADS-B
                
Autor               :   Fernando Gonzalez

Fecha               :   18-Junio-2025

Ultima modificacion :   21-Junio-2025
"""

import socket
import threading
import pyModeS as pms
import chacha20 as cc20
import os
import zlib
import credentials
import time

HOST = '0.0.0.0'
PORT = 30002

trusted_senders = []
untrusted_senders = []

""" Llave y nonce para encriptacion con chacha20 """
key = credentials.key       # 256-bit key
nonce = credentials.nonce   # 128-bit nonce (cryptography usa 16 bytes, no 12)

"""
Codigo seleccionado para nuevo mensaje de identificacion
Se selecciono 0 porque no tiene asignacion
Ref: https://mode-s.org/1090mhz/content/ads-b/1-basics.html
"""
ID_TYPE_CODE = 0

""" Cantidad de mensajes usados para la validacion """
MAX_MSG = 10

"""
cifra los datos usando chacha20
data: lista que contiene los mensajes a cifrar
"""
def calculate_chacha20(data):
    aux = ""
    
    for m in data:
        aux += m
        
    return cc20.chacha20_encrypt(key, nonce, aux.encode())

"""
calcula el crc32 a partir de los mensajes cifrados
msg: mensaje obtenido de cifrar los datos almacenados en el buffer
"""
def calculate_crc32(msg):
    cksum = zlib.crc32(msg)
    return cksum
        

def handle_client(conn, addr):
    print(f"Conectado: {addr}")
    
    first_id_rx = False # bandera de inicio
    msg_buffer = [] # buffer temporal
    msg_counter = 0
    trusted = False
    
    with open('receiver_log.txt', 'w') as l:
        l.write("msg\tsender\ttrusted\n")
    
    with conn:
        while True:
            data = conn.recv(1024)
            
            if not data:
                print(f"Cliente desconectado: {addr}")
                break
                
            adsb_raw_msg = data.decode()            
            type_code = pms.adsb.typecode(adsb_raw_msg)
            sender = pms.adsb.icao(adsb_raw_msg)
            
            msg_counter += 1
            
            print("----------------")
            print("raw       : "+adsb_raw_msg)
            print("type code : "+str(type_code))
            print("sender    : "+sender)
            
            # Si ya se recibio el primer mensaje de identificacion, se inicia
            # el proceso de validacion
            if first_id_rx:
                
                # el mensaje actual es de identificacion
                if type_code == ID_TYPE_CODE:
                    
                    # cifrar los mensajes del buffer
                    calc_chacha20 = calculate_chacha20(msg_buffer)
                    
                    # calcular el crc32 a partir de los datos cifrados
                    calc_crc32 = calculate_crc32(calc_chacha20)
                    print("calc_crc32: " + str(calc_crc32))
                    
                    # limpiar el buffer
                    msg_buffer.clear()
                    
                    
                    # crc32 recibido en el mensaje de identificacion
                    rx_crc32 = int(pms.data(adsb_raw_msg)[6:], 16)
                    print("rx_crc32: " + str(rx_crc32))
                    
                    # el CRC calculado es igual al recibido
                    if rx_crc32 == calc_crc32:
                        print("trusted sender")
                        trusted = True
                        # agrega el transmisor a la lista de confiables
                        if sender not in trusted_senders:
                            trusted_senders.append(sender)
                        # elimina el transmisor de la lista de no confiables
                        if sender in untrusted_senders:
                            untrusted_senders.remove(sender)
                        
                    else:
                        print("untrusted sender")
                        trusted = False
                        # elimina el transmisor de la lista de confiables
                        if sender in trusted_senders:
                            trusted_senders.remove(sender)
                        # agrega el transmisor a la lista de no confiables
                        if sender not in untrusted_senders:
                            untrusted_senders.append(sender)
                            
                    print("trusted_senders: " + str(trusted_senders))
                    print("untrusted_senders: " + str(untrusted_senders))
                    
                # Si no es mensaje de identificacion, guarde el mensaje en el
                # buffer temporal
                elif len(msg_buffer) < MAX_MSG:
                    msg_buffer.append(adsb_raw_msg)
                    print("msg_buffer: " + str(msg_buffer))
                    
                # Si llegamos aqui no se ha recibido ID despues de 10 mensajes
                # El sender ya no es confiable
                elif len(msg_buffer) == MAX_MSG:
                    trusted = False
                    # elimina el transmisor de la lista de confiables
                    if sender in trusted_senders:
                        trusted_senders.remove(sender)
            
            # Aun no se ha recibido el primer mensaje de identificacion
            else:
                # Se verifica si el mensaje actual es de identificacion
                if type_code == ID_TYPE_CODE:
                    first_id_rx = True
                    print("first_id_rx: " + str(first_id_rx))
                    
            with open('receiver_log.txt', 'a') as l:
                l.write(str(msg_counter) + "\t" + sender + "\t" + str(trusted) + "\n")
            

            
            print("----------------")    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor escuchando en {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
