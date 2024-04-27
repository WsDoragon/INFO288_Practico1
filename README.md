# INFO288-Practico1

## Consideraciones:
| Problema 1
| ---------- |
* Se necesita insertar documento y busqueda
* Programar el master y el slave
* Particion por tipo de documento (Tesis - General - Video - Papers)
* Interesante: Esclavo que lo posee - Hora y fecha
* 2 tablas por bsd: Documentos (Local) y Tipo de documentos (Deberia estar en todas este)
----------------
* Podemos generar en la misma BSD 4 tablas (Documento1 , ...2 , ...3 , ...4)
* columna de quien ingreso la informacion

----------------
| Problema 2 |
| ---------- |
* Puntuaciones manejadas por servidor o Cliente, vale de ambas formas
* Es asincrona, se pueden inscribir equipos en cualquier momento.

* Requerimientos:
    * python 3.10+
    * librerias:
            * socket
            * json
            * queue
            * random
            * time
            * threading
            * argparse
            * os
* Correr server.py:
    * python3 server.py --host "direccion ip maquina " --port "puerto a usar"
        * ejemplo: python3 server.py --host 192.168.1.26 --port 20002 
* Correr client.py:
    * python3 client.py --host "direccion ip servidor" --port "puerto destino" --nick "nombre del jugador"
        * ejemplo: python3 client.py --host 192.168.1.26 --port 20002 --nick Leoxz98

* Consideraciones generales:
    * No hay manejo de excepciones (ingresar y operacion lo que se pide exactamente)
    * puede hacer un poco de delay, solo esperar
    * cuando alguien se une, le toca jugar en la siguiente ronda, si es que hay
    * cuando alguien es rechazo tiene que volver a elegir equipo