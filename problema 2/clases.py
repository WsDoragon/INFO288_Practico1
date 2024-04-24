#clases server.py
import random

import random

class Player:
    def __init__(self, nickName, ip, port, ip_server, port_server):
        self.nickName = nickName
        self.ip = ip
        self.port = port
        self.ip_server = ip_server
        self.port_server = port_server
        self.turn = False
        self.nDice = 0

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

    def play(self,turn): 
        #lanzar los dados de todos los miembros
        if(turn):
            for x in self.players:
                x.rollDice()
            self.turn = False
        pass
    
    def playersCount(self):
        return len(self.players)
        
        
    
    


