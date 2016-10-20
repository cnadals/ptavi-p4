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
metodo = "REGISTER sip:" + sys.argv[3] + ' ' + "SIP/2.0\r\n\r\n"
# añado el nuevo valor de line (cambia a "una posicion superior")
line = sys.argv[4]
# añado campo expires
expires = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((server, port))
    #compruebo si es register, y doy su "nuevo valor"
    if metodo == 'REGISTER':
    	line = metodo + 'Expires: ' + expires + '\r\n'
    print("Enviando:", line)
    my_socket.send(b(line, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
