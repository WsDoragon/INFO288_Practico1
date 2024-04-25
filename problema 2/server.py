import socket
import signal
import sys
import threading

import time

from clases import Player
from clases import Team
from functions import registered
from functions import verificar_equipos

#from matchMaking import matchMaking
#from matchManagment import matchManagment

def matchMaking(servidor_socket,lista_jugadores):
    while True:
        print("aaaa")
        print(lista_jugadores[0].ip)
        print(lista_jugadores[0].port)
        mensaje = "envio desde hilo manin!!"
        servidor_socket.sendto(mensaje.encode('utf-8'), (lista_jugadores[0].ip,lista_jugadores[0].port))
        time.sleep(15)


def manejar_conexion(conexion, direccion_cliente):
    global hiloMatchMaking
    global hiloMatchManagment
    print(f"Conexión entrante desde {direccion_cliente}")

    try:
        while True:
            # Recibir datos del cliente
            datos = conexion.recv(1024)
            if not datos:
                break

            mensaje_cliente = datos.decode()
            print(f"Mensaje recibido del cliente {direccion_cliente}: {mensaje_cliente}")
            
            if(registered(direccion_cliente[0],direccion_cliente[1],jugadores)):
                #enviar mensaje con info de los teams disponibles
                # dar las opciones a: unirse a un team: b crear uno y unirse a ese
                
                pass
            else:
                u = Player(mensaje_cliente,direccion_cliente[0],direccion_cliente[1],ip_servidor,puerto_servidor)
                jugadores.append(u)
                pass

            # Enviar respuesta al cliente
            respuesta = f"Me llegó tu mensaje: {mensaje_cliente}"
            conexion.sendall(respuesta.encode())

            if(len(jugadores)>0 and hiloMatchMaking):
                #ejecutar el hilo de ingresar a equipo o crear equipo
                hiloMatchMakingObj.start()
                hiloMatchMaking = False
                pass

            if(verificar_equipos(teams) and hiloMatchManagment):
                #ejecutar hilo de juego
                hiloMatchManagment = False
                pass

    except KeyboardInterrupt:
        print("Se recibió una señal de interrupción. Cerrando la conexión con el cliente.")
    finally:
        # Cerrar la conexión
        conexion.close()

def iniciar_servidor(ip, puerto):
    # Crear un objeto socket TCP/IP
    # servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Permitir reutilizar el puerto después de cerrar el socket
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enlazar el socket a la dirección y puerto especificados
        servidor_socket.bind((ip, puerto))

        # Escuchar por conexiones entrantes
        servidor_socket.listen(5)

        print(f"Servidor escuchando en {ip}:{puerto}")

        while True:
            # Esperar por una conexión
            conexion, direccion_cliente = servidor_socket.accept()
            manejar_conexion(conexion, direccion_cliente)

    except KeyboardInterrupt:
        print("Se recibió una señal de interrupción. Cerrando el servidor.")
        servidor_socket.close()
        sys.exit()
    except ConnectionRefusedError:
        print("No se pudo establecer conexión con el cliente.")

    finally:
        # Cerrar el socket del servidor
        #servidor_socket.close()
        pass

if __name__ == "__main__":
    # Dirección IP y puerto en el que escuchará el servidor
    ip_servidor = "127.0.0.1"  
    puerto_servidor = 12345

    # Iniciar el servidor
    jugadores = []
    nTeams = 2
    teams = []
    pt = Team(1)
    st = Team(2)
    teams.append(pt)
    teams.append(st)

    hiloMatchMaking = True
    hiloMatchManagment = True 

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   


    hiloMatchMakingObj = threading.Thread(target=matchMaking,kwargs={"servidor_socket":servidor_socket,"lista_jugadores":jugadores})

    iniciar_servidor(ip_servidor, puerto_servidor)


