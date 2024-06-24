## Explicacion
* Este codigo separa los logs verificando a que juego pertenecen y almacenandolos en `gameLogs`, luego se itera sobre cada archivo separado para graficar las estadisticas solicitadas, estas son almacenadas en la carpeta `graficosEstadisticos`.

## Ejecucion
- Ejecucion: `python main.py path_to_log`
    * path_to_log: Ruta hasta la ubicacion del log centralizado

## Componentes
* main.py: Ejecuta cada uno de los componentes inferiores y genera archivos de logs por cada juego existente
    * Archivo generado: ``game_[N° Juego].txt``
* actionsPerUser.py: Se encarga de verificar las jugadas realizadas por cada usuario a lo largo del juego.
    * Archivo generado: `game_[N° Juego revisado]_ActionsPerUser.png`
* usersPerTeam.py: Se encarga de verificar cuantos usuarios exisitieron por equipo en total en el juego.
    * Archivo generado: `game_[N° Juego revisado]_UsersPerTeam.png`
* scoreCurves.py: Se encarga de verificar cuanto fue la puntuacion de los equipos a lo largo del juego segun el intervalo otorgado en las variables de entorno.
    * Archivo generado: `game_[N° Juego revisado]_ScoreCurves.png`
* teamsInTime.py: Se encarga de verificar cuantos equipos se crearon a lo largo de la partida segun el intervalo otorgado en las variables de entorno.
    * Archivo generado: `game_[N° Juego revisado]_TeamsPerInterval.png`
* playersInTime.py: Se encarga de verificar cuantos usuarios se crearon a lo largo de la partida segun el intervalo otorgado en las variables de entorno.
    * Archivo generado: `game_[N° Juego revisado]_PlayersPerInterval.png`

## Variables de entorno
* Se utilizo un archivo .env para almacenar las siguientes variables:

| Variable | Descripcion |
| -------- | ----------- |
| SCORE_INTERVAL | Intervalo de tiempo en minutos para componente de ``scoreCurves.py``  |
| TEAMS_INTERVAL | Intervalo de tiempo en minutos para componente de ``teamsInTime.py``  |
| USERS_INTERVAL | Intervalo de tiempo en minutos para componente de ``usersPerTeam.py`` |

## Consideraciones
* Al momento de ejecutar main.py si existen .txt en la carpeta de gameLogs igual seran analizados, en caso de que no contengan la estructura de la informacion utilizada este programa terminara en error.
