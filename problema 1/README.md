# Problema 1

## Descripción
 Se propuso crear una Biblioteca digital distribuida segun el tipo documento utilizando Python, esta solucion contempla el realizar diferentes consultas mediante la parametros en la url de la biblioteca.

## Framework
* Flask: 
    * Flask es un framework web ligero y flexible para Python que proporciona herramientas y bibliotecas para construir aplicaciones web rápidas y escalables. Se utiliza en este proyecto para manejar las rutas, vistas y la lógica de la aplicación.

## Funciones
Esta implementacion de Biblioteca Distribuida cuenta con las siguientes funciones:
* Obtener datos de los diferentes nodos, de forma especifica o en modo broadcast.
* Realizar una actualizacion de la url y puerto del nodo destino que posee un tipo de documento especifico, esto mediante una peticion desde un nodo esclavo al nodo maestro.
    *  Metodo: POST | ``http://localhost:5000/registrarNodo`` 

    | Variable  | Descripcion |
    | --------  | ----------- |
    | url       | URL del nodo esclavo |
    | port      | Puerto sobre el cual se ejecuta el nodo |
    | tipo_nodo | Tipo de documento que almacena el nodo |

    * Este proceso es automatico de cada slave, lo unico necesario es tener en la base de datos un registro previo del tipo de documento que se quiere agregar e igualmente una base de datos / tabla especifica para el nodo.

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

## Uso de Aplicación
Este sistema esta diseñado para ser utilizado mediante un navegador web o consultas mediante software parecido a Postman
* Metodo: POST | ``http://localhost:5000/insert`` 
    * Se utiliza para insertar un elemento nuevo en un nodo existente.
    * Datos Necesarios:
        | Variable | Descripcion | 
        | -------- | ----------- |
        | titulo   | Nombre / titulo del documento subido |
        | tipo_doc | Nombre del tipo de documento |
        | autor    | Nombre del autor o quien sube el archivo |

* Metodo: GET | ``http://localhost:5000/query?titulo=[Terminos a buscar]``
    * Mediante esta url se realiza una busqueda de los documentos que tengan un titulo conteniendo alguna de las palabras entregadas en la url en todos los nodos que maneja la biblioteca distribuida, posteriormente se entregan todos estos.
    * Ejemplo de uso: `http://localhost:5000/query?titulo=fisica+cuantica`

* Metodo: GET | ``http://localhost:5000/query?tipo_doc=[tipo de documento a buscar]``
    * Mediante esta url se realiza una peticion para consultar a nodos especificos, obteniendo como resultado los elementos manejados por cada uno de esos nodos y entregandolo al usuario.
    * Ejemplo de uso: `http://localhost:5000/query?tipo_doc=tesis+general+audio`


