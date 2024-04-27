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

def votes_management(equipos,jugadores):
     global waitingConnect
     while True:
          if(not waitingConnect.empty()):
               finish = False
               #logica de votación u = [received_data["teamId"],addr]
               info = waitingConnect.get()
               gente = len(equipos[info[0]].players)
               for x in equipos[info[0]].players:
                sendFeedback(feedback,"v",1,"server",0,"",(x.ip,x.port))
               time.sleep(3)
               while(not finish):
                    hg = 0
                    positive = 0
                    for y in equipos[info[0]].players:
                         if (y.voted == 1):
                            hg += 1
                         if (y.aprove == 1):
                            positive += 1

                    if(gente == hg):
                        finish = True
                        if(positive == gente):
                            sendFeedback(feedback,"m",1,"server",1,"",info[1])                    
                            #meterlo al team
                            equipos[info[0]].players.append(jugadores[info[2]])
                        else:
                            sendFeedback(feedback,"m",0,"server",0,"",info[1])
                         
                    time.sleep(1)
               for y in equipos[info[0]].players:
                y.voted = 3
                y.aprove = 3
          else:
               time.sleep(5)
     

def game(equipos,jugadores):
    print("Inicio el partido!")
    game_continue = True
    while game_continue:
        for x in equipos:
            for y in x.players:
                sendFeedback(feedback,"r",1,"server",0,"",(y.ip,y.port))
            time.sleep(10) #en main todos los jugadores a los que les llego el msj deberian enviar sus dados y ser sumados
            while(x.played < len(x.players)):
                time.sleep(3)
                print("esperando...")
            x.played = 0
        
        #enviar puntajes
        msj = ""
        for t in equipos:
             msj += f"Team: {t.id} - Points {t.getPoints()} +"
        
        for x in equipos:
            for y in x.players:
                sendFeedback(feedback,"s",1,"server",0,msj,(y.ip,y.port))
            if(x.points >= 15):
                 game_continue = False
                 winner:id = x.id
        
        #print puntajes en terminal
        print("\n")
        for x in equipos:
             print(f"Team: {x.id} - Points: {x.getPoints()} \n")

        time.sleep(2)

        if (not game_continue):
            for x in equipos:
                for y in x.players:
                    sendFeedback(feedback,"d",1,"server",0,winner,(y.ip,y.port))
             #enviar mensaje de final de partido y ganador
             

        #print(msj)
    print(f"finalizó la partida - reiniciar server para iniciar una nueva - gano team: {winner}")
             

def sendFeedback(feedback,act,stat,nick,ndice,stadis,target):
    feedback["action"] = act
    feedback["status"] = stat
    feedback["nickName"] = nick
    feedback["dice"] = ndice
    feedback["stadis"] = stadis
    json_data = json.dumps(feedback)
    server_socket.sendto(json_data.encode('utf-8'), target)

# crear conexion
host = '192.168.1.5'  
port = 20001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

# variables 
MAX_USERS_PER_IP = 64
jugadores = []
waitingConnect = Queue()
demon_game = False
flag_votacion = False
demon_vote = False

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
    #print(received_data)

        
    if received_data["action"] == "c" and not has_conex(addr[0],addr[1],jugadores):
            new_player = Player(received_data["nickName"],addr[0],addr[1],'192.168.1.26',20001,idCounter)
            jugadores.append(new_player)
            idCounter += 1            
            sendFeedback(feedback,"c",1,"you",0,"",addr)

    if received_data["action"] == "t":
         #enviar info de los teams
         msj = ""
         for x in equipos:
            msj+= f"E:{x.id} - P:{x.playersCount()} +"
         sendFeedback(feedback,"t",1,"you",0,msj,addr)
    
    if received_data["action"] == "m":
          #print("aki")
          j = get_index(addr[0],addr[1],jugadores)
          #print(type(received_data["teamId"]))
          if received_data["teamId"] > len(equipos)-1:
              new_team = Team(received_data["teamId"])
              #new_team.players.append(jugadores[j])
              equipos.append(new_team)
              #print("###############\nIntregranres del equipo: \n###############")
              #print(equipos[received_data["teamId"]].players)
         
          if (len(equipos[received_data["teamId"]].players)>0):
               #votes_management(equipos[received_data["teamId"]],jugadores[j])
               u = [received_data["teamId"],addr,j]
               waitingConnect.put(u)
               if(not demon_vote):
                    vote_thread = threading.Thread(target=votes_management,kwargs={"equipos":equipos, "jugadores": jugadores})
                    vote_thread.daemon = True  
                    vote_thread.start()
                    demon_vote = True                        
          else:
              equipos[received_data["teamId"]].players.append(jugadores[j])
              sendFeedback(feedback,"m",1,"you",0,"",addr)
         
          if (firstConex):
               demon_game = True
               firstConex = False
         
    
    if received_data["action"] == "r":
         #
         jt = received_data["teamId"]
         result = received_data["Dice"]
         equipos[jt].points += result
         equipos[jt].played += 1

    if received_data["action"] == "v":
         j = get_index(addr[0],addr[1],equipos[received_data["teamId"]].players)
         print("xd  ")
         print(j)
         if received_data["status"] == 1:
              equipos[received_data["teamId"]].players[j].aprove = 1
              pass
         else:
              equipos[received_data["teamId"]].players[j].aprove = 0
              pass
         equipos[received_data["teamId"]].players[j].voted = 1
              
    if demon_game and verificar_equipos(equipos):
            game_thread = threading.Thread(target=game,kwargs={"equipos":equipos, "jugadores": jugadores})
            game_thread.daemon = True  
            game_thread.start()
            demon_game = False
            pass
    
    if(demon_vote):
         pass
         
    """
    print("Lista de clientes conectados por IP:")
    for cliente in jugadores:
        print(f"IP: {cliente.ip}")
        print(f"Puerto: {cliente.port}")
        print("---------------")  # Separador entre clientes
    """        
    print("\n")
    for x in equipos:
         print(f"Team:{x.id} - Players:{x.playersCount()} \n")
    
# Cerrar el socket al finalizar
server_socket.close()



