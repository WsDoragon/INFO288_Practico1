# esclavo.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos simulada para este esclavo
base_de_datos = {
    "tesis": ["Tesis sobre...", "Otra tesis..."],
    # Agrega más tipos de documentos y datos según sea necesario
}

@app.route('/search?tipo_doc')
def search():
    titulo = request.args.get('titulo')
    tipo_doc = request.args.get('tipo_doc')

    if tipo_doc in base_de_datos:
        # Realizar búsqueda en la base de datos del esclavo
        resultados = [documento for documento in base_de_datos[tipo_doc]]
        return jsonify(resultados)
    else:
        return jsonify([])
    
@app.route('/search?titulo')
def searchTitle():
    titulo = request.args.get('titulo')
    resultados = []
    #Busqueda en la base de datos mediante el titulo
    for documentos in base_de_datos.items():
        for documento in documentos:
            if titulo in documento:
                resultados.append(documento)

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Cambia el puerto para cada esclavo
