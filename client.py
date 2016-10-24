#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket

# Compruebo la longitud de los argumentos
# Creo excepcion: si no esta bien escrito, cómo se hace.
# Para ello, elimino los sys anteriores.
if not len(sys.argv) == 6:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")
_, server, port, metodo, line, expires = sys.argv
port = int(port)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((server, port))
    if metodo == 'register':
        line = 'REGISTER sip:' + line + ' ' + 'SIP/2.0\r\n\r\n' + 'Expires: ' + expires + '\r\n'
    print("Enviando:", line)
    my_socket.send(bytes(line, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))
print("Socket terminado.")
