from flask import Flask, jsonify, request
import sqlite3
from archivos import list_of_dbs
from querys_db import dict_of_tables
from create_JSON import table_to_dict

app = Flask(__name__)

#####################
# Conectar a la base de datos SQLite
def obtener_conexion(file="rtr_db.db"):
    path = f"database/{file}"
    #print (path)
    return sqlite3.connect(path)
    #return sqlite3.connect('database/rtr_db.db')

def obtener_basesdedatos():
    return list_of_dbs()
    
# Obtener todas las tablas de la base de datos
def obtener_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    conexion.close()
    return [tabla[0] for tabla in tablas]



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
