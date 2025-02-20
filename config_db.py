import sqlite3 as sql
from scrap_url import scrap_rtr_crawler, request_categorias_and_main_urls, find_child_urls
import time
from kkp2 import scraped_list

path = "database/rtr_crawler.db"

####### Funciones simples
# Crea la base de Datos y las tablas
def create_tables (path = "database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()

        #Creamos tabla HISTORIAL PRECIOS
        instruction = '''
        CREATE TABLE IF NOT EXISTS historial_precios (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	rtr_id TEXT NOT NULL UNIQUE,
    	precio REAL NOT NULL,
    	fecha TEXT DEFAULT (strftime('%d-%m-%Y', 'now', 'localtime')),
    	FOREIGN KEY (rtr_id) REFERENCES articulos(rtr_id)
		);
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -precios- creada correctamente")
        
        #Creamos tabla ARTÍCULOS
        instruction = '''
        CREATE TABLE IF NOT EXISTS articulos (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
    	nombre TEXT,
    	rtr_id TEXT NOT NULL UNIQUE,
        ean INTEGER,
        art_url TEXT,
        img_url TEXT
		);
        '''
        cursor.execute(instruction)
        connection.commit()
        print("Tabla -articulos- creada correctamente")

# Función para obtener list de tuplas (id,rtr_id)
def obtener_lista_articulos_declarados(path = "database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT id, rtr_id FROM articulos ''')
        id_rtrid_lst = cursor.fetchall()        
    return id_rtrid_lst

# Función para agregar un artículo
def agregar_articulo( categoria, nombre, rtr_id, ean, art_url, img_url,  path = "database/rtr_crawler.db"):

    # Comprobamos que el artículo no esta en la tabla de artículos
    rtr_ids_lst = [rtr_id[1] for rtr_id in obtener_lista_articulos_declarados()]    
    if rtr_id in rtr_ids_lst:
        print("Artículo DUPLICADO en tabla")
        return False
    
    # Insertamos datos en tabla
    else:    
        with sql.connect(path) as connection:
            cursor = connection.cursor()
            instruction = '''INSERT OR IGNORE INTO articulos (categoria, nombre, rtr_id, ean, art_url, img_url)
                            VALUES (?, ?, ?, ?, ?, ?)'''
            cursor.execute(instruction, (categoria, nombre, rtr_id, ean, art_url, img_url))
            connection.commit()

# Función para agregar el precio de un artículo al historial
def agregar_precio(rtr_id, precio, path = "database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''INSERT INTO historial_precios (rtr_id, precio) 
                      VALUES (?, ?)'''
        cursor.execute(instruction, (rtr_id, precio))
        connection.commit()

#### Funciones de Comprobación  ####
# Check if rtr_id in tabla articulos
def check_rtr_id_in_articulos(scraped_product):
    new_cat,new_rtr_id,new_name, new_price, new_ean, new_art_url, new_art_img_url = scraped_product    
    if new_rtr_id in [ rtr_id for id, rtr_id in obtener_lista_articulos_declarados()]:
        print('Artículo declarado en la lista de artículos')
        return True
    else:
        print('Artículo no declarado en la lisa de artículos')
        print('Agregando NUEVO RTR_ID')
        agregar_articulo(new_cat, new_name, new_rtr_id, new_ean, new_art_url, new_art_img_url)
        return False
        
        
def check_double_data_in_db():
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT articulo_id, fecha FROM historial_precios ''')
        dbl_check_list = cursor.fetchall()
        
        ids_vistos = set()
        duplicados = set()
    
        for id, fecha in dbl_check_list:
            #time.sleep(0.3)
            print(id)
            if id in ids_vistos:
                duplicados.add(id)
                print("Elemento duplicado encontrado", id)
            else:
                ids_vistos.add(id)
                print('ok')
       
        print(ids_vistos)
        return list(duplicados)

#### Funciones Complejas  ####

# Actualiza la tabla de artículos
def update_tabla_articulos():
    #Update tabla ARTICULOS
    print("Inicio UPDATE ARTICULOS")
    for cat, rtr_id, name, price, ean, art_url, art_img_url in scrap_rtr_crawler():
        agregar_articulo(cat, name, rtr_id, ean, art_url, art_img_url )
        #print(f'Artículos agregados a categoria: {cat}')
    print("Tabla Articulos ACTUALIZADA")

# Actualiza la tabla de precio
def update_tabla_precios():
    #Update tabla ARTICULOS
    print("Inicio UPDATE PRECIOS")
    for cat, rtr_id, name, price, ean, art_url, art_img_url in scrap_rtr_crawler():
        agregar_precio(rtr_id,price)


def eliminar_filas_por_fecha(fecha, path="database/rtr_crawler.db"):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        instruction = '''DELETE FROM historial_precios WHERE fecha = ?'''
        cursor.execute(instruction, (fecha,))
        connection.commit()
        print(f"Filas con fecha {fecha} eliminadas correctamente")

# # Ejemplo de uso
# fecha_especifica = "2025-02-17"
# eliminar_filas_por_fecha(fecha_especifica)

create_tables()
update_tabla_articulos()
update_tabla_precios()



