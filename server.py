#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    # creo mi diccionario vacio
    misdatos = {}

    def handle(self):
        #imprimo IP y PUERTO por pantalla
        print('IP del cliente: ' + self.client_address[0])
        print('PUERTO del cliente: ' + str(self.client_address[1]))
        datos = self.rfile.read().decode('utf-8').split(' ')
        #compruebo si es register. si es, mando OK
        if datos[0] == 'REGISTER':
            self.misdatos[datos[1]] = self.client_address
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            if int(datos[-1]) == 0:  # Compruebo si expires = 0.
                del self.misdatos[datos[1]]  # Si es = 0 --> fuera.
        print(self.misdatos)

if __name__ == "__main__":

    # pido el puerto por parametro
    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
