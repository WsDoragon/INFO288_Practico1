import socket
import json
import random
import threading
import queue
import time
import sys
import argparse
import os
import Pyro4
from datetime import datetime

from functions import clear_terminal

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Parseador de argumentos
parser = argparse.ArgumentParser(description='Client script with parameters.')
parser.add_argument('--host', type=str, default='127.0.0.1', help='Server host address')
parser.add_argument('--port', type=int, default=20001, help='Server port number')
parser.add_argument('--nick', type=str, default="player", help='Player nick name')
parser.add_argument('--game', type=str, default="Juego_1", help='Game number to log')
args = parser.parse_args()

def generate_log_entry(action, inicio, fin, player, team, extra):
    timestamp = datetime.now().isoformat()
    return f"{timestamp} | {action} | {game_num} | {inicio} | {fin} | {player} | {team} | {extra} |"

# Funcion que revisa la cola de mensajes y retorna positvo o afirmativo
def getFeedback(cola,accion):
    datos = cola.get()
   
    #print(datos)
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
            print("respuesta: ")
            time.sleep(1) #Solucion bug windows
            message= client_socket.recv(1024)
            json_data = message.decode('utf-8')
            received_data = json.loads(json_data)
            colaMsj.put(received_data)            
        except Exception as e:
            print(f"Error al recibir mensajes del servidor: {e}")
            break

def send_logs():
    # Connect to the name server
    ns = Pyro4.locateNS()
    uri = ns.lookup("example.logserver")
    log_server = Pyro4.Proxy(uri)  # Create a proxy for the log server object
    while True:
        if(not colaLogs.empty()):
            log_entry = colaLogs.get()
            response = log_server.add_log(log_entry)
        else:
            pass


#  ------Varibles-------
#server_host = '192.168.1.26' 
#server_port = 20001
server_host = args.host    
server_port = args.port    
player_nickName = args.nick
game_num = args.game


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
colaLogs = queue.Queue()

# ---------- variables de control -------------

ini_demon = True
is_connected = False
has_info = False
has_elected = False
waiting_time = (random.randint(500, 5000))/1000
game_continue = True
maxDiceNumber = 20

# --------- flujo principal --------------

while game_continue:

    if ini_demon:# Los hilos se ejecutarán en segundo plano
        receiving_thread = threading.Thread(target=recibir_mensajes)
        receiving_thread.daemon = True  
        receiving_thread.start()

        sending_thread = threading.Thread(target=send_logs)
        sending_thread.daemon = True  
        sending_thread.start()

        ini_demon = False

    # Inicia la conexion con el servidor
    if not is_connected:
        colaLogs.put(generate_log_entry("INI_CONEX",1,0,player_nickName,"n/a",""))
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
            
            colaLogs.put(generate_log_entry("INI_CONEX",0,1,player_nickName,"n/a",""))
            is_connected = True
    
    # Obtiene e imprime la informacion de los equipos
    if not has_info and is_connected:
        colaLogs.put(generate_log_entry("GET_TEAM_DATA",1,0,player_nickName,"n/a",""))
        data["action"] = "t"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        
        datos = colaMsj.get()
        maxDiceNumber = int(datos["maxDice"])
        options = datos["stadis"].split("+")
        options[-1] = ":Nuevo"
        print("elige un equipo:\n")
        for i in range(len(options)):
            print(f"{i}:{options[i]}\n")
        has_info = True
        colaLogs.put(generate_log_entry("GET_TEAM_DATA",0,1,player_nickName,"n/a",""))

    # Hace la eleccion | Manejo de votacion (Apruebo / Rechazo )
    if not has_elected and is_connected:
        colaLogs.put(generate_log_entry("SELECT_TEAM",1,0,player_nickName,"n/a",""))
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
            print(f" \n Error al unirse al equipo: {elec}\n")
            has_info = False
        colaLogs.put(generate_log_entry("SELECT_TEAM",0,1,player_nickName,elec,""))
        time.sleep(5)
    
    # Manejo de los mensajes de servidor (Juego y votaciones) -> uso de colas para no perder ninguno
    if(not colaMsj.empty()):
        datos = colaMsj.get()

        # Envio de dado
        if(datos["action"] == "r"): 
            colaLogs.put(generate_log_entry("GAME_ACTIONS",1,0,player_nickName,elec,"SEND_DICE"))
            data["action"] = "r"
            t = random.randint(1, maxDiceNumber)
            data["Dice"] = t
            #a = int(input("envia dado (pone un int): ")) #ingresa un int random asdasdsa
            a = input("Enter para lanzar y enviar dado... ") #ingresa un int random asdasdsa
            json_data = json.dumps(data)
            client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
            print(f"\nse envio el dado con resultado: {t}! \n ")
            colaLogs.put(generate_log_entry("GAME_ACTIONS",0,1,player_nickName,elec,f"SEND_DICE: {t}"))
        
        # Recepcion de estadisticas del juego en curso
        if(datos["action"] == "s"):
            colaLogs.put(generate_log_entry("GAME_ACTIONS",1,0,player_nickName,elec,"GET_GAME_STATS"))
            clear_terminal()
            print("Resultados de la ronda: \n ")
            resu = datos["stadis"].split("+")
            for t in resu:
                print(t)
                print("\n")
            print("\n")
            colaLogs.put(generate_log_entry("GAME_ACTIONS",0,1,player_nickName,elec,"GET_GAME_STATS"))

        # Aviso y manejo de una votacion
        if(datos["action"] == "v"):
            colaLogs.put(generate_log_entry("GAME_ACTIONS",1,0,player_nickName,elec,"VOTE_MANAGEMENT"))
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
            #colaLogs.put(generate_log_entry("GAME_ACTIONS",0,1,player_nickName,elec,f"VOTE_MANAGEMENT: {datos["stadis"]} -> {response}"))
            colaLogs.put(generate_log_entry("GAME_ACTIONS", 0, 1, player_nickName, elec, f"VOTE_MANAGEMENT: {datos['stadis']} -> {response}"))


        # Aviso de finalizacion del juego
        if(datos["action"] == "d"):
            colaLogs.put(generate_log_entry("GAME_ACTIONS",1,0,player_nickName,elec,"END_GAME"))
            clear_terminal()
            print("finalizo el juego. Team ganador:")
            print(datos["stadis"])
            print("\n")
            game_continue = False
            colaLogs.put(generate_log_entry("GAME_ACTIONS",0,1,player_nickName,elec,f"END_GAME: team winner -> {datos['stadis']}"))
            sys.exit()
        pass
    
# Cerrar el socket al finalizar
client_socket.close()
