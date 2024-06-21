import json
import os
import matplotlib.pyplot as plt


# Abre el archivo en modo lectura
archivo = open("../gameLog.txt", "r")

# Lee el contenido del archivo
contenido = archivo.read()
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
        #print(games_logs)
        games_logs[actual_game].append(linea)


# Cierra el archivo
archivo.close()

# Recorrer games_logs y guardar en un archivo txt cada juego
for game in games_logs:
    archivo = open(f"./gameLogs/game_{game}.txt", "w")
    for log in games_logs[game]:
        archivo.write(log + "\n")
    archivo.close()


# Cantidad de usuarios por equipo durante el juego
gamesUsers = {} #Division equipos por juego
for game in games_logs:
    teamsUsers = {} #variable de usuarios en cada equipo "equipo":[usuarios]...
    for log in games_logs[game]:
        if "TEAM_MANAGEMENT" in log and ("NICK" in log or "GET_INTO_TEAM" in log):
            splitted = log.split("|")
            ini = int(splitted[3].strip())
            end = int(splitted[4].strip())
            extraSplit = splitted[7].strip()
            if (ini == 1 and end == 0):
                print("Inicio:", extraSplit)
                username = extraSplit.split(":")[1].strip()
            if (ini == 0 and end == 1):
                print("Fin:", extraSplit)
                team = extraSplit.split(":")[1].strip()
                if team not in teamsUsers:
                    teamsUsers[team] = []
                teamsUsers[team].append(username)
    gamesUsers[game] = teamsUsers
    
print("Games Users: ", gamesUsers)
# print de usuarios de cada equipo por juego
for game in gamesUsers:
    print(f"Juego {game}:")
    for team in gamesUsers[game]:
        print(f"Equipo {team}: {len(gamesUsers[game][team])}")


# Para cada juego, generar un gráfico de barras mostrando usuarios por equipo
for game, teamsUsers in gamesUsers.items():
    teams = list(teamsUsers.keys())
    players_count = [len(users) for users in teamsUsers.values()]

    # Generar el gráfico de barras
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico
    plt.bar(teams, players_count, color='skyblue')  # Crea las barras
    plt.xlabel('Equipos')  # Etiqueta del eje X
    plt.ylabel('Cantidad de Jugadores')  # Etiqueta del eje Y
    plt.title(f'Cantidad de Jugadores por Equipo en {game}')  # Título del gráfico
    plt.xticks(rotation=45)  # Rota los nombres de los equipos para mejor lectura
    #plt.show()  # Muestra el gráfico
    plt.savefig(f"./graficosEstadisticos/game_{game}_UsersPerTeam.png")


# Acciones de cada usuario por partida
gamesActions = {} #Division acciones por juego
for game in games_logs:
    usersActions = {} #variable de acciones por usuario "usuario":[acciones]...
    for log in games_logs[game]:
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
    gamesActions[game] = usersActions

print("Games Actions: ", gamesActions)

# Para cada juego y cada usuario, generar un gráfico de barras mostrando cantidad de acciones
for game, usersActions in gamesActions.items():
    users = list(usersActions.keys())
    print("users: ", users)
    actions_count = [len(actions) for actions in usersActions.values()]
    print("actions_count: ", actions_count)

    # Generar el gráfico de barras
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico
    plt.bar(users, actions_count, color='skyblue')  # Crea las barras
    plt.xlabel('Usuarios')  # Etiqueta del eje X
    plt.ylabel('Cantidad de Acciones')  # Etiqueta del eje Y
    plt.title(f'Cantidad de Acciones por Usuario en {game}')  # Título del gráfico
    plt.xticks(rotation=45)  # Rota los nombres de los usuarios para mejor lectura
    #plt.show()  # Muestra el gráfico
    plt.savefig(f"./graficosEstadisticos/game_{game}_ActionsPerUser.png")




from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Suponiendo que el formato de timestamp es 'YYYY-MM-DD HH:MM:SS'
timestamp_format = '%Y-%m-%dT%H:%M:%S'
window_size_minutes = 4  # Ventana de tiempo en minutos

for game, teamsUsers in gamesUsers.items():
    teams = list(teamsUsers.keys())
    scores = {team: [] for team in teams}
    for log in games_logs[game]:
        if "SEND_GAME_STATS" in log and "Points" in log:
            splitted = log.split("|")
            timestamp = datetime.strptime(splitted[0].strip().split(".")[0], timestamp_format)
            team_scores = splitted[7].strip().split("+")
            team_scores.pop()  # eliminar último elemento
            for team_score in team_scores:
                team, score = team_score.split("- Points ")
                scores[team.strip().split(" ")[1]].append((timestamp, int(score.strip())))
    
    # Convertir las puntuaciones en series de tiempo agrupadas por ventana de tiempo
    for team in teams:
        scores[team].sort(key=lambda x: x[0])  # Ordenar por timestamp
        grouped_scores = {}
        start_time = scores[team][0][0] if scores[team] else None
        for timestamp, score in scores[team]:
            if start_time:
                time_diff = (timestamp - start_time).total_seconds() / 60  # Diferencia en minutos
                window = int(time_diff // window_size_minutes)
                if window not in grouped_scores:
                    grouped_scores[window] = 0
                grouped_scores[window] += score
        
        # Preparar datos para el gráfico
        windows = sorted(grouped_scores.keys())
        points = [grouped_scores[window] for window in windows]
        # Convertir ventanas a marcas de tiempo reales para etiquetas
        timestamps = [start_time + timedelta(minutes=window * window_size_minutes) for window in windows]
        
        # Graficar
        plt.plot(str(timestamps), points, label=team)

    plt.xlabel('Tiempo')
    plt.ylabel('Puntuación')
    plt.title(f'Curvas de Puntuación por Equipo en {game}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig(f"./graficosEstadisticos/game_{game}_ScoreCurves.png")