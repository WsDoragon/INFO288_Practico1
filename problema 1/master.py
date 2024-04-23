from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__)

# Diccionario que mapea tipos de documento a los esclavos correspondientes
esclavos_por_tipo = {
    "tesis": "http://localhost:5001",
    "libro": "http://localhost:5002",
    "video": "http://localhost:5003",

}
#Carga env master
load_dotenv('.envmaster')

#Conectar a la base de datos
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
    )
print(mydb)
    
mycursor = mydb.cursor()
#mycursor.execute("SELECT * FROM tipos")
#tipos = mycursor.fetchall()
#print (tipos)
@app.route('/')
def index():
    return "Hola mundo"
@app.route('/registrarNodo', methods=['POST'])
def registrarNodo():
    print("Registrando nodo", request.args.get('url'), request.args.get('port'))
    return jsonify({"status": "ok"})

@app.route('/query')
def test():
    tipo_doc = request.args.get('tipo_doc')
    titulo = request.args.get('titulo')
    print(titulo)
    if tipo_doc:
        mycursor.execute("SELECT nombre, nodoDestino FROM tipos WHERE nombre = %s", (tipo_doc.lower(),))
        esclavoTipo = mycursor.fetchone()
        print(esclavoTipo)
        if esclavoTipo:
            esclavo = esclavoTipo[1]
            response = requests.get(esclavo + '/searchDocs', params={'tipo_doc': tipo_doc.lower()})
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({"Error": 'Error en la consulta'})
        else:
            return jsonify({"Error": 'Tipo de documento no encontrado'})
        
    elif titulo:
        mycursor.execute("SELECT nombre, nodoDestino FROM tipos")
        esclavos = mycursor.fetchall()
        resultados = []
        for esclavo in esclavos:
            print(esclavo)
            response = requests.get(esclavo[1] + '/searchTitulo', params={'titulo': titulo})
            if response.status_code == 200:
                resultados.extend(response.json())
        return jsonify(resultados)
    else:
        return jsonify({"Error": 'No se especifico operacion'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
