import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import os


def main(path_to_log):
    #path_to_log = ".\gameLogs\game_Juego_1.txt"
    #abrir archivo
    archive = open(path_to_log, "r")
    # Lee el contenido del archivo
    archive_content = archive.read()
    # Divide el contenido en líneas
    archive_lines = archive_content.split("\n")
    games_logs = []
    # Itera sobre cada línea
    for line in archive_lines:
        # Divide la línea en partes usando el separador "|"
        partes = line.split("|")
        if len(partes) > 2:
            games_logs.append(line)

    usersActions = {} #variable de acciones por usuario "usuario":[acciones]...
    for log in games_logs:
        if "GAME_ACTIONS" in log and "SEND_DICE" in log:
            splitted = log.split("|")
            ini = int(splitted[3].strip())
            end = int(splitted[4].strip())
            player = splitted[5].strip()
            action = splitted[7].strip()
            if player not in usersActions:
                usersActions[player] = []
            #if (ini == 1 and end == 0):
                #print("Inicio:", action)
            if (ini == 0 and end == 1):
                #print("Fin:", action)
                usersActions[player].append(action)

    game = games_logs[0].split("|")[2].strip()
    players = list(usersActions.keys())
    actions_count = [len(actions) for actions in usersActions.values()]

    # Generar el gráfico de barras
    plt.figure(figsize=(12, 8))  # Ajusta el tamaño del gráfico
    plt.bar(players, actions_count, color='skyblue')  # Crea las barras
    plt.xlabel('Usuarios')  # Etiqueta del eje X
    plt.ylabel('Cantidad de Acciones')  # Etiqueta del eje Y
    plt.title(f'Cantidad de Acciones por Usuario en {game}')  # Título del gráfico
    plt.xticks(rotation=45)  # Rota los nombres de los usuarios para mejor lectura
    plt.savefig(f"./graficosEstadisticos/game_{game}_ActionsPerUser.png")
    #plt.show()  # Muestra el gráfico
    
    print("\n* Acciones por usuario en el juego", game, "guardados en ./graficosEstadisticos/game_"+ game + "_ActionsPerUser.png")
