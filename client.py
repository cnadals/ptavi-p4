#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket

# Constantes. Dirección IP del servidor y contenido a enviar
# Pido por pantalla ip, puerto y mensaje
#server = sys.argv[1]
#port = int(sys.argv[2])
#metodo = sys.argv[3]
# añado el nuevo valor de line (cambia a "una posicion superior")
#line = sys.argv[4]
# añado campo expires
#expires = sys.argv[5]

# Creo excepcion: si no esta bien escrito, como se hace.
# Para ello, elimino los sys anteriores.
if not len(sys.argv) == 6:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")
_, server, port, metodo, line, expires = sys.argv
port = int(port)

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((server, port))
    #compruebo si es register, y doy su "nuevo valor"
    if metodo == 'register':
    	line = 'REGISTER sip:' + line + ' ' + 'SIP/2.0 200 OK\r\n\r\n' + 'Expires: ' + expires + '\r\n'
    print("Enviando:", line)
    my_socket.send(bytes(line, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
