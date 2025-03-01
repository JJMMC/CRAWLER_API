from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from models import engine, Articulo, HistorialPrecio
from sqlalchemy import insert, select, join



app = Flask(__name__)

# Crear una sesión - Conexión que nos permite interactuar con la base de datos
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        return session
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

@app.route('/')
def index():
    return ''' "Base Datos RTR" '''

@app.route('/articulos', methods=['GET'])
def get_articulos():
    session = get_session()
    try:
        stmt = select(Articulo)
        result = session.execute(stmt)
        articulos = []
        for articulo in result.scalars():
            articulo_dict = articulo.__dict__.copy()
            articulo_dict.pop('_sa_instance_state', None)
            articulos.append(articulo_dict)
        return jsonify(articulos)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
