import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import os

#argumentos de entrada


def main(path_to_log):
    #path_to_log = "../gameLog.txt"
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

    teamsUsers = {} #variable de usuarios en cada equipo "equipo":[usuarios]...
    for log in games_logs:
        if "TEAM_MANAGEMENT" in log and ("NICK" in log or "GET_INTO_TEAM" in log):
            splitted = log.split("|")
            ini = int(splitted[3].strip())
            end = int(splitted[4].strip())
            extraSplit = splitted[7].strip()
            if (ini == 1 and end == 0):
                #print("Inicio:", extraSplit)
                username = extraSplit.split(":")[1].strip()
            if (ini == 0 and end == 1):
                #print("Fin:", extraSplit)
                team = extraSplit.split(":")[1].strip()
                if team not in teamsUsers:
                    teamsUsers[team] = []
                teamsUsers[team].append(username)
    
    game = games_logs[0].split("|")[2].strip()
    teams = list(teamsUsers.keys())
    players_count = [len(users) for users in teamsUsers.values()]

    # Generar el gráfico de barras
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico
    plt.bar(teams, players_count, color='skyblue')  # Crea las barras
    plt.xlabel('Equipos')  # Etiqueta del eje X
    plt.ylabel('Cantidad de Jugadores')  # Etiqueta del eje Y
    plt.title(f'Cantidad de Jugadores por Equipo en {game}')  # Título del gráfico
    plt.xticks(rotation=45)  # Rota los nombres de los equipos para mejor lectura
    plt.savefig(f"./graficosEstadisticos/game_{game}_UsersPerTeam.png")
    #plt.show()  # Muestra el gráfico

    print("* Usuarios por equipo en el juego", game, " guardados en ./graficosEstadisticos/game_"+ game + "_UsersPerTeam.png")