import sqlite3 as sql
import os

def show_table_data(table):
	for i in table:
		print(i[0],".-",i[1], "Precio", i[2])
		#print(i[1:3])



def read_all_rows(tabla):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} "
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()    
    #print (show_table_data(datos))
    return datos
# print (read_all_rows("Coches"))
# Conectar a la base de datos SQLite

def obtener_conexion(file="rtr_db.db"):
    path = f"database/{file}"
    #print (path)
    return sql.connect(path)
    #return sqlite3.connect('database/rtr_db.db')


    
# Obtener todas las tablas de la base de datos
def obtener_tablas(file="rtr_db.db"):
    conn = obtener_conexion(file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    conn.close()
    return [tabla[0] for tabla in tablas] #Lista []



def dict_of_tables(file="rtr_db.db"):
    table_lst = obtener_tablas(file)
    data = {}
    data["Tablas"] = []
    for index in range(len(table_lst)):
        #print(index)
        data["Tablas"].append({
		    index+1:table_lst[index]
		    })
    #print(data)
    return data #Dict {}

def dict_of_tables_items(file="rtr_db.db"):
    table_lst = obtener_tablas(file)
    data = {}
    data["Tablas"] = []
    for index in range(len(table_lst)):
        #print(index)
        data["Tablas"].append({
		    table_lst[index]:read_all_rows(table_lst[index])
		    })
    #print(data)
    return data #Dict {}


#Función para filtrar por precio MENOR
def filter_precio_menor (tabla,precio):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE precio_it < {precio} ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Función para filtrar por precio MAYOR
def filter_precio_mayor (tabla,precio):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE precio_it > {precio} ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Función para filtrar por precio IGUAL
def filter_precio_igual (tabla,precio):
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE precio_it = {precio} ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Función para filtrar resultados de una tabla por precio. 3 tipos: menor,mayor o igual.
def filter_precio (tipo,tabla,precio):
    if tipo == "menor":
        result_filter = filter_precio_menor (tabla,precio)
        return result_filter
    elif tipo == "mayor":
        result_filter = filter_precio_mayor (tabla,precio)
        return result_filter
    elif tipo == "igual":
        result_filter = filter_precio_igual (tabla,precio)
        return result_filter
    elif tipo == "todo":
        result_filter = read_all_rows(tabla)
        return result_filter
    else:
        print("ERROR")

#Funcion para filtrar por nombre
def filter_nombre (tabla, nombre):
    #nombre = f"%{nombre}%"
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM {tabla} WHERE nombre_it LIKE '%{nombre}%' ORDER BY precio_it DESC"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()   
    return datos

#Funcion para saber si esta creada la BD
def check_if_db_exists(db_directory = "database/rtr_db.db"):
	if os.path.exists(db_directory):
		return (True)
	else:
		return (False)

#Funcion para saber si la BD esstá vacía
def check_if_empty_db(db_directory = "database/rtr_db.db"):
	if obtener_tablas(db_directory) == []:
		print ("Base de datos vacía")
	else:
		print ("Base de datos llena")



def colum_names(nombre_tabla):
    # Conectar a la base de datos SQLite (asegúrate de que el archivo exista)
    conn = sql.connect("database/rtr_db.db")
    cursor = conn.cursor()
    nombre_tabla = 'Coches'# Especificar el nombre de la tabla
    cursor.execute(f"PRAGMA table_info({nombre_tabla})") # Obtener la información de la tabla
    columnas = cursor.fetchall()    # Obtener los resultados
    nombres_columnas = [columna[1] for columna in columnas] # Extraer solo los nombres de las columnas
    conn.close()
    return(nombres_columnas)


