# maestro.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Diccionario que mapea tipos de documento a los esclavos correspondientes
esclavos_por_tipo = {
    "tesis": "http://localhost:5001",
    "libro": "http://esclavo2:5002",
    "video": "http://esclavo3:5003",
    # Agrega más tipos de documentos y esclavos según sea necesario
}

print("hola")

@app.route('/query')
def query():
    tipo_doc = request.args.get('tipo_doc')
    titulo = request.args.get('titulo')
    if tipo_doc:
        esclavos = [esclavos_por_tipo[doc] for doc in tipo_doc.split('+')]
    else:
        # Si no se proporciona tipo_doc, enviar la consulta a todos los esclavos
        esclavos = list(esclavos_por_tipo.values())

    resultados = []

    for esclavo_url in esclavos:
        # Realizar la consulta a cada esclavo
        response = requests.get(esclavo_url + '/search', params={'tipo_doc': tipo_doc})
        if response.status_code == 200:
            # Agregar los resultados de este esclavo a la lista total de resultados
            resultados.extend(response.json())

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
