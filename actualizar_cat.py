import sqlite3 as sql
from datetime import datetime

# Old SQLite database
old_db_path = 'database/rtr_crawler_dbCompleta.db'

def actualizar_categorias():
    with sql.connect(old_db_path) as connection:
        old_cursor = connection.cursor()
        
        # Seleccionar todas las categorías
        old_cursor.execute('SELECT id, categoria FROM precios')
        rows = old_cursor.fetchall()
        
        # Actualizar cada categoría
        for row in rows:
            id, categoria = row
            categoria_strip = categoria.strip()
            
            # Actualizar la fila en la base de datos
            old_cursor.execute('UPDATE precios SET categoria = ? WHERE id = ?', (categoria_strip, id))
        
        # Guardar los cambios
        connection.commit()

# Llamar a la función para actualizar las categorías
actualizar_categorias()