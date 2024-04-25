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
demon = False
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



