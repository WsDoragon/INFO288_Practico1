#clases server.py
import random

class Player:
    def __init__(self,nickName, ip, port, ip_server, port_server,id):
        self.nickName = nickName
        self.ip = ip
        self.port = port
        self.ip_server = ip_server
        self.port_server = port_server
        self.id = id
        self.turn = False
        self.nDice = 0
        self.hasTeam = False
        self.teamId = 0

    #posiblemente esto se borre
    def rollDice(self):
        self.nDice = random.randint(1, 6)
        self.sendPoints(self)
        self.nDice = 0

    def sendPoints(self):
        print(f"mensaje a enviar:\n"
              f"ip_server: {self.ip_server}\n"
              f"ip_port: {self.port_server}\n"
              f"puntos: {self.nDice}")

class Team:
    def __init__(self,id):
        self.id = id
        self.players = []
        self.points = 0
        self.turn = False
        self.played = 0
    
    def playersCount(self):
        return(len(self.players))
        
    def getPoints(self):
        return self.points
    
    def displayJ(self):
        if(len(self.players) == 0):
            print(f"equipo:{id} vacio")
        else:
            for x in self.players:
                print(f"jugador ip:{x.ip} port:{x.port}")
        
    
    


