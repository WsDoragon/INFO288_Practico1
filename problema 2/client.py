import socket
import json
import random
import threading
import queue
import time


def getFeedback(cola,accion):
    datos = cola.get()
    if(datos["status"] == 0 and datos["action"] == accion):
        return False
    elif(datos["status"] == 1 and datos["action"] == accion):
        return True
    else:
        return False

def sendMsj(msj):
    data["action"] = msj
    json_data = json.dumps(data)
    client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))

def recibir_mensajes():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            json_data = message.decode('utf-8')
            received_data = json.loads(json_data)
            colaMsj.put(received_data)
            print(received_data) #aki
        except Exception as e:
            print(f"Error al recibir mensajes del servidor: {e}")
            break

#  ------Varibles-------
server_host = '192.168.1.26' 
server_port = 20001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


data = {
  "action": "c, t ,m , r, s, d", 
  "status": 0, 
  "nickName": "Server",
  "Dice": 0,
  "teamId":0
}

json_data = json.dumps(data)
colaMsj = queue.Queue()




# ---------- variables de control -------------

ini_demon = True
is_connected = False
waiting_time = (random.randint(500, 5000))/1000



# --------- flujo principal --------------

while True:

    if ini_demon:# El hilo se ejecutará en segundo plano
        receiving_thread = threading.Thread(target=recibir_mensajes)
        receiving_thread.daemon = True  
        receiving_thread.start()
        ini_demon = False

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
    
# Cerrar el socket al finalizar
client_socket.close()
