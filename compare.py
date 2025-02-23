import sqlite3 as sql
from datetime import datetime
from config_db import obtener_lista_articulos_declarados

path = "database/rtr_crawler.db"

def obtener_todo(path = "database/rtr_crawler.db", tabla="historial_precios"):
    # Conectar a la base de datos SQLite
    with sql.connect(path) as connection:
        cursor = connection.cursor()

    # Obtener toda la información de la base de datos
    cursor.execute(f"SELECT rtr_id, precio, fecha  FROM {tabla} ORDER BY fecha DESC")
    todo = cursor.fetchall()# Retorna lista de tuplas (articulo, precio, fecha)
    return todo
    #return [(rtr_id, precio, datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')) for rtr_id, precio, fecha in todo]


def obtener_fechas_unicas(path = "database/rtr_crawler.db"):
    total = obtener_todo(path)
    total = [(rtr_id, precio, fecha) for rtr_id, precio, fecha in total]
    lst_fechas = []
    for articulo in total:
        if articulo[2] not in lst_fechas:
            lst_fechas.append(articulo[2])
    return(lst_fechas)

    
def obtener_precio_por_fecha(rtr_id,fecha):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT precio FROM historial_precios 
                      WHERE rtr_id = ? AND fecha = ? ORDER BY fecha DESC LIMIT 1''', (rtr_id, fecha))
        resultado = cursor.fetchone()
    return resultado[0] if resultado else None


# Función para verificar si el precio de UN artículo ha bajado
def verificar_ultimo_precio(rtr_id):
    ultimo_precio = obtener_precio_por_fecha(rtr_id, obtener_fechas_unicas()[0])
    penultimo_precio = obtener_precio_por_fecha(rtr_id, obtener_fechas_unicas()[1])
    if ultimo_precio > penultimo_precio:
        print("El precio ha SUBIDO ",ultimo_precio-penultimo_precio)
        return 
    elif ultimo_precio < penultimo_precio:
        print("El precio ha BAJADO",ultimo_precio-penultimo_precio)
        return ultimo_precio-penultimo_precio
    else:
        print("El precio sigue igual")
        return None


def verificar_todos_precios(rtr_id_lst):
    for rtr_id in rtr_id_lst:
        verificar_ultimo_precio(rtr_id)



def main():
    rtr_id_list = [rtr_id for rtr_id, _, _ in obtener_todo()]
    verificar_todos_precios(rtr_id_list)
    
	
















# 5. Flujo del programa
# Cada 15 minutos: El programa descarga los datos de los artículos desde la web.
# Para cada artículo:
# Verifica si el artículo ya existe en la base de datos. Si no, lo agrega.
# Compara el nuevo precio con el último registrado en el historial.
# Si el precio ha bajado, lo registra en el historial.
# 6. Mejoras y consideraciones
# Optimización: Si el volumen de datos es muy grande, podrías considerar el uso de índices en las columnas url y articulo_id para mejorar el rendimiento de las búsquedas.
# Alertas: Podrías configurar el programa para que, cuando detecte una bajada de precio, envíe una notificación por correo o mensaje.

