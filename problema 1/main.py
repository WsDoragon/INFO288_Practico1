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
mycursor.execute("SELECT * FROM tipos")
tipos = mycursor.fetchall()
#print (tipos)
    

@app.route('/query')
def query():
    tipo_doc = request.args.get('tipo_doc').lower()
    titulo = request.args.get('titulo')
    print(tipo_doc, titulo)
    if tipo_doc:
        esclavos = [esclavos_por_tipo[doc] for doc in tipo_doc.split('+')]
    else:
        # Si no se proporciona tipo_doc, enviar la consulta a todos los esclavos
        esclavos = list(esclavos_por_tipo.values())

    resultados = []

    for esclavo_url in esclavos:
        # Realizar la consulta a cada esclavo
        response = requests.get(esclavo_url + '/searchDocs', params={'tipo_doc': tipo_doc})
        if response.status_code == 200:
            # Agregar los resultados de este esclavo a la lista total de resultados
            resultados.extend(response.json())

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
