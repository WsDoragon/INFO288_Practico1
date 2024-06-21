import datetime
from collections import defaultdict

#Funcion para ordenar las entradas obtenidas anteriormente por timestamp
def sort_entries_by_timestamp(entries):
    return sorted(entries, key=lambda x: datetime.datetime.strptime(x.split('|')[0].strip(), '%Y-%m-%dT%H:%M:%S.%f'))

def get_log_entries_by_intervals(log_file, interval_minutes):
    # Leer el archivo de registro y obtener la primera hora
    with open(log_file, 'r') as file:
        log_entries = file.readlines()
        sorted_log = sort_entries_by_timestamp(log_entries)
        first_entry = sorted_log[0]

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

    return entries_by_interval



interval_minutes = 0.5  # Intervalo de tiempo en minutos
log_file = '../gameLog.txt'

entries_by_interval = get_log_entries_by_intervals(log_file, interval_minutes)
print("entries_by_interval: ", entries_by_interval)
for interval, entries in entries_by_interval.items():
    print(f"Intervalo {interval}:")
    for entry in entries:
        print(entry)


def points_by_team(entries):
    for interval, entries_list in entries.items():
        for entry in entries_list:
            #print("entry: ", entry)
            teams = entry.split('|')[7].strip().split('+')
            teams.pop()
            for team in teams:
                #print("team: ", team)
                team_name, points = team.split('- Points ')
                print(f"Intervalo {interval}: Equipo {team_name.strip()[-1]} - Puntos: {points}")

points_by_team(entries_by_interval)