from flask import Flask, jsonify
from archivos import list_of_dbs
from querys_db import dict_of_tables
from create_JSON import table_to_dict

app = Flask(__name__)


#############


@app.route('/')
def index():
    return ''' "Base Datos RTR" 
    /tabla --> Listado de tablas
    /tabla/"tabla" --> Datos de la tabla seleccionada
    '''

@app.route('/tabla/<table_id>', methods=['GET'])
def mostrar_tabla(table_id):
    response = table_to_dict(table_id)
    return jsonify(response)

@app.route('/tabla', methods=['GET'])
def lista_tabla():
    response = dict_of_tables()
    print(response)
    return jsonify(response)
    #return "Listado de Tablas"

if __name__ == "__main__":
    app.run(debug=True)
