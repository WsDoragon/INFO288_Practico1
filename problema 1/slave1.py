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


#Conexion a BSD
load_dotenv('.envslave')
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
    )
print(mydb)
myCursor = mydb.cursor()


@app.route('/searchDocs')
def testDocs():
    tipo_doc = request.args.get('tipo_doc')
    print(os.getenv('DB_TABLE'))
    myCursor.execute(f'SELECT titulo, tipo, nodo FROM {os.getenv("DB_TABLE")}')
    docs = myCursor.fetchall()
    resultados = []
    for doc in docs:
        if doc[1] == tipo_doc:
            resultados.append({"titulo": doc[0], "tipo": doc[1], "nodo": doc[2]})
    return jsonify(resultados)
    
@app.route('/searchTitulo')
def testTitulo():
    titulo = request.args.get('titulo')
    titulo = unquote_plus(titulo)
    palabras = titulo.split(' ')
    myCursor.execute(f'SELECT titulo, tipo, nodo FROM {os.getenv("DB_TABLE")}')
    docs = myCursor.fetchall()
    resultados = []
    #print(palabras)    
    for doc in docs:
        for palabra in palabras:
            print(palabra)
            if palabra.lower() in doc[0].lower():
                print("ENTRE")
                resultados.append({"titulo": doc[0], "tipo": doc[1], "nodo": doc[2]})
                break
    return jsonify(resultados)

@app.route('/testDocs')
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

    
@app.route('/testTitulo')
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

@app.route('/insertDoc', methods=['POST'])
def insertDoc():
    documento = request.json
    base_de_datos.append(documento['titulo'])
    return jsonify({"mensaje": "Documento insertado correctamente"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  
