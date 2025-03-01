from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from models import HistorialPrecio

# Conexión a la base de datos SQLite original
engine_src = create_engine('sqlite:///rtr_crawler.db')
metadata_src = MetaData()
historial_precios_src = Table('historial_precios', metadata_src, autoload_with=engine_src)

# Conexión a la base de datos SQLite destino
engine_dst = create_engine('sqlite:///rtr_crawler_Alchemy.db')
Session = sessionmaker(bind=engine_dst)
session_dst = Session()

# Leer datos de la tabla historial_precios de la base de datos original
with engine_src.connect() as connection:
    result = connection.execute(historial_precios_src.select())
    rows = result.fetchall()

# Insertar datos en la tabla historial_precios de la base de datos destino
for row in rows:
    historial_precio = HistorialPrecio(
        id=row['id'],
        rtr_id=row['rtr_id'],
        precio=row['precio'],
        fecha=row['fecha']
    )
    session_dst.add(historial_precio)

# Confirmar la transacción
session_dst.commit()
session_dst.close()

print("Datos importados exitosamente.")