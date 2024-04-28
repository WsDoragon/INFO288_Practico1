from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import unquote_plus
import sys
import requests

app = Flask(__name__)

args = sys.argv
if len(args) < 2:
    print("Porfavor ingrese posicion .env\nEjemplo: python slave1.py ./slave_envs/.envslave1")
    sys.exit(1)
print("Arguments:", args)

#Conexion a BSD
load_dotenv(args[1])
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
    myCursor.execute(f'SELECT titulo, tipo, nodo, autor FROM {os.getenv("DB_TABLE")}')
    docs = myCursor.fetchall()
    resultados = []
    
    for doc in docs:
        for palabra in palabras:
            if palabra.lower() in doc[0].lower():
                resultados.append({"titulo": doc[0], "tipo": doc[1], "nodo": doc[2], "autor": doc[3]})
                break
    return jsonify(resultados)

@app.route('/insertDoc', methods=['POST'])
def insertDoc():
    documento = request.json
    print(documento)
    titulo = documento['titulo']
    tipo = documento['tipo_doc']
    autor = documento['autor']
    nodo = "slave"+os.getenv('TIPO_NODO').capitalize()
    myCursor.execute(f'INSERT INTO {os.getenv("DB_TABLE")} (titulo, tipo, autor, nodo) VALUES (%s, %s, %s, %s)', (titulo, tipo, autor, nodo))
    mydb.commit()
    return jsonify({"status": "ok"})

    

if __name__ == '__main__':
    response = requests.post('http://' + os.getenv("NODO_MAESTRO") + '/registrarNodo', params={'url': os.getenv('NODO_SLAVE'), 'port': os.getenv('PORT'), 'tipo_nodo': os.getenv('TIPO_NODO')})
    print(response.json())    
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
