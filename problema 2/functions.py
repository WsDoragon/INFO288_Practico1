#definir funciones


def has_conex(ip, puerto, lista_clientes):
    for cliente in lista_clientes:
        if cliente.ip == ip and cliente.puerto == puerto:
            return True  # Se encontró un cliente con la misma IP y puerto
    return False  # No se encontró ningún cliente con la misma IP y puerto

def verificar_equipos(lista_equipos):
    count = 0
    for equipo in lista_equipos:
        if len(equipo.players) > 0:
            count += 1
            if count == 2:
                return True
    return False