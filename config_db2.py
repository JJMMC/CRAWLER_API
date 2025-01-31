import sqlite3 as sql
import datetime
from scrap_url import *

path = "database/compare.db"

def create_db():
    conn = sql.connect(path)
    conn.commit ()
    conn.close()

# Crea tablas en funcion de una lista dada con ID de ARTICULO y DATESTAMP ojo detect_types en SQLITE
def create_tables (nombres_tablas):
    for i in nombres_tablas:
        conn = sql.connect(path,
                             detect_types=sql.PARSE_DECLTYPES |
                             sql.PARSE_COLNAMES)
        cursor = conn.cursor()
        instruccion = f"CREATE TABLE IF NOT EXISTS {i} (id_it INTEGER NOT NULL PRIMARY KEY, nombre_it TEXT, precio_it REAL, date TIMESTAMP)"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()

# Introduce list() de datos en la tabla dada y TIMESTAMP
def insert_family_data_in_table(table, item_list):
    actual_date = datetime.datetime.now()
    conn = sql.connect(path, detect_types=sql.PARSE_DECLTYPES |sql.PARSE_COLNAMES)
    cursor = conn.cursor()
    instruccion = f"INSERT INTO {table} VALUES (NULL,?, ?,'{actual_date}')"
    cursor.executemany(instruccion, item_list)
    conn.commit()
    conn.close()

# Insert all data in tables
def insert_all ():    
    categorias_y_urls = [(i[2],i[1]) for i in request_categorias_and_main_urls()]
    for i in categorias_y_urls:
        print(i)

    #Accedemos a las pág child de las urls
    for i in categorias_y_urls:
        urls = (urls_in_categoria(i[1]))
        for url in urls:
            print (url)
            data = get_items_price(url)
            insert_family_data_in_table (i[0],data)

#Rebuild_db_with_tables ()
def rebuild_db_with_tables ():
    create_db()
    categorias = [i[2] for i in request_categorias_and_main_urls()]
    create_tables(categorias)
    insert_all()






