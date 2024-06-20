import socket
import json
from queue import Queue
import random
import time
import threading
import argparse
import os

import Pyro4
from datetime import datetime

# Commit 2da prueba test

from dotenv import load_dotenv

from clases import Player
from clases import Team

from functions import has_conex
from functions import verificar_equipos
from functions import get_index
from functions import clear_terminal



parser = argparse.ArgumentParser(description='Server script with parameters.')
parser.add_argument('--env', type=str, default='.envserver', help='Server environment file name')
args = parser.parse_args()

load_dotenv(args.env)

# Hilo (thread) que maneja las votaciones - Las votaciones van en FIFO dentro de la cola waitingConnect
def votes_management(equipos,jugadores):
     global waitingConnect
     while True:
          if(not waitingConnect.empty()): # Verifica que hay votaciones pendientes, si hay las recupera y ejecuta
               finish = False
               info = waitingConnect.get()
               gente = len(equipos[info[0]].players)
               for x in equipos[info[0]].players:
                sendFeedback(feedback,"v",1,"server",0,jugadores[info[2]].nickName,(x.ip,x.port)) # Envia pregunta a los integrantes de team x
               time.sleep(3)
               while(not finish):
                    hg = 0
                    positive = 0
                    for y in equipos[info[0]].players: # Recuento de votos
                         if (y.voted == 1):
                            hg += 1
                         if (y.aprove == 1):
                            positive += 1

                    if(gente == hg): # Verifica si votaron todos, si no espera y reinicia el recuento
                        finish = True
                        if(positive == gente): # Aceptacion del miembro
                            sendFeedback(feedback,"m",1,"server",1,"",info[1])                    
                            equipos[info[0]].players.append(jugadores[info[2]])
                            colaLogs.put(generate_log_entry("TEAM_MANAGEMENT",0,1,host,"n/a",f"GET_INTO_TEAM: {equipos[info[0]].id}"))
                        else: # Rechazo del miembro
                            sendFeedback(feedback,"m",0,"server",0,"",info[1])
                            colaLogs.put(generate_log_entry("TEAM_MANAGEMENT",0,1,host,"n/a",f"REJECT: {equipos[info[0]].id}"))
                         
                    time.sleep(1)

               # Limpieza de varibles de votación de los objetos players
               for y in equipos[info[0]].players:
                y.voted = 3
                y.aprove = 3
                colaLogs.put(generate_log_entry("VOTE_MANAGEMENT",0,1,host,equipos[info[0]].id,f"NICK: {jugadores[info[2]].nickName}"))
          else:
               time.sleep(5)
     

# Hilo (thread) que maneja el partido (time.sleep para esperar que los jugadores envien sus dados)
def game(equipos,jugadores):
    print("Inicio el partido!")
    game_continue = True
    while game_continue:
        for x in equipos:
            colaLogs.put(generate_log_entry("GAME_RUNNING",1,0,host,x.id,f"NPLAYERS: {len(x.players)}"))
            for y in x.players:
                sendFeedback(feedback,"r",1,"server",0,"",(y.ip,y.port)) # Aviso a los integrantes de un equipo de su turno
            time.sleep(10)
            while(x.played < len(x.players)): # Verifica que todos jugaron y pasa al siguiente equipo. si no espera
                print(f"esperando a jugadores del Equipo: {x.id}")
                time.sleep(3)
            x.played = 0
            colaLogs.put(generate_log_entry("GAME_RUNNING",0,1,host,x.id,f"NPLAYERS: {len(x.players)}"))
        
        # Enviar puntajes totales al final de la ronda a todos los jugadores
        colaLogs.put(generate_log_entry("SEND_GAME_STATS",1,0,host,"",""))
        msj = ""
        for t in equipos:
             msj += f"Team: {t.id} - Points {t.getPoints()} +"
        
        for x in equipos:
            for y in x.players:
                sendFeedback(feedback,"s",1,"server",0,msj,(y.ip,y.port))
            if(x.points >= puntuacionLimite): # Condicion de ganar el partido
                 game_continue = False
                 winner:id = x.id
        colaLogs.put(generate_log_entry("SEND_GAME_STATS",0,1,host,"",msj))
        
        # Imprime  puntajes en terminal del servidor
        clear_terminal()
        print("\n")
        for x in equipos:
             print(f"Team: {x.id} - Points: {x.getPoints()} \n")

        time.sleep(2)

        if (not game_continue):
             #Termina el partido
            colaLogs.put(generate_log_entry("SEND_GAME_END",1,0,host,"",""))
            for x in equipos:
                for y in x.players:
                    sendFeedback(feedback,"d",1,"server",0,winner,(y.ip,y.port)) # Envio de resultados a jugadores
             #enviar mensaje de final de partido y ganador
            colaLogs.put(generate_log_entry("SEND_GAME_END",0,1,host,"",""))

        
    print(f"finalizó la partida - reiniciar server para iniciar una nueva - gano team: {winner}")
             

# Funcion que toma el json, lo modifica y envia al taget = (ip,port)
def sendFeedback(feedback,act,stat,nick,ndice,stadis,target):
    feedback["action"] = act
    feedback["status"] = stat
    feedback["nickName"] = nick
    feedback["dice"] = ndice
    feedback["stadis"] = stadis
    
    json_data = json.dumps(feedback)
    #print(f"enviando mensaje: {json_data} a {target}")
    server_socket.sendto(json_data.encode('utf-8'), target)

def generate_log_entry(action, inicio, fin, player, team, extra):
    timestamp = datetime.now().isoformat()
    return f"{timestamp} | {action} | {os.getenv('GAME_NUM')} | {inicio} | {fin} | {player} | {team} | {extra} |"


def send_logs():
    # Connect to the name server --HILO
    ns = Pyro4.locateNS()
    uri = ns.lookup("example.logserver")
    log_server = Pyro4.Proxy(uri)  # Create a proxy for the log server object
    while True:
        if(not colaLogs.empty()):
            log_entry = colaLogs.get()
            response = log_server.add_log(log_entry)
        else:
            pass


# crear conexion

#host = '192.168.1.26'  
#port = 20002
host = os.getenv('HOST')
port = int(os.getenv('PORT'))
puntuacionLimite = int(os.getenv('MAX_POINTS'))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

# ---------- variables de control -------------

MAX_USERS_PER_IP = 64
jugadores = []
waitingConnect = Queue()
demon_game = False
flag_votacion = False
demon_vote = False

colaLogs = Queue()

pt = Team(0)
st = Team(1)
equipos = []
equipos.append(pt)
equipos.append(st)

nEquiposMax = int(os.getenv("MAX_TEAMS")) # maximo de equipos en servidor
maxPlayerPerTeam = int(os.getenv("MAX_PER_TEAM")) # maximo de jugadores por equipo

firstConex = True
idCounter = 0


feedback = { # Estructura de los mensajes
  "action": "c, t ,m , r, s, d", 
  "status": 0, 
  "nickName": "Server",
  "Dice": 0,
  "maxDice": os.getenv("MAX_DICE"),
  "teamId":0,
  "stadis": "ss",
  "gameNum": os.getenv("GAME_NUM")
}

# --------- flujo principal --------------

print(f"Servidor UDP escuchando en {host}:{port}")
sending_thread = threading.Thread(target=send_logs)
sending_thread.daemon = True  
sending_thread.start()


while True:

    # Recepcion de la informacion
    data, addr = server_socket.recvfrom(1024)  # 1024 es el tamaño máximo de datos que se puede recibir
    json_data = data.decode('utf-8')
    received_data = json.loads(json_data) # Convertir la cadena JSON de vuelta a un diccionario

    # Recibir e inscribir jugador en el servidor -> se guarda en lista "jugadores"
    if received_data["action"] == "c" and not has_conex(addr[0],addr[1],jugadores):
            colaLogs.put(generate_log_entry("PLAYER_REG",1,0,host,"n/a",f"NICK: {received_data['nickName']}"))
            new_player = Player(received_data["nickName"],addr[0],addr[1],host,port,idCounter)
            jugadores.append(new_player)
            idCounter += 1            
            sendFeedback(feedback,"c",1,"you",0,"",addr)
            colaLogs.put(generate_log_entry("PLAYER_REG",0,1,host,"n/a",f"NICK: {received_data['nickName']}"))

    # Enviar informacion de los teams para que el jugador decida a cual unirse o crear uno nuevo 
    if received_data["action"] == "t":
         colaLogs.put(generate_log_entry("SEND_TEAM_INFO",1,0,host,"n/a",f"NICK: {received_data['nickName']}"))
         msj = ""
         for x in equipos:
            msj+= f"E:{x.id} - P:{x.playersCount()} +"  # se agrega "+" para hacer .split() en el client
         sendFeedback(feedback,"t",1,"you",0,msj,addr)
         colaLogs.put(generate_log_entry("SEND_TEAM_INFO",0,1,host,"n/a",f"NICK: {received_data['nickName']}"))
    
    #Manejo de seleccion de equipo -> puede resultar en votaciones, unirse o crear un nuevo equipo
    if received_data["action"] == "m":
          colaLogs.put(generate_log_entry("TEAM_MANAGEMENT",1,0,host,"n/a",f"NICK: {received_data['nickName']}"))
          j = get_index(addr[0],addr[1],jugadores)
          if received_data["teamId"] >= nEquiposMax:
              sendFeedback(feedback,"m",0,"you",0,"",addr)
          else:
          # Crear un nuevo equipo
               if received_data["teamId"] > len(equipos)-1:
                    new_team = Team(received_data["teamId"])
                    equipos.append(new_team)
                    colaLogs.put(generate_log_entry("TEAM_MANAGEMENT",0,1,host,"n/a",f"CREATE_NEW_TEAM: {received_data['teamId']}"))
          
          # Entra a votacion de los intengrantes de un equipo en dejarlo unirse
               if (len(equipos[received_data["teamId"]].players)>0) and (len(equipos[received_data["teamId"]].players) + 1 <= maxPlayerPerTeam):
                    colaLogs.put(generate_log_entry("VOTE_MANAGEMENT",1,0,host,received_data['teamId'],f"NICK: {received_data['nickName']}"))
                    u = [received_data["teamId"],addr,j]
                    waitingConnect.put(u)
                    if(not demon_vote):
                         vote_thread = threading.Thread(target=votes_management,kwargs={"equipos":equipos, "jugadores": jugadores})
                         vote_thread.daemon = True  
                         vote_thread.start()
                         demon_vote = True                        
               
               
               elif (len(equipos[received_data["teamId"]].players) + 1 > maxPlayerPerTeam):
                    sendFeedback(feedback,"m",0,"you",0,"",addr)
                    colaLogs.put(generate_log_entry("TEAM_MANAGEMENT",0,1,host,"n/a",f"REJECT: {received_data['teamId']}"))
                    
                    pass
               
               # Se une ya que el Equipo esta vacio
               else:
                    equipos[received_data["teamId"]].players.append(jugadores[j])
                    sendFeedback(feedback,"m",1,"you",0,"",addr)
                    colaLogs.put(generate_log_entry("TEAM_MANAGEMENT",0,1,host,"n/a",f"GET_INTO_TEAM: {received_data['teamId']}"))
         
          if (firstConex):
               demon_game = True
               firstConex = False
         
    # Recepcion de los resultados de lanzar dados por parte de los jugadores
    if received_data["action"] == "r":
         jt = received_data["teamId"]
         result = received_data["Dice"]
         equipos[jt].points += result
         equipos[jt].played += 1

    # Manejo de los votos para la union de un jugador a un equipo
    if received_data["action"] == "v":
         j = get_index(addr[0],addr[1],equipos[received_data["teamId"]].players)
         print(j)
         if received_data["status"] == 1:
              equipos[received_data["teamId"]].players[j].aprove = 1
              pass
         else:
              equipos[received_data["teamId"]].players[j].aprove = 0
              pass
         equipos[received_data["teamId"]].players[j].voted = 1
              
    # Detecta que hay al menos 2 equipos con un minimo de 1 jugador e inicia el partido
    if demon_game and verificar_equipos(equipos):
            game_thread = threading.Thread(target=game,kwargs={"equipos":equipos, "jugadores": jugadores})
            game_thread.daemon = True  
            game_thread.start()
            demon_game = False
            pass
    
    if(demon_vote):
         pass
                 
    print("\n")
    for x in equipos:
         print(f"Team:{x.id} - Players:{x.playersCount()} \n")
    
# Cerrar el socket al finalizar
server_socket.close()



