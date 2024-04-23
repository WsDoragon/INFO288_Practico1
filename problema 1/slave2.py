from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from urllib.parse import unquote_plus

app = Flask(__name__)

# Base de datos simulada para este esclavo
base_de_datos =  [
    "Tesis sobre...2", 
    "Otra tesis...2", 
    "Cambios Fasicos2",
    "Fisica Cuantica2", 
    "Cuantica de los fluidos2"
    ]
    


# Load environment variables from .envslave file
load_dotenv('.envslave')

bsd = os.environ.get('nombre')


@app.route('/searchDocs')
def search():
    tipo_doc = request.args.get('tipo_doc')
    resultados = []
    for documento in base_de_datos:
        resultados.append(
            {"titulo": documento, 
             "nodo": f"Slave {tipo_doc}", 
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
                    "nodo": "Slave General", 
                    "tipo": "tesis"})
                break 
            
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Cambia el puerto para cada esclavo
