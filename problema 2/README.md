# Problema 2
* Edit: en la seccion de `Prueba Practica 2` se encuentran actualizaciones
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
* ejemplo:
    ```CMD
    python3 server.py --env .envserver
    ``` 

### Correr client.py:
* python3 client.py --host "direccion ip servidor" --port "puerto destino" --nick "nombre del jugador"
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



# Prueba Practica 2
* Unicamente se mostraran actualizaciones en esta seccion.
* En la carpeta `Estadisticas` se encuentra el problema 2 de esta prueba practica junto a su ``README.md``

## Descripcion
Se propuso la implementacion de logs atraves de un servidor RMI, almacenando logs del servidor y el cliente en un log centralizado para realizar un analisis de este posteriormente.

## Requerimientos
* Librerias nuevas:
    *  Pyro4 (`pip install Pyro4`)

* Realizar la ejecucion de un nameserver pyro4 en la maquina que tendra el servidor RMI de logs
    ```bash
    #En consola windows
    > python -m Pyro4.naming --host [IP computador]

    #Para verificar las URI registradas
    > python -m Pyro4.nsc list --host [IP host nameserver]
    ```

## Ejecucion
### Correr logServer.py:
* Es necesaria la ejecucion de este en una terminal antes de iniciar el servidor y cliente del juego.
* Ejecucion:
    ```bash
    #Comando de ejecucion de servidor RMI
    python logServer.py
    ``` 

## Descripcion Logs almacenados

* Estructura de logs
    * timestamp | accion | Juego[N°] | Inicio | Fin | Jugador | Equipo | Espacio libre para más info |
    * Se utilizo `|` como separador de posiciones en el log

    | Posicion | Variable  | Descripcion |
    |----------| --------  | ----------- |
    | 0 | timestamp | Indica la hora a la que se genero el log |
    | 1 | accion    | Identificador de la accion ejecutada |
    | 2 | Juego[N°] | Identificador de Nombre de juego almacenado |
    | 3 | Inicio | Indica con "1" el inicio de la accion, si es 0 no es inicio |
    | 4 | Fin | Indica con "1" el Fin de la accion, si es 0 no es Fin |
    | 5 | Jugador | Nombre del jugador al que pertenece la accion, en caso del servidor se muestra la IP de este |
    | 6 | Equipo | Se muestra el equipo al que pertenece el jugador, en caso de no estar en un equipo es n/a|
    | 7 | Espacio libre | A partir de este punto se guarda informacion especial que requiera cada accion |


* Acciones de jugador:
    | Accion    | Descripcion |
    | --------- | ----------- |
    | INI_CONEX | Conexion inicial al servidor | 
    | GET_TEAM_DATA | Obtencion equipos existentes en el servidor |
    | SELECT_TEAM  | Escoger equipo en al cual unirse |
    | GAME_ACTIONS | Acciones que se realizan en el juego, utiliza el campo `Espacio Libre` para enviar mas informacion |

    * Informacion extra de GAME_ACTIONS

    | String    | Descripcion |
    | --------- | ----------- |
    | SEND_DICE: [N°] | Indica el inicio y fin de enviar un dado, se muestra el numero enviado |
    | GET_GAME_STATS | Indica la obtencion de estadisticas del servidor |
    | VOTE_MANAGEMENT | Indica el manejo de votaciones para aceptar usuario |
    | END_GAME | Indica el fin del juego |


* Acciones del Servidor

    | Accion    | Descripcion |
    | --------- | ----------- |
    | SERVER_START | Indica el inicio del servidor de juego |
    | PLAYER_REG | Indica la conexion de un usuario al servidor, Espacio extra con la variable NICK: [Nombre del jugador] |
    | SEND_TEAM_INFO | Indica que se esta enviando informacion de los equipos al nuevo usuario |
    | CREATE_NEW_TEAM | Indica la creacion de un equipo adicional a los 2 por defecto del servidor |
    | TEAM_MANAGEMENT | Relacionado al manejo de equipos, puede utilizar el espacio adicional con `GET_INTO_TEAM: [Equipo]` indicando el unirse de forma exitosa o `REJECT` indicando que no se pudo unir el jugador |
    | VOTE_MANAGEMENT | Manejo de los votos |
    | GAME_RUNNING | Indica el inicio  y el fin de una ronda, Utiliza espacio adicional indicando el ``TEAM`` que juega en la ronda y ``NPLAYERS`` con el numero de jugadores por el equipo jugando |
    | SEND_GAME_STATS | Indica el envio de estadisticas de juego utilizando espacio adicional para indicar puntos por equipo | Hace uso de espacio adicional para enviar estadisticas.
    | SEND_GAME_END | Envia el fin del juego a los jugadores |



## Enviroment
> Se han actualizado las variables de entorno utilizadas en el proyecto, a continuacion se mostraran cuales han sido agregadas unicamente, en la seccion anterior se pueden encontrar la totalidad.

* Variables `.envserver` nuevas

| Variable | Descripcion |
| -------- | ----------- |
| GAME_NUM | Indica el numero de juego, se aconseja tener este formato: `Juego_[N°]` |
| LOG_SERVER_IP | Direccion ip maquina que contiene el servidor RMI de logs y nameserver |
| LOG_SERVER_NAME | Nombre que se buscara en el nameserver de Pyro4 en la maquina del servidor RMI |

* Variables `.envLogs`

| Variable | Descripcion |
| -------- | ----------- |
| LOGNAME | Nombre del archivo en el cual se guardaran los logs del servidor y clientes |
| LOG_SERVER | Nombre que se utiliza en el nameserver el servidor RMI |
| LOG_SERVER_IP | IP sobre la cual correra nuestro servidor RMI |

* Variables `.envclient`

| Variable | Descripcion |
| -------- | ----------- |
| LOG_SERVER_IP | Direccion ip maquina que contiene el servidor RMI de logs y nameserver |
| LOG_SERVER_NAME | Nombre que se buscara en el nameserver de Pyro4 en la maquina del servidor RMI |

## Consideraciones Generales
* La maquina host del servidor RMI puede necesitar que la red este configurada como privada en caso de trabajar en windows.
* Es completamente necesario que el nameserver de Pyro4 se encuentre en ejecucion mientras se ejecuta todo.
* Durante las pruebas se pudo observar un fenomeno en el cual en ocasiones el logserver agregaba los datos cortados al archivo de logs.