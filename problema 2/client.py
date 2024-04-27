import socket
import json
import random
import threading
import queue
import time
import sys
import argparse
import os

from functions import clear_terminal

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Parseador de argumentos
parser = argparse.ArgumentParser(description='Client script with parameters.')
parser.add_argument('--host', type=str, default='192.168.1.26', help='Server host address')
parser.add_argument('--port', type=int, default=20001, help='Server port number')
parser.add_argument('--nick', type=str, default="player", help='Player nick name')
args = parser.parse_args()

# Funcion que revisa la cola de mensajes y retorna positvo o afirmativo
def getFeedback(cola,accion):
    datos = cola.get()
    if(datos["status"] == 0 and datos["action"] == accion):
        return False
    elif(datos["status"] == 1 and datos["action"] == accion):
        return True
    else:
        return False

# Hilo que recibe mensajes y los mete en cola
def recibir_mensajes():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            json_data = message.decode('utf-8')
            received_data = json.loads(json_data)
            colaMsj.put(received_data)            
        except Exception as e:
            print(f"Error al recibir mensajes del servidor: {e}")
            break

#  ------Varibles-------
#server_host = '192.168.1.26' 
#server_port = 20001
server_host = args.host    
server_port = args.port    
player_nickName = args.nick

#client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = { # Estructura de los mensajes
  "action": "c, t ,m , r, s, d", 
  "status": 0, 
  "nickName": player_nickName,
  "Dice": 0,
  "teamId":0,
  "stadis": "ss"
}

json_data = json.dumps(data)
colaMsj = queue.Queue()

# ---------- variables de control -------------

ini_demon = True
is_connected = False
has_info = False
has_elected = False
waiting_time = (random.randint(500, 5000))/1000
game_continue = True

# --------- flujo principal --------------

while game_continue:

    if ini_demon:# El hilo se ejecutará en segundo plano
        receiving_thread = threading.Thread(target=recibir_mensajes)
        receiving_thread.daemon = True  
        receiving_thread.start()
        ini_demon = False

    # Inicia la conexion con el servidor
    if not is_connected:
        data["action"] = "c"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        print("Esperando conexion con el servidor")
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"c")):
            print("conexion exitosa! \n")
            is_connected = True
    
    # Obtiene e imprime la informacion de los equipos
    if not has_info and is_connected:
        data["action"] = "t"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        
        datos = colaMsj.get()
        options = datos["stadis"].split("+")
        options[-1] = ":Nuevo"
        print("elige un equipo:\n")
        for i in range(len(options)):
            print(f"{i}:{options[i]}\n")
        has_info = True

    # Hace la eleccion | Manejo de votacion (Apruebo / Rechazo )
    if not has_elected and is_connected:
        data["action"] = "m"
        elec = int(input("opcion: "))
        data["teamId"] = elec
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #print("se envio")
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"m")):
            print("\n conexion exitosa! \n")
            has_elected = True
        else:
            print(f" \n Los integrantes de equipo: {elec} te rechazaron \n")
            has_info = False
        time.sleep(5)
    
    # Manejo de los mensajes de servidor (Juego y votaciones) -> uso de colas para no perder ninguno
    if(not colaMsj.empty()):
        datos = colaMsj.get()

        # Envio de dado
        if(datos["action"] == "r"): 
            data["action"] = "r"
            t = random.randint(1, 20)
            data["Dice"] = t
            #a = int(input("envia dado (pone un int): ")) #ingresa un int random asdasdsa
            a = input("Enter para lanzar y enviar dado... ") #ingresa un int random asdasdsa
            json_data = json.dumps(data)
            client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
            print(f"\nse envio el dado con resultado: {t}! \n ")
        
        # Recepcion de estadisticas del juego en curso
        if(datos["action"] == "s"):
            clear_terminal()
            print("Resultados de la ronda: \n ")
            resu = datos["stadis"].split("+")
            for t in resu:
                print(t)
                print("\n")
            print("\n")

        # Aviso y manejo de una votacion
        if(datos["action"] == "v"):
            print("player: ")
            print(datos["stadis"])
            print(f"quiere unirse al team: n°{elec}")
            response = input("y/n: ")
            data["action"] = "v"
            if(response == "y"):
                data["status"] = 1
            else:
                data["status"] = 0
            json_data = json.dumps(data)
            client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
            print("\n")

        # Aviso de finalizacion del juego
        if(datos["action"] == "d"):
            clear_terminal()
            print("finalizo el juego. Team ganador:")
            print(datos["stadis"])
            print("\n")
            game_continue = False
            sys.exit()
        pass
    
# Cerrar el socket al finalizar
client_socket.close()
