import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def chacha20_encrypt(key, nonce, plaintext):
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext)

def chacha20_decrypt(key, nonce, ciphertext):
    # Es simétrico: usar la misma clave y nonce
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)

"""

key = os.urandom(32)        # 256-bit key
nonce = os.urandom(16)      # 128-bit nonce (cryptography usa 16 bytes, no 12)

mensaje = b"Este es un mensaje secreto usando ChaCha20."
print("Mensaje original:", mensaje)

# Cifrado
cifrado = chacha20_encrypt(key, nonce, mensaje)
print("Cifrado (hex):", cifrado.hex())

# Descifrado
descifrado = chacha20_decrypt(key, nonce, cifrado)
print("Descifrado:", descifrado.decode())

"""