import sqlite3 as sql
import datetime
from scrap_url import get_items_data, request_categorias_and_main_urls, find_child_urls

path = "database/rtr_crawler_db.db"


def create_tables ():
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''
        CREATE TABLE precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        articulo TEXT NOT NULL,
        precio REAL NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -precios- creada correctamente")

def insert_in_table(table,item_list):
    with sql.connect(path) as connection:
        actual_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = connection.cursor()
        instruccion = f"INSERT INTO {table} VALUES (NULL,?, ?, ?,'{actual_date}')"
        cursor.executemany(instruccion, item_list)
        connection.commit()

#Request data from all categories and insert them in DB
def request_all_and_insert(table='precios'):
    categories_and_urls = [(i[2],i[1]) for i in request_categorias_and_main_urls()]
    for main_urls in categories_and_urls:         
        child_urls = find_child_urls(main_urls[1]) #List    
        for url in child_urls:
                print (url)
                item_list = get_items_data(url)
                insert_in_table(table,item_list)

def request_category_and_insert(cat=0,table='precios'):
    categories_and_urls = [(i[2],i[1]) for i in request_categorias_and_main_urls()]
    main_urls = categories_and_urls[cat]
    child_urls = find_child_urls(main_urls[1]) #List    
    for url in child_urls:
            print (url)
            item_list = get_items_data(url)
            #insert_in_table(table,item_list)
            print(item_list[0])
            #print("")
    



#Rebuild_db_with_tables ()
def rebuild_db_with_tables ():
    create_tables()
    request_all_and_insert()







