# Problema 1

### Descripción
 Se propuso crear una Biblioteca digital distribuida segun el tipo documento utilizando Python, esta solucion contempla el realizar diferentes consultas mediante la parametros en la url de la biblioteca

## Funciones

## Requisitos
* Es necesario estar en la carpeta `problema 1`
* Python 3.11
* MariaDB
* (Opcional) miniconda con ambiente llamado INFO288
    * Este metodo es opcional pero recomendado para mantener un ambiente limpio para la prueba de esta implementación, igualmente es requisito para utilizar el auto iniciador de Slaves.

```cmd
conda create -n INFO288 python=3.11
conda activate INFO288
```

## Instalación
* Instalacion de requirements.txt
    ```pip install -r requirements.txt```
* Importar Base de datos contenida en "ARCHIVO.sql"
    * Con este comando se ejecutara automaticamente la creacion de la base de datos.
```SQL
/*Utilizando la terminal de mariaDB utilizar el siguiente comando*/
/*Se debe cambiar "RUTA/HASTA/" con la ruta en donde se encuentra almacenado el archivo sql*/
SOURCE RUTA/HASTA/ARCHIVO.sql
```
#### Disclaimer: Se utilizo windows para ejecutar esta implementación

## Iniciar
Para realizar un inicio correcto de la aplicacion es necesario seguir los siguientes pasos.
1. Iniciar Nodo Maestro
```cmd
python master.py
```
2. Iniciar Nodo/s Esclavo/s, tenemos 2 opciones
    * Opción inicio automatico
    ```cmd
    python iniciador.py [nombre ambiente]
    Ej: python iniciador.py INFO288
    ```
    * Opcion manual: Esta se debe realizar por cada esclavo que se quiera levantar.

    ```cmd
    python slave.py ./slave_envs/.envslave[N°]
    Ej: python slave.py ./slave_envs/.envslave1
    ```

> * Esta ejecucion base cuenta con la opcion de levantar 4 esclavos, 
> * En caso de querer agregar más es necesario: 
>   * crear archivo `.envslave[N°]` conteniendo los datos de la seccion        `Enviroment`
>   * crear un registro inicial en la tabla `tipos` de la base de datos indicando:
>       * nombre = Tipo_Nodo
>       * nodoDestino = http://[ruta o ip nodo esclavo]:[Puerto]
>       * nodo = master (Nodo en el que se aloja el diccionario de tipos)
>   * Crear tabla a consultar DB_TABLE de slave

## Enviroment
* .envslave[N°]:
    * DB_NAME = "distribuidos1" [Nombre base de datos]
    * DB_HOST = "localhost" [Host de base de datos]
    * DB_USER = [Usuario de base de datos]
    * DB_PASS = [Contraseña de usuario]
    * DB_TABLE = [Nombre de la tabla]
    * NODO_MAESTRO = "localhost:5000" [Se indica URL a Nodo Maestro]
    * NODO_SLAVE = "localhost" [URL de Nodo Slave]
    * PORT = [Pueto que utilizara el Nodo Slave]
    * TIPO_NODO = [Tipo de documento que almacena el nodo]

* .envmaster:
    * DB_NAME = "distribuidos1" [Nombre base de datos]
    * DB_HOST = "localhost" [Host de base de datos]
    * DB_USER = [Usuario de base de datos]
    * DB_PASS = [Contraseña de usuario]


