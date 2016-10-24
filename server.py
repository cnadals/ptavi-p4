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

    def register2json(self):
        # abro y escribo en un fichero llamado registered.json
        # con permiso de escritura
        with open('registered.json', 'w') as fichero:
            json.dump(self.diccionario, fichero)

    def handle(self):
        #imprimo self.client_address[0] y PUERTO por pantalla
        print('IP del cliente: ' + self.client_address[0])
        print('PUERTO del cliente: ' + str(self.client_address[1]))
        datos = self.rfile.read().decode('utf-8').split(' ')
        print('Segundos para EXPIRAR: ' + datos[-1])
        #compruebo si es register. si es, mando OK
        if datos[0] == 'REGISTER':
            self.diccionario[datos[1]] = self.client_address[0]
            direccion = datos[1].split(':')[1]
            # Transformamos la fecha de un formato a otro
            ####
            time_expires = time.gmtime(time.time() + int(datos[-1]))
            time_expires = time.strftime('%Y-%m-%d %H:%M:%S', time_expires)
            current_time = time.gmtime(time.time())
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
            self.diccionario[direccion] = [self.client_address[0], time_expires]
            print('Address:' + self.client_address[0])
            print('Expires:' + time_expires)
            #print(time_expires + ('....') + current_time)
            if (time_expires <= current_time):
                del self.diccionario[direccion]
                print('Eliminada direccion: ' + direccion)
            ####
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            if int(datos[-1]) == 0:  # Compruebo si expires = 0.
                del self.diccionario[datos[1]]  # Si es = 0 --> fuera.
        print('Almacenado en mi diccionario: ', self.diccionario)
        self.register2json()

   # def registrar(self):

if __name__ == "__main__":

    # pido el puerto por parametro
    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
