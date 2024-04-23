from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import unquote_plus

app = Flask(__name__)

# Base de datos simulada para este esclavo
base_de_datos =  [
    "Tesis sobre...", 
    "Otra tesis...", 
    "Cambios Fasicos",
    "Fisica Cuantica", 
    "Cuantica de los fluidos"
    ]

# Load environment variables from .envslave file
load_dotenv('.envslave')
#Conectar a la base de datos
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
    )
print(mydb)



@app.route('/searchDocs')
def search():
    tipo_doc = request.args.get('tipo_doc')
    resultados = []
    for documento in base_de_datos:
        resultados.append(
            {"titulo": documento, 
             "nodo": "Slave Tesis", 
             "tipo": tipo_doc})

    #resultados = [documento for documento in base_de_datos]
    return jsonify(resultados)

    
@app.route('/searchTitulo')
def searchTitle():
    titulo = request.args.get('titulo')
    palabras = titulo.split(' ')
    for i in palabras: print(i)
    resultados = []
    #Busqueda en la base de datos mediante el titulo
    for documento in base_de_datos:
        for palabra in palabras:
     #       print(palabra)
            if palabra.lower() in documento.lower():
                resultados.append(
                    {"titulo": documento, 
                    "nodo": "Slave Tesis", 
                    "tipo": "tesis"})
                break 
            
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Cambia el puerto para cada esclavo
