import sqlite3 as sql
from datetime import datetime

path = "database/rtr_crawler.db"

def obtener_todo(path = "database/rtr_crawler.db", tabla="historial_precios"):
    # Conectar a la base de datos SQLite
    with sql.connect(path) as connection:
        cursor = connection.cursor()

    # Obtener toda la información de la base de datos
    cursor.execute(f"SELECT articulo_id, precio, fecha  FROM {tabla} ORDER BY fecha DESC")
    todo = cursor.fetchall()# Retorna lista de tuplas (categoria, articulo, precio, fecha)
    return todo
    #return [(articulo_id, precio, datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')) for articulo_id, precio, fecha in todo]


def obtener_fechas_unicas(path = "database/rtr_crawler.db"):
    total = obtener_todo(path)
    total = [(articulo_id, precio, datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')) for articulo_id, precio, fecha in total]
    lst_fechas = []
    for articulo in total:
        if articulo[2] not in lst_fechas:
            lst_fechas.append(articulo[2])
    return(lst_fechas)


def obtener_ultimo_precio(articulo_id):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT precio FROM historial_precios 
                      WHERE articulo_id = ? ORDER BY fecha DESC LIMIT 1''', (articulo_id,))
        resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def contar_entradas_articulo(articulo_id):
    with sql.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM historial_precios 
                          WHERE articulo_id = ?''', (articulo_id,))
        resultado = cursor.fetchone()
    return resultado[0] if resultado else 0


print(contar_entradas_articulo(13))






	

# Para almacenar datos en una base de datos SQLite y realizar un seguimiento de los cambios de precios, lo más recomendable es estructurar bien las tablas y mantener un historial de los precios de los artículos. Te sugeriría una estructura de base de datos con al menos dos tablas: una para los artículos y otra para el historial de precios.

# Aquí te dejo un esquema básico para las tablas y algunas ideas sobre cómo podrías implementar la solución:

# 1. Tablas de la base de datos
# Tabla de Artículos

# CREATE TABLE IF NOT EXISTS articulos (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nombre TEXT NOT NULL,
#     descripcion TEXT,
#     url TEXT UNIQUE,
#     categoria TEXT
# );
# Tabla de Historial de Precios

# CREATE TABLE IF NOT EXISTS historial_precios (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     articulo_id INTEGER,
#     precio REAL NOT NULL,
#     fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (articulo_id) REFERENCES articulos(id)
# );
# 2. Explicación de la estructura
# articulos: Esta tabla almacena la información básica del artículo (nombre, descripción, URL, categoría, etc.).
# historial_precios: Esta tabla guarda el historial de precios de cada artículo. En cada descarga que hagas desde la web, se añadirá un nuevo registro a esta tabla con el precio actualizado del artículo en la fecha actual. Cada entrada está relacionada con un artículo específico mediante articulo_id.
# 3. Cómo actualizar los datos
# Cuando descargues los datos de la web cada 15 minutos, seguirías estos pasos:

# Verificar si el artículo ya existe en la base de datos:
# Si el artículo ya existe (basado en su URL o nombre), actualizas el precio en la tabla historial_precios.
# Si no existe, primero debes agregarlo a la tabla articulos y luego insertar el precio en historial_precios.
# Insertar nuevos precios en historial_precios:
# Si el precio ha cambiado respecto a la última captura, se guarda el nuevo precio.
# Si no ha cambiado, puedes optar por no guardar el nuevo precio o, si lo deseas, guardar todos los precios para tener un historial completo.
# Comparar precios con los registros anteriores:
# Puedes consultar el historial de precios de cada artículo para detectar si ha bajado el precio respecto a la última captura. Para esto, puedes hacer una consulta a la base de datos comparando el último precio con el precio actual.
# 4. Código de ejemplo en Python con SQLite
# Aquí tienes un ejemplo de cómo implementar la inserción y comparación de precios usando SQLite en Python:

# import sqlite3
# from datetime import datetime

# # Conexión a la base de datos SQLite
# conn = sqlite3.connect('articulos.db')
# cursor = conn.cursor()

# # Función para agregar un artículo
# def agregar_articulo(nombre, descripcion, url, categoria):
#     cursor.execute('''INSERT OR IGNORE INTO articulos (nombre, descripcion, url, categoria)
#                       VALUES (?, ?, ?, ?)''', (nombre, descripcion, url, categoria))
#     conn.commit()

# # Función para agregar el precio de un artículo al historial
# def agregar_precio(articulo_id, precio):
#     cursor.execute('''INSERT INTO historial_precios (articulo_id, precio) 
#                       VALUES (?, ?)''', (articulo_id, precio))
#     conn.commit()

# # Función para obtener el último precio de un artículo
# def obtener_ultimo_precio(articulo_id):
#     cursor.execute('''SELECT precio FROM historial_precios 
#                       WHERE articulo_id = ? ORDER BY fecha DESC LIMIT 1''', (articulo_id,))
#     resultado = cursor.fetchone()
#     return resultado[0] if resultado else None

# # Función para verificar si el precio ha bajado
# def verificar_precio_bajado(articulo_id, nuevo_precio):
#     ultimo_precio = obtener_ultimo_precio(articulo_id)
#     if ultimo_precio is None:
#         print("No hay historial de precios para este artículo.")
#     elif nuevo_precio < ultimo_precio:
#         print("¡El precio ha bajado!")
#     else:
#         print("El precio no ha bajado.")

# # Ejemplo de uso
# # Suponiendo que ya tienes el artículo con ID 1
# articulo_id = 1
# nuevo_precio = 150.0  # Precio que obtuviste de la web
# verificar_precio_bajado(articulo_id, nuevo_precio)

# # Si el precio ha bajado, puedes agregar el nuevo precio
# agregar_precio(articulo_id, nuevo_precio)

# # Cerrar la conexión
# conn.close()
# 5. Flujo del programa
# Cada 15 minutos: El programa descarga los datos de los artículos desde la web.
# Para cada artículo:
# Verifica si el artículo ya existe en la base de datos. Si no, lo agrega.
# Compara el nuevo precio con el último registrado en el historial.
# Si el precio ha bajado, lo registra en el historial.
# 6. Mejoras y consideraciones
# Optimización: Si el volumen de datos es muy grande, podrías considerar el uso de índices en las columnas url y articulo_id para mejorar el rendimiento de las búsquedas.
# Alertas: Podrías configurar el programa para que, cuando detecte una bajada de precio, envíe una notificación por correo o mensaje.

