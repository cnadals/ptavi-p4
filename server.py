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
    # creo mi diccionario vacio
    diccionario = {}

    def json2registered(self):
        """
        Comprobacion existencia fichero
        """
        # compruebo si existe un fichero registered.json
        try:
            with open('registered.json', 'r') as fichero:
                self.diccionario = json.load(fichero)
        except:
            pass

    def register2json(self):
        """
        Creacion de fichero
        """
        # abro y escribo en un fichero llamado registered.json
        # con permiso de escritura
        with open('registered.json', 'w') as fichero:
            json.dump(self.diccionario, fichero)

    def handle(self):
        """
        Manejador
        """
        if len(self.diccionario) == 0:
            self.json2registered()
        #imprimo IP y PUERTO por pantalla
        print('IP del cliente: ' + self.client_address[0])
        print('PUERTO del cliente: ' + str(self.client_address[1]))
        datos = self.rfile.read().decode('utf-8').split(' ')
        print('Segundos para EXPIRAR: ' + datos[-1])
        #compruebo si es register. si es, mando OK
        if datos[0] == 'REGISTER':
            #self.diccionario[datos[1]] = self.client_address[0]
            direccion = datos[1].split(':')[1]
            # Transformamos la fecha de un formato a otro
            # Mi tiempo de expiracion --> formato
            tiempo_exp = time.gmtime(time.time() + int(datos[-1]))
            tiempo_exp = time.strftime('%Y-%m-%d %H:%M:%S', tiempo_exp)
            # Tiempo de expiracion --> formato
            HoraActual = time.gmtime(time.time())
            HoraActual = time.strftime('%Y-%m-%d %H:%M:%S', HoraActual)
            self.diccionario[direccion] = [self.client_address[0], tiempo_exp]
            print('Address: ' + self.client_address[0])
            print('Fecha y hora actual: ' + HoraActual)    
            print('Expires: ' + tiempo_exp + ' +0000')
            # Si tiempo de expiracion es mayor que el que ha pasado, elimino
            if (tiempo_exp <= HoraActual):
                del self.diccionario[direccion]
                print('Eliminada direccion: ' + direccion)
            # Escribo la info en mi fichero
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            if int(datos[-1]) == 0:  # Compruebo si expires = 0.
                del self.diccionario[datos[1]]  # Si es = 0 --> fuera.
        print('Almacenado en mi diccionario: ', self.diccionario)
        self.register2json()
        self.json2registered()

if __name__ == "__main__":

    # pido el puerto por parametro
    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
