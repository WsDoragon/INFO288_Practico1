# Problema 2

## Descripcion
Se propuso la creacion de un juego en el que 2 o mas equipos compiten para ver quien alcanza antes la puntuacion objetivo lanzando dados.

## Funcionamiento
* Implementacion cliente - servidor mediante UDP
* Asincrono, se pueden inscribir equipos en cualquier momento

## Requerimientos:
* Python 3.10+
* Librerias utilizadas:
    * socket
    * json
    * queue
    * random
    * time
    * threading
    * argparse
    * os
    * python-dotenv (``pip install python-dotenv``)

## Ejecucion
### Correr server.py:
* python3 server.py --env "Nombre archivo .env"
* ejemplo: python3 server.py --env .envserver

### Correr client.py:
* ``python3 client.py --host "direccion ip servidor" --port "puerto destino" --nick "nombre del jugador"``
* Ejemplo:
    ```CMD
    python3 client.py --host 192.168.1.26 --port 20002 --nick Leoxz98
    ```

## Enviroment
Se utilizan variables de entorno para configurar el servidor.
| Variable | Descripcion |
| -------- | ----------- |
| HOST | Direccion ip maquina |
| PORT | Puerto sobre el que escuchara la maquina |
| MAX_POINTS | Limite de puntuacion que tendra la partida |
| MAX_TEAMS | Limite de equipos que se podran crear en la partida, minimo 2 |
| MAX_PER_TEAM | Limite de jugadores por equipo |
| MAX_DICE | Dado que el servidor define para los jugadores |

## Consideraciones generales:
* No hay manejo de excepciones (ingresar y realizar operacion segun lo que se pide exactamente)
* puede existir un poco de delay, es necesario esperar
* cuando alguien se une, le toca jugar en la siguiente ronda, si es que hay
* cuando alguien es rechazo tiene que volver a elegir equipo