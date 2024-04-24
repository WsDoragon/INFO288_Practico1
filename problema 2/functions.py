#definir funciones


def registered(ip, puerto, lista):
    for x in lista:
        if(ip == x.ip and puerto == x.port):
            return True
        
    return False


def verificar_equipos(lista_equipos):
    count = 0
    for equipo in lista_equipos:
        if len(equipo.players) > 0:
            count += 1
            if count == 2:
                return True
    return False