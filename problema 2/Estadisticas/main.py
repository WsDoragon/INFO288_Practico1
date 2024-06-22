import os
import sys
import matplotlib.pyplot as plt

import actionsPerUser
import usersPerTeam
import playersInTime
import teamsInTime
import scoreCurves

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

# solicitar args de ejecucion "python main.py path_to_log"
if len(sys.argv) != 3 or not os.path.exists(sys.argv[1]) or not float(sys.argv[2]).is_integer:
    print("Error: Problema en la ejecucion de argumentos\nEjecucion: python main.py path_to_log intervalo_en_minutos\nEjemplo: python main.py ../gameLog.txt 5\n\n")
    sys.exit()

print(f"Archivo de log: {sys.argv[1]} | {sys.argv[2]}")

path_to_log = sys.argv[1]
interval = float(sys.argv[2])
divide_centra_log(path_to_log)



# leer todos los archivos de gameLogs
logs_path = "./gameLogs"
files = os.listdir(logs_path)

#print("Archivos de logs: ", files)

for file in files:

    print(f"\n---------- RUTAS DE GRAFICOS {file} ----------")
    actionsPerUser.main(f"{logs_path}/{file}")
    usersPerTeam.main(f"{logs_path}/{file}")
    playersInTime.main(f"{logs_path}/{file}", interval)
    teamsInTime.main(f"{logs_path}/{file}", interval)
    scoreCurves.main(f"{logs_path}/{file}", interval)


