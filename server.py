#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    diccionario = {}

    def json2registered(self):
        """
        Comprobacion existencia fichero
        """
        try:
            with open('registered.json', 'r') as fichero:
                self.diccionario = json.load(fichero)
        except:
            pass

    def register2json(self):
        """
        Creacion de fichero
        """
        with open('registered.json', 'w') as fichero:
            json.dump(self.diccionario, fichero)

    def handle(self):
        """
        Manejador
        """
        if len(self.diccionario) == 0:
            self.json2registered()
        print('IP del cliente: ' + self.client_address[0])
        print('PUERTO del cliente: ' + str(self.client_address[1]))
        datos = self.rfile.read().decode('utf-8').split(' ')
        print('Segundos para EXPIRAR: ' + datos[-1])
        if datos[0] == 'REGISTER':
            direccion = datos[1].split(':')[1]
            tiempo_exp = time.gmtime(time.time() + int(datos[-1]))
            tiempo_exp = time.strftime('%Y-%m-%d %H:%M:%S', tiempo_exp)
            HoraActual = time.gmtime(time.time())
            HoraActual = time.strftime('%Y-%m-%d %H:%M:%S', HoraActual)
            self.diccionario[direccion] = [self.client_address[0], tiempo_exp]
            print('Address: ' + self.client_address[0])
            print('Fecha y hora actual: ' + HoraActual)
            print('Expires: ' + tiempo_exp + ' +0000')
            if (tiempo_exp <= HoraActual):
                del self.diccionario[direccion]
                print('Eliminada direccion: ' + direccion)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            if int(datos[-1]) == 0:  # Compruebo si expires = 0.
                del self.diccionario[datos[1]]  # Si es = 0 --> fuera.
        print('Almacenado en mi diccionario: ', self.diccionario)
        self.register2json()
        self.json2registered()

if __name__ == "__main__":

    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
