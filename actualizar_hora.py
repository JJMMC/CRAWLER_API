import sqlite3 as sql
from datetime import datetime

# Old SQLite database
old_db_path = 'database/rtr_crawler_dbCompleta.db'

def actualizar_hora_fecha():
    with sql.connect(old_db_path) as connection:
        old_cursor = connection.cursor()
        
        # Seleccionar todas las fechas
        old_cursor.execute('SELECT id, fecha FROM precios')
        rows = old_cursor.fetchall()
        
        # Actualizar cada fecha
        for row in rows:
            id, fecha_str = row
            fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            nueva_fecha_str = fecha_dt.strftime('%Y-%m-%d') + ' 20:43:00'
            
            # Actualizar la fila en la base de datos
            old_cursor.execute('UPDATE precios SET fecha = ? WHERE id = ?', (nueva_fecha_str, id))
        
        # Guardar los cambios
        connection.commit()

# Llamar a la función para actualizar las fechas
actualizar_hora_fecha()