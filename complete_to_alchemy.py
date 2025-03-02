import sqlite3 as sql
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalch_queries import obtener_articulos_por_categoria

# Old SQLite database
old_db_path = 'database/rtr_crawler_dbCompleta.db'

def old_db_data(old_db_path = 'database/rtr_crawler_dbCompleta.db'):
    with sql.connect(old_db_path) as connection:
        old_cursor = connection.cursor()
        old_cursor.execute(f'SELECT * FROM precios')
        rows = old_cursor.fetchall()

        return rows

#### TRABAJANDO CON FECHAS ####


def obtener_fechas_unicas_old_db():
    with sql.connect(old_db_path) as connection:
        old_cursor = connection.cursor()
        old_cursor.execute('SELECT DISTINCT fecha FROM precios')
        fechas_unicas = old_cursor.fetchall()
        fechas_unicas = [date[0] for date in fechas_unicas]
        return fechas_unicas

'''
# Not in USE
def formatear_fecha_unica(fecha):
    fecha_dt = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    fecha_formateada = fecha_dt.strftime('%Y-%m-%d')
    return fecha_formateada

# Not in USE
def fechas_unicas_in_old_db():
    final_fechas_unicas = []
    for fecha in obtener_fechas_unicas_old_db():
        fecha_formateada = formatear_fecha_unica(fecha)
        if fecha_formateada not in final_fechas_unicas:
            final_fechas_unicas.append(fecha_formateada)
    return final_fechas_unicas
'''

#### SELECCIONANDO DATOS ####

# DATOS OLD DB por Categoría y fecha única. 
def cat_date_data_old_db(cat,fecha):
    with sql.connect(old_db_path) as connection:
        old_cursor = connection.cursor()

        instruccion = f'SELECT * FROM precios WHERE categoria = ? AND fecha = ?'
        old_cursor.execute(instruccion,(cat,fecha))
        datos_old_cat_fecha = old_cursor.fetchall()

    return datos_old_cat_fecha

# for i in (cat_date_data_old_db('Coches',(obtener_fechas_unicas_old_db()[0]))):
#     print(i)



##### OBTENIENDO LISTA DE ART DECLARADOS DB ALCHEMY ####

for art in obtener_articulos_por_categoria('Coches'):
    print(art)

