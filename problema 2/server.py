import socket
import json
from queue import Queue
import random
import time
import threading

from clases import Player
from clases import Team

from functions import has_conex
from functions import verificar_equipos
from functions import get_index


def game(equipos,jugadores):
    while True:
        for x in equipos:
            for y in x.players:
                sendFeedback(feedback,"r",1,"server",0,"",(y.ip,y.port))
            time.sleep(10) #en main todos los jugadores a los que les llego el msj deberian enviar sus dados y ser sumados
            while(x.played < len(x.players)):
                time.sleep(5)
                print("esperando...")
            x.played = 0
        
        #enviar puntajes
        msj = ""
        for t in equipos:
             msj += str(t.id)
             msj += "="
             msj += str(t.getPoints())
             msj += " | "
        
        for x in equipos:
            for y in x.players:
                sendFeedback(feedback,"s",1,"server",0,msj,(y.ip,y.port))
        
        time.sleep(7)
        print(msj)
             

def sendFeedback(feedback,act,stat,nick,ndice,stadis,target):
    feedback["action"] = act
    feedback["status"] = stat
    feedback["nickName"] = nick
    feedback["dice"] = ndice
    feedback["stadis"] = stadis
    json_data = json.dumps(feedback)
    server_socket.sendto(json_data.encode('utf-8'), target)

# crear conexion
host = '192.168.1.26'  
port = 20001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

# variables 
MAX_USERS_PER_IP = 64
jugadores = []
waitingConnect = Queue()
demon_game = False

pt = Team(0)
st = Team(1)
equipos = []
equipos.append(pt)
equipos.append(st)


firstConex = True
idCounter = 0


feedback = {
  "action": "c, t ,m , r, s, d", 
  "status": 0, 
  "nickName": "Server",
  "Dice": 0,
  "teamId":0,
  "stadis": "ss"
}

#addr[0] ip
#addr[1] puerto

print(f"Servidor UDP escuchando en {host}:{port}")

while True:
    data, addr = server_socket.recvfrom(1024)  # 1024 es el tamaño máximo de datos que se puede recibir
    json_data = data.decode('utf-8')
    received_data = json.loads(json_data)# Convertir la cadena JSON de vuelta a un diccionario
    print(received_data)

    if demon_game and verificar_equipos(equipos):
            game_thread = threading.Thread(target=game,kwargs={"equipos":equipos, "jugadores": jugadores})
            game_thread.daemon = True  
            game_thread.start()
            demon_game = False
            pass
        
    if received_data["action"] == "c" and not has_conex(addr[0],addr[1],jugadores):
            new_player = Player(received_data["nickName"],addr[0],addr[1],'192.168.1.26',20001,idCounter)
            jugadores.append(new_player)
            idCounter += 1            
            sendFeedback(feedback,"c",1,"you",0,"",addr)

    if received_data["action"] == "t":
         #enviar info de los teams
         msj = ""
         for x in equipos:
              msj += x.playersCount()
         sendFeedback(feedback,"t",1,"you",0,msj,addr)
    
    if received_data["action"] == "m":
         print("aki")
         j = get_index(addr[0],addr[1],jugadores)
         print(type(received_data["teamId"]))
         if received_data["teamId"] > len(equipos)-1:
              new_team = Team(received_data["teamId"])
              new_team.players.append(jugadores[j])
              equipos.append(new_team)
         else:
              equipos[received_data["teamId"]].players.append(jugadores[j])
         
         if (firstConex):
            demon_game = True
            firstConex = False
    
    if received_data["action"] == "r":
         #j = get_index(addr[0],addr[1],jugadores)
         jt = received_data["teamId"]
         result = received_data["Dice"]
         equipos[jt].points += result
         equipos[jt].played += 1
         
        
    print("Lista de clientes conectados por IP:")
    for cliente in jugadores:
        print(f"IP: {cliente.ip}")
        print(f"Puerto: {cliente.port}")
        print("---------------")  # Separador entre clientes

    serverStats = ""
    for x in equipos:
        serverStats += x.playersCount()
    print(serverStats.split("+"))
    
# Cerrar el socket al finalizar
server_socket.close()



