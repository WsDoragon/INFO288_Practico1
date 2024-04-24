#definir funciones


def registered(ip, puerto, lista):
    for x in lista:
        if(ip == x.ip and puerto == x.port):
            return True
        
    return False



# registro de par (ip,port)