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

    def play(self,turn): 
        #lanzar los dados de todos los miembros - enviar mensaje de envio y espera respuestas
        if(turn):
            for x in self.players:
                x.rollDice() #cambiar por funcion que envie respuestas o hacerla aqui
            self.turn = False
        pass
    
    def playersCount(self):
        return len(self.players)
        
        
    
    


