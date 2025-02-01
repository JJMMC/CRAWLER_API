import sqlite3 as sql
import datetime
from scrap_url import *

path = "database/compare.db"


def create_tables ():
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''
        CREATE TABLE IF NOT EXISTS rtr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            articulo TEXT NOT NULL,
            precio REAL, 
            date TIMESTAMP
        );
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -rtr- creada correctamente")


def insert_in_table(table='rtr'):
    categorias_y_urls = [(i[2],i[1]) for i in request_categorias_and_main_urls()]
    for i in categorias_y_urls:
        print(i)
    
    for i in categorias_y_urls:
        urls = (urls_in_categoria(i[1]))
        for url in urls:
            print (url)
            data = get_items_price(url) #-> Lista de tuplas
            print (data)

    #Creamos la lista de tuplas final para el QUERY tuple(cat,item,)

    # with sql.connect(path) as connection:
    #     actual_date = datetime.datetime.now()
    #     cursor = connection.cursor()
    #     instruction = '''
    #     INSERT INTO {table} VALUES () 
    #     '''

insert_in_table()







