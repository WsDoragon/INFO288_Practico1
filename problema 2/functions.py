# Funciones
import os

def has_conex(ip, puerto, lista_clientes):
    for cliente in lista_clientes:
        if cliente.ip == ip and cliente.port == puerto:
            return True  # Se encontró un cliente con la misma IP y puerto
    return False  # No se encontró ningún cliente con la misma IP y puerto

def get_index(ip, puerto, lista_clientes):
    for indice, cliente in enumerate(lista_clientes):
        if cliente.ip == ip and cliente.port == puerto:
            return indice  # Se encontró un cliente con la misma IP y puerto, retorna su índice
    return -1  # No se encontró ningún cliente con la misma IP y puerto, retorna -1

def verificar_equipos(lista_equipos): #Verifica condicion para iniciar partido
    count = 0
    for equipo in lista_equipos:
        if len(equipo.players) > 0:
            count += 1
            if count == 2:
                return True
    
    return False

def clear_terminal():
    # Verificar el sistema operativo para determinar el comando de limpieza
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Posix (Linux, macOS, Unix)
        os.system('clear')

