from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
def conectar():
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'
    engine = create_engine(url)
    return engine

##try:
    engine = conectar()
    engine.connect()
    print("Conexión exitosa a la base de datos.")
##except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    