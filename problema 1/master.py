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

# Ruta para registrar la direccion del nodo esclavo (url / ip y puerto)
@app.route('/registrarNodo', methods=['POST'])
def registrarNodo():
    print("Registrando nodo", request.args.get('url'), request.args.get('port'))
        
    tipo_nodo = request.args.get('tipo_nodo')
    nodo_destino = request.args.get('url')+':'+request.args.get('port')

    # Verificacion de parametros
    if tipo_nodo and nodo_destino:
        mycursor.execute("UPDATE tipos SET nodoDestino = %s, updatedAt = NOW() WHERE nombre = %s", (nodo_destino, tipo_nodo.lower()))
        mydb.commit()
        return jsonify({"status": "ok"})
    else:
        return jsonify({"Error": 'Falta tipo de documento o nodo destino'})
    
# Ruta para insertar un documento nuevo
@app.route('/insert', methods=['POST'])
def insert():
    documento = request.json
    print(documento)
    tipo = documento['tipo_doc'] # Tipo de documento, uso para buscar el nodo destino
    mycursor.execute("SELECT nodoDestino FROM tipos WHERE nombre = %s", (tipo.lower(),))
    nodo_destino = mycursor.fetchone()

    # Si encontramos el nodo destino, enviamos el documento
    if nodo_destino: 
        response = requests.post('http://' + nodo_destino[0] + '/insertDoc', json=documento) #Envio a nodo destino
        if response.status_code == 200:
            return jsonify({"status": "ok"})
        else:
            return jsonify({"Error": 'Error en la insercion'})
    # Si no encontramos el nodo destino, retornamos un error
    else:
        return jsonify({"Error": 'Tipo de documento no encontrado'})

@app.route('/query')
def test():
    try:
        tipo_doc = request.args.get('tipo_doc')
        titulo = request.args.get('titulo')
        # Busqueda por tipo de documento
        if tipo_doc:
            #print("Query de tipo: ",tipo_doc)
            resultados = []
            tiposDocs = tipo_doc.split(' ') # Split de los tipos de documentos
            for tipo in tiposDocs: # Busqueda de cada tipo de documento
                mycursor.execute("SELECT nombre, nodoDestino FROM tipos WHERE nombre = %s", (tipo.lower(),)) # Busqueda del nodo destino
                nodo = mycursor.fetchone()
                print(nodo)
                if nodo: # Si encontramos el nodo destino, enviamos la peticion
                    response = requests.get("http://" + nodo[1] + '/searchDocs', params={'tipo_doc': tipo})
                    if response.status_code == 200 and response.json() != []:
                        resultados.extend(response.json())
                    
                    else: # Si el nodo esta vacio, agregamos un aviso a la lista a entregar
                        resultados.append([{"Hint": 'Base de datos se encuentra vacia', "tipo": tipo, "status": "200 - OK"}])
                else: # Si no encontramos el nodo destino, agregamos un error a la lista a entregar
                    resultados.append([{"Error": 'Tipo de documento no encontrado', "tipo": tipo, "status": "404 - Not Found"}])
            return jsonify(resultados)
        
        # Busqueda por titulo   
        elif titulo:
            mycursor.execute("SELECT nombre, nodoDestino FROM tipos") #Obtenemos todos los nodos esclavos
            esclavos = mycursor.fetchall()
            resultados = []
            # recorremos todos los esclavos
            for esclavo in esclavos:
                print("Consultando nodo: ", esclavo[0])
                response = requests.get("http://" + esclavo[1] + '/searchTitulo', params={'titulo': titulo}) #enviamos la peticion al nodo
                if response.status_code == 200:
                    resultados.extend(response.json())
            return jsonify(resultados)
        else: # Si no recibimos tipo_doc o titulo para query, retornamos un error
            return jsonify({"Error": 'No se especifico operacion'})
        
    except Exception as e:
        return jsonify({"Error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
