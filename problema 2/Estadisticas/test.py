import datetime
from collections import defaultdict

def get_log_entries_by_intervals(log_file, interval_minutes):
    # Leer el archivo de registro y obtener la primera hora
    with open(log_file, 'r') as file:
        first_entry = file.readline()
        log_entries = file.readlines()
        log_entries.insert(0, first_entry)  # Reinsertar la primera entrada para incluirla en el análisis

    first_timestamp_str = first_entry.split('|')[0].strip()
    first_timestamp = datetime.datetime.strptime(first_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')

    # Función para calcular el intervalo de una entrada
    def calculate_interval(entry_time, start_time, interval):
        delta = entry_time - start_time
        return int(delta.total_seconds() // (interval * 60))

    # Agrupar las entradas de registro por intervalos de tiempo
    entries_by_interval = defaultdict(list)
    lastGoodEntry = ""
    for entry in log_entries:
        count = 0
        if "SEND_GAME_STATS" in entry and "Points" in entry:
            timestamp_str = entry.split('|')[0].strip()
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            interval = calculate_interval(timestamp, first_timestamp, interval_minutes)
            entries_by_interval[interval].append(entry)
            lastGoodEntry = entry
            count += 1
        if count == 0:
            timestamp_str = entry.split('|')[0].strip()
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            interval = calculate_interval(timestamp, first_timestamp, interval_minutes)
            if len(entries_by_interval[interval]) == 0:
                entries_by_interval[interval].append(lastGoodEntry)

    return entries_by_interval

# Ejemplo de uso
interval_minutes = 0.5  # Intervalo de tiempo en minutos
log_file = '../gameLog.txt'  # Reemplaza con la ruta a tu archivo de registro

entries_by_interval = get_log_entries_by_intervals(log_file, interval_minutes)
print("entries_by_interval: ", entries_by_interval)
for interval, entries in entries_by_interval.items():
    print(f"Intervalo {interval}:")
    for entry in entries:
        print(entry)