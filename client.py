#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket

# Constantes. Dirección IP del servidor y contenido a enviar
# Pido por pantalla ip, puerto y mensaje
server = sys.argv[1]
port = int(sys.argv[2])
metodo = "REGISTER sip:" + sys.argv[3] + "SIP/2.0\r\n\r\n"
#direccionsip = sys.argv[4]
#if direccionsip != 'register':
#	sys.exit("User error")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((server, port))
    print("Enviando:", metodo)
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
