## Explicacion
* Este codigo separa los logs verificando a que juego pertenecen y almacenandolos en `gameLogs`, luego se itera sobre cada archivo separado para graficar las estadisticas solicitadas, estas son almacenadas en la carpeta `graficosEstadisticos`.

## Ejecucion
- Ejecucion: `python main.py path_to_log intervalo_en_minutos`
    * path_to_log: Ruta hasta la ubicacion del log centralizado

## Componentes
* actionsPerUser.py: Se encarga de verificar las jugadas realizadas por cada usuario a lo largo del juego.
* usersPerTeam.py: Se encarga de verificar cuantos usuarios exisitieron por equipo en total en el juego.
* scoreCurves.py: Se encarga de verificar cuanto fue la puntuacion de los equipos a lo largo del juego segun el intervalo otorgado en las variables de entorno.
* teamsInTime.py: Se encarga de verificar cuantos equipos se crearon a lo largo de la partida segun el intervalo otorgado en las variables de entorno.
* playersInTime.py: Se encarga de verificar cuantos usuarios se crearon a lo largo de la partida segun el intervalo otorgado en las variables de entorno.

## Variables de entorno
* Se utilizo un archivo .env para almacenar las siguientes variables:

| Variable | Descripcion |
| -------- | ----------- |
| SCORE_INTERVAL | Intervalo de tiempo en minutos para componente de ``scoreCurves.py``  |
| TEAMS_INTERVAL | Intervalo de tiempo en minutos para componente de ``teamsInTime.py``  |
| USERS_INTERVAL | Intervalo de tiempo en minutos para componente de ``usersPerTeam.py`` |


