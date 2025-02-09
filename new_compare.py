import sqlite3 as sql
from datetime import datetime

db_path = "database/rtr_crawler_db.db"

def obtener_fechas(path, tabla="precios"):
    # Conectar a la base de datos SQLite
    with sql.connect(path) as connection:
        cursor = connection.cursor()

    # Obtener los precios de todos los productos
    cursor.execute(f"SELECT fecha FROM {tabla}")
    todo = cursor.fetchall()# 
    print (type(todo))
    print(todo[0])
    #return [datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y') for fecha in todo]

obtener_fechas(db_path)
# lst_fechas = []
# for fecha in obtener_fechas(db_path):

#     if fecha not in lst_fechas:
#         lst_fechas.append(fecha)
# print (lst_fechas)




'''
def obtener_todo(path, tabla="precios"):
    # Conectar a la base de datos SQLite
    with sql.connect(path) as connection:
        cursor = connection.cursor()

    # Obtener los precios de todos los productos
    cursor.execute(f"SELECT categoria, articulo, precio, fecha FROM {tabla}")
    todo = cursor.fetchall()# Retorna lista de tuplas (categoria, articulo, precio, fecha)
    print(len(todo))
    # Devolver un diccionario con el id del producto como clave y como valor una lista con (categoria, precio, fecha)
    #return {articulo:[categoria, precio, fecha] for categoria, articulo, precio, fecha in todo}
    return {articulo:[categoria, precio, fecha] for categoria, articulo, precio, fecha in todo}
# print("\n",obtener_todo(db_path),"\n")

total = obtener_todo(db_path)
print (type(total))
print (len(total))
# for articulo in total:
#     print ("\n", articulo)
#     print ("\n", total[articulo])   
#     print ("\nCategoria", total[articulo][0])
#     print ("\nPrecio", total[articulo][1])
#     print ("\nFecha", total[articulo][2])


def obtener_fechas():
    total = obtener_todo(db_path)
    lst_fechas = []
    for articulo in total:
        fecha_formateada = datetime.strptime(total[articulo][2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        if fecha_formateada not in lst_fechas:
            lst_fechas.append(fecha_formateada)
    return lst_fechas

print (obtener_fechas())
'''