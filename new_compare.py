import sqlite3 as sql
from datetime import datetime

db_path = "database/rtr_crawler_db.db"

def obtener_todo(path, tabla="precios"):
    # Conectar a la base de datos SQLite
    with sql.connect(path) as connection:
        cursor = connection.cursor()

    # Obtener toda la información de la base de datos
    cursor.execute(f"SELECT categoria, articulo, precio, fecha FROM {tabla}")
    todo = cursor.fetchall()# Retorna lista de tuplas (categoria, articulo, precio, fecha)

    return [(articulo, categoria, precio, datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')) for categoria, articulo, precio, fecha in todo]


def obtener_fechas_unicas():
    total = obtener_todo(db_path)
    lst_fechas = []
    for articulo in total:
        if articulo[3] not in lst_fechas:
            lst_fechas.append(articulo[3])
    return(lst_fechas)


