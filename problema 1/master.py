from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__)

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
    return "Hola mundo!"

@app.route('/registrarNodo', methods=['POST'])
def registrarNodo():
    print("Registrando nodo", request.args.get('url'), request.args.get('port'))
        
    tipo_nodo = request.args.get('tipo_nodo')
    nodo_destino = request.args.get('url')+':'+request.args.get('port')

        
    if tipo_nodo and nodo_destino:
        mycursor.execute("UPDATE tipos SET nodoDestino = %s, updatedAt = NOW() WHERE nombre = %s", (nodo_destino, tipo_nodo.lower()))
        mydb.commit()
        return jsonify({"status": "ok"})
    else:
        return jsonify({"Error": 'Falta tipo de documento o nodo destino'})
    
@app.route('/insert', methods=['POST'])
def insert():
    documento = request.json
    print(documento)
    tipo = documento['tipo_doc']
    mycursor.execute("SELECT nodoDestino FROM tipos WHERE nombre = %s", (tipo.lower(),))
    nodo_destino = mycursor.fetchone()

    if nodo_destino:
        response = requests.post('http://' + nodo_destino[0] + '/insertDoc', json=documento)
        if response.status_code == 200:
            return jsonify({"status": "ok"})
        else:
            return jsonify({"Error": 'Error en la insercion'})
    else:
        return jsonify({"Error": 'Tipo de documento no encontrado'})

@app.route('/query')
def test():
    try:
        tipo_doc = request.args.get('tipo_doc')
        titulo = request.args.get('titulo')
        #print(titulo)
        if tipo_doc:
            print("Query de tipo: ",tipo_doc)
            resultados = []
            tiposDocs = tipo_doc.split(' ')
            for tipo in tiposDocs:
                mycursor.execute("SELECT nombre, nodoDestino FROM tipos WHERE nombre = %s", (tipo.lower(),))
                nodo = mycursor.fetchone()
                print(nodo)
                if nodo:
                    response = requests.get("http://" + nodo[1] + '/searchDocs', params={'tipo_doc': tipo})
                    if response.status_code == 200 and response.json() != []:
                        resultados.extend(response.json())
                    
                    else:
                        resultados.append([{"Hint": 'Base de datos se encuentra vacia', "tipo": tipo, "status": "200 - OK"}])
                else:
                    resultados.append([{"Error": 'Tipo de documento no encontrado', "tipo": tipo, "status": "404 - Not Found"}])
            return jsonify(resultados)
        
    
            """
            mycursor.execute("SELECT nombre, nodoDestino FROM tipos WHERE nombre = %s", (tipo.lower(),))
                    esclavoTipo = mycursor.fetchone()
                    print(esclavoTipo)
                    if esclavoTipo:
                        esclavo = esclavoTipo[1]
                        response = requests.get(esclavo + '/searchDocs', params={'tipo_doc': tipo.lower()})
                        if response.status_code == 200:
                            return jsonify(response.json())
                        else:
                            return jsonify({"Error": 'Error en la consulta'})
                    else:
                        return jsonify({"Error": 'Tipo de documento no encontrado'})
            """      

            
        elif titulo:
            mycursor.execute("SELECT nombre, nodoDestino FROM tipos")
            esclavos = mycursor.fetchall()
            resultados = []
            for esclavo in esclavos:
                print(esclavo)
                response = requests.get("http://" + esclavo[1] + '/searchTitulo', params={'titulo': titulo})
                if response.status_code == 200:
                    resultados.extend(response.json())
            return jsonify(resultados)
        else:
            return jsonify({"Error": 'No se especifico operacion'})
        
    except Exception as e:
        return jsonify({"Error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
