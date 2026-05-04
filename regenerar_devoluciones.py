import mysql.connector
import random
import pandas as pd
from faker import Faker
from dotenv import load_dotenv
from db_connector import conectar
import os

load_dotenv()
fake = Faker()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME")
}

def generar_devoluciones(cursor, ticket_ids, productos_df):
    motivos = ["Talla incorrecta", "Defecto", "No convence", "Color diferente", "Regalo duplicado"]
    tickets_con_devolucion = random.sample(ticket_ids, int(len(ticket_ids) * 0.05))
    
    for ticket_id in tickets_con_devolucion:
        producto_id = random.randint(1, 400)
        producto = productos_df[productos_df['id'] == producto_id]
        talla = producto['talla'].values[0]
        precio = producto['precio_venta'].values[0]
        
        if talla in ['XS', 'XXL']:
            motivo = random.choice(['Talla incorrecta', 'Talla incorrecta', 'Talla incorrecta', 'Defecto', 'No convence'])
        elif precio > 100:
            motivo = random.choice(['No convence', 'Color diferente', 'Defecto'])
        else:
            motivo = random.choice(motivos)
        
        cursor.execute("""
            INSERT INTO devoluciones (ticket_id, producto_id, cantidad, fecha, motivo)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            ticket_id,
            producto_id,
            random.randint(1, 3),
            fake.date_between(start_date="-3y", end_date="today"),
            motivo if random.random() > 0.1 else None
        ))
    print(f"{len(tickets_con_devolucion)} devoluciones generadas")

def main():
    print("Regenerando devoluciones...")
    
    # CONEXIÓN
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    engine = conectar()
    
    # VACIAR TABLAS
    cursor.execute("TRUNCATE TABLE devoluciones")
    cursor.execute("TRUNCATE TABLE devoluciones_clean")
    conn.commit()
    print("Tablas vaciadas")
    
    # LEER DATOS EXISTENTES
    tickets_df = pd.read_sql("SELECT id FROM tickets", engine)
    ticket_ids = tickets_df['id'].tolist()
    productos_df = pd.read_sql("SELECT id, talla, precio_venta FROM productos", engine)
    
    # REGENERAR DEVOLUCIONES
    generar_devoluciones(cursor, ticket_ids, productos_df)
    conn.commit()
    
    # LIMPIAR Y ACTUALIZAR DEVOLUCIONES_CLEAN
    from clean_db import limpiar_tabla, guardar_tabla_clean
    df_limpio = limpiar_tabla(engine, "devoluciones")
    guardar_tabla_clean(engine, df_limpio, "devoluciones")
    
    cursor.close()
    conn.close()
    print("Devoluciones regeneradas correctamente")

if __name__ == "__main__":
    main()