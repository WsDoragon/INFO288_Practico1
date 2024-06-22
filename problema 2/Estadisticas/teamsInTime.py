import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

def sort_entries_by_timestamp(entries):
    return sorted(entries, key=lambda x: datetime.datetime.strptime(x.split('|')[0].strip(), '%Y-%m-%dT%H:%M:%S.%f'))

def get_log_entries_by_intervals(log_file, interval_minutes):
    # Leer el archivo de registro y obtener la primera hora
    with open(log_file, 'r') as file:
        log_entries = file.readlines()
        sorted_log = sort_entries_by_timestamp(log_entries)
        first_entry = sorted_log[0]
        last_entry = sorted_log[-1]
        game_number = first_entry.split('|')[2].strip()

    first_timestamp_str = first_entry.split('|')[0].strip()
    first_timestamp = datetime.datetime.strptime(first_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')

    last_timestamp_str = last_entry.split('|')[0].strip()
    last_timestamp = datetime.datetime.strptime(last_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')

    # Función para calcular el intervalo de una entrada
    def calculate_interval(entry_time, start_time, interval):
        delta = entry_time - start_time
        return int(delta.total_seconds() // (interval * 60))

    # Agrupar las entradas de registro por intervalos de tiempo
    entries_by_interval = defaultdict(list)

    
    for entry in sorted_log:
        count = 0
        ini = entry.split('|')[3].strip()
        end = entry.split('|')[4].strip()
        if "CREATE_NEW_TEAM" in entry and end == "1":
            timestamp_str = entry.split('|')[0].strip()
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            interval = calculate_interval(timestamp, first_timestamp, interval_minutes)
            entries_by_interval[interval].append(entry)
            count += 1

    return entries_by_interval, game_number, first_timestamp, last_timestamp


def left_intervals_detect(entries_by_interval, first_timestamp, last_timestamp, interval_minutes):
    left_intervals = {}
    interval = 0
    while first_timestamp + datetime.timedelta(minutes=interval * interval_minutes) < last_timestamp:
        if interval not in entries_by_interval:
            left_intervals[interval] = []
        interval += 1
    return left_intervals


def main(path_to_log, set_interval):
    interval_minutes = set_interval  # Intervalo de tiempo en minutos
    log_file = path_to_log

    entries_by_interval, game_num, first_timestamp, last_timestamp = get_log_entries_by_intervals(log_file, interval_minutes)
    #print("entries_by_interval: ", entries_by_interval)
    #print("first_timestamp: ", first_timestamp)
    #print("last_timestamp: ", last_timestamp)

    left_intervals = left_intervals_detect(entries_by_interval, first_timestamp, last_timestamp, interval_minutes)
    #print("intervalos sin datos: ", left_intervals)
    entries_by_interval.update(left_intervals)

    teams_per_interval = defaultdict(int)
    for interval, entries in entries_by_interval.items():
        counter = 0
        counter = len(entries)
        #print(f"Intervalo {interval}: {counter} usuarios")
        teams_per_interval[interval] = (counter)

    teams_per_interval[0] = teams_per_interval[0] + 2 #Se agregan los 2 iniciales del servidor
    teams_per_interval = dict(sorted(teams_per_interval.items()))
    #print("teams_per_interval: ", teams_per_interval)

    # Generar el gráfico de barras de equipos por intervalo
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico
    plt.bar(teams_per_interval.keys(), teams_per_interval.values(), color='skyblue')  # Crea las barras
    plt.xlabel('Intervalo')  # Etiqueta del eje X
    plt.xticks(list(teams_per_interval.keys()))
    plt.ylabel('Cantidad de Equipos')  # Etiqueta del eje Y
    plt.title(f'Cantidad de Equipos por Intervalo en {game_num}')  # Título del gráfico
    plt.xticks(rotation=45)  # Rota los nombres de los intervalos para mejor lectura
    plt.savefig(f"./graficosEstadisticos/game_{game_num}_TeamsPerInterval.png")
    #plt.show()  # Muestra el gráfico

    print("* Equipos por intervalo en el juego'", game_num, "'guardados en ./graficosEstadisticos/game_"+ game_num + "_TeamsPerInterval.png")
