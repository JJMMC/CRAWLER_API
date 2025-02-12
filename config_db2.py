import sqlite3 as sql
import time
from scrap_url import get_items_data, request_categorias_and_main_urls, find_child_urls

path = "database/rtr_crawler.db"


def create_tables (path = "database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()

        #Creamos tabla HISTORIAL PRECIOS
        instruction = '''
        CREATE TABLE IF NOT EXISTS historial_precios (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	articulo_id INTEGER,
    	precio REAL NOT NULL,
    	fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    	FOREIGN KEY (articulo_id) REFERENCES articulos(id)
		);
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -precios- creada correctamente")
        
        #Creamos tabla ARTÍCULOS
        instruction = '''
        CREATE TABLE IF NOT EXISTS articulos (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	nombre TEXT NOT NULL UNIQUE,
    	categoria TEXT
		);
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -articulos- creada correctamente")

# Función para obtener list de tuplas (id,nombre)
def obtener_articulo_id_nombre(path = "database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT id, nombre FROM articulos ''')
        id_name_lst = cursor.fetchall()        
    return id_name_lst

# Función para agregar un artículo
def agregar_articulo(nombre, categoria):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''INSERT OR IGNORE INTO articulos (nombre, categoria)
                         VALUES (?, ?)'''
        cursor.execute(instruction, (nombre, categoria))
        connection.commit()

# Función para agregar el precio de un artículo al historial
def agregar_precio(articulo_id, precio, path = "database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''INSERT INTO historial_precios (articulo_id, precio) 
                      VALUES (?, ?)'''
        cursor.execute(instruction, (articulo_id, precio))
        connection.commit()


def request_and_insert_all():
    categories_and_urls = [(i[2],i[1]) for i in request_categorias_and_main_urls()]
    for main_urls in categories_and_urls:         
        child_urls = find_child_urls(main_urls[1]) #List    
        for url in child_urls:
                print (url)
                item_list = get_items_data(url) #list(cat, name, price)
                for cat_to_import, nom_to_import, pre_to_import in item_list:
                    check_article_id_and_insert(cat_to_import, nom_to_import, pre_to_import)
                

def check_article_id_and_insert(cat_to_import, nom_to_import, pre_to_import):        
    id_nom_lst = obtener_articulo_id_nombre()#lista tuplas(id,nombre) TABLA ARTICULOS

    if nom_to_import in [nom for id, nom in id_nom_lst]:#Comprobamos si el artículo está en la TABLA ARTICULOS
        print ("SI está en Tabla artículos")
        for articulo_id, nombre in id_nom_lst: #Desempaquetamos list id's y nombres y nos movemos por la lista 
            if nom_to_import == nombre: #Buscamos el id vía el nombre 
                    print('ID localizado; Insertamos nuevo precio')
                    agregar_precio(articulo_id, pre_to_import)
                    #time.sleep(1)
            else:
                continue
    else:
        agregar_articulo(nom_to_import,cat_to_import)
        check_article_id_and_insert(cat_to_import, nom_to_import, pre_to_import)




#request_and_insert_all()










