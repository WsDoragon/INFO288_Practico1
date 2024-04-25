

"""
Se activará cuando el largo de la lista de players sea distinta de 0
pasos a seguir:
    1- enviar info de los teams disponibles
    2- esperar a que el player eliga unirse o crear
    3- hacer el management de lo anterior    
"""

import threading
import time
import socket

def matchMaking(servidor_socket,lista_jugadores):
    while True:
        mensaje = "envio desde hilo manin!!"
        servidor_socket.sendto(mensaje.encode('utf-8'), (lista_jugadores[0].ip,lista_jugadores[0].port))
        time.sleep(15)

