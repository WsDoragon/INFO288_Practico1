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

correr server: python3 server.py
correr cliente python3 client.py ip port