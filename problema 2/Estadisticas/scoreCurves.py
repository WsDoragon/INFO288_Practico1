import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


#Funcion para ordenar las entradas obtenidas anteriormente por timestamp
def sort_entries_by_timestamp(entries):
    return sorted(entries, key=lambda x: datetime.datetime.strptime(x.split('|')[0].strip(), '%Y-%m-%dT%H:%M:%S.%f'))

def get_log_entries_by_intervals(log_file, interval_minutes):
    # Leer el archivo de registro y obtener la primera hora
    with open(log_file, 'r') as file:
        log_entries = file.readlines()
        sorted_log = sort_entries_by_timestamp(log_entries)
        first_entry = sorted_log[0]
        game_number = first_entry.split('|')[2].strip()

    first_timestamp_str = first_entry.split('|')[0].strip()
    first_timestamp = datetime.datetime.strptime(first_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')

    # Función para calcular el intervalo de una entrada
    def calculate_interval(entry_time, start_time, interval):
        delta = entry_time - start_time
        return int(delta.total_seconds() // (interval * 60))

    # Agrupar las entradas de registro por intervalos de tiempo
    entries_by_interval = defaultdict(list)

    
    for entry in sorted_log:
        count = 0
        if "SEND_GAME_STATS" in entry and "Points" in entry:
            timestamp_str = entry.split('|')[0].strip()
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            interval = calculate_interval(timestamp, first_timestamp, interval_minutes)
            entries_by_interval[interval].append(entry)
            count += 1

    return entries_by_interval, game_number, first_timestamp



interval_minutes = 5  # Intervalo de tiempo en minutos
log_file = '../gameLog.txt'

entries_by_interval, game_num, first_timestamp = get_log_entries_by_intervals(log_file, interval_minutes)
print("entries_by_interval: ", entries_by_interval)
for interval, entries in entries_by_interval.items():
    print(f"Intervalo {interval}:")
    for entry in entries:
        print(entry)


def points_by_team(entries):
    
    points_by_interval_and_team = defaultdict(dict)

    for interval, entries_list in entries.items():
        for entry in entries_list:
            teams = entry.split('|')[7].strip().split('+')
            teams.pop()
            for team in teams:
                team_name, points = team.split('- Points ')
                team_name = team_name.strip().split(' ')[1]
                points = int(points)
                if team_name in points_by_interval_and_team[interval]:
                    points_by_interval_and_team[interval][team_name] += points
                else:
                    points_by_interval_and_team[interval][team_name] = points
    return points_by_interval_and_team

    ''' print("Points by interval and team:")
    for interval, teams in points_by_interval_and_team.items():
        print(f"Interval {interval}:")
        for team, points in teams.items():
            print(f"Team {team}: Points {points}")'''


def obtain_one_entry_per_interval(entries):
    # Obtener una entrada por intervalo
    one_entry_per_interval = defaultdict(list)
    for interval, entries_list in entries.items():
        one_entry_per_interval[interval].append(min(entries_list, key=lambda x: datetime.datetime.strptime(x.split('|')[0].strip(), '%Y-%m-%dT%H:%M:%S.%f')))
    return(one_entry_per_interval)

intervaled = obtain_one_entry_per_interval(entries_by_interval)

TheEnd = points_by_team(intervaled)
print("TheEnd: ", TheEnd)



# Obtener todos los intervalos existentes
all_intervals = set(TheEnd.keys())
print(TheEnd[min(all_intervals)].keys())
temp_zero_points = {}
if 0 not in all_intervals:
    for key in TheEnd[min(all_intervals)].keys():
        temp_zero_points[key] = 0
    TheEnd[0] = temp_zero_points

# Obtener todos los intervalos nuevos
all_intervals = set(TheEnd.keys())
# Encontrar el intervalo mínimo y máximo
min_interval = min(all_intervals)
max_interval = max(all_intervals)

# Crear un nuevo diccionario para almacenar los puntos por intervalo y equipo con los intervalos faltantes
filled_points_by_interval_and_team = {}

# Iterar sobre todos los intervalos desde el mínimo hasta el máximo
for interval in range(min_interval, max_interval + 1):
    # Si el intervalo existe en TheEnd, copiar los puntos por equipo
    if interval in TheEnd:
        filled_points_by_interval_and_team[interval] = TheEnd[interval]
    # Si el intervalo no existe en TheEnd, copiar los puntos del intervalo anterior
    else:
        filled_points_by_interval_and_team[interval] = filled_points_by_interval_and_team[interval - 1]

# Actualizar TheEnd con los intervalos faltantes
TheEnd = filled_points_by_interval_and_team

def plot_points_by_team(points_by_team):
    teams = list(points_by_team.values())[0].keys()
    intervals = list(points_by_team.keys())
    
    plt.figure(figsize=(12, 8))
    for team in teams:
        points = [points_by_team[interval][team] for interval in intervals]
        plt.plot(intervals, points, label=team)
    plt.xlabel('Interval')
    plt.ylabel('Points')
    plt.title(f'Puntos en intervalos de tiempo en {game_num}')  # Título del gráfico
    # Descripción de los intervalos
    interval_description = f"Intervalo de {interval_minutes} minutos\nInicio en {first_timestamp}"
    plt.figtext(0.5, 0.01, interval_description, wrap=True, horizontalalignment='center', fontsize=10)
    plt.legend()
    #plt.show()
    plt.savefig(f'./graficosEstadisticos/game_{game_num}_ScoreCurves.png')

plot_points_by_team(TheEnd)
