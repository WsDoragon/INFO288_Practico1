import os
import sys
import matplotlib.pyplot as plt

import actionsPerUser
import usersPerTeam
import playersInTime
import teamsInTime
import scoreCurves
from dotenv import load_dotenv

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def divide_centra_log(path):
    archive = open(path, "r")

    # Lee el contenido del archivo
    contenido = archive.read()
    # Divide el contenido en líneas
    lineas = contenido.split("\n")
    games_logs = {}

    # Itera sobre cada línea
    for linea in lineas:
        # Divide la línea en partes usando el separador "|"
        partes = linea.split("|")
        if len(partes) > 2:
            #timestamp | accion | Juego[N°] | Inicio | Fin | Player | Team | extra
            actual_game = partes[2].strip()
            if actual_game not in games_logs:
                games_logs[actual_game] = []
            
            games_logs[actual_game].append(linea)

    # Cierra el archivo
    archive.close()
    # Recorrer games_logs y guardar en un archivo txt cada juego
    for game in games_logs:
        archivo = open(f"./gameLogs/game_{game}.txt", "w")
        for log in games_logs[game]:
            archivo.write(log + "\n")
        archivo.close()

# -------------------Main-------------------- #

# solicitar args de ejecucion
if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
    print("Error: Problema en la ejecucion de argumentos\nEjecucion: python main.py path_to_log \nEjemplo: python main.py ../gameLog.txt \n\n")
    sys.exit()

path_to_log = sys.argv[1]
divide_centra_log(path_to_log)

load_dotenv()

# leer todos los archivos de gameLogs
logs_path = "./gameLogs"
files = os.listdir(logs_path)

for file in files:
    print(f"\n---------- RUTAS DE GRAFICOS {file} ----------")
    actionsPerUser.main(f"{logs_path}/{file}")
    usersPerTeam.main(f"{logs_path}/{file}")
    playersInTime.main(f"{logs_path}/{file}", float(os.getenv("USERS_INTERVAL")))
    teamsInTime.main(f"{logs_path}/{file}", float(os.getenv("TEAMS_INTERVAL")))
    scoreCurves.main(f"{logs_path}/{file}", float(os.getenv("SCORE_INTERVAL")))


print("\n")