import pandas as pd
import csv
from faker import Faker
import random

# Crear instancia de Faker
fake = Faker()

# Rutas de los archivos
venta_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\venta.csv"
output_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\resena_publicada.csv"

# Leer el archivo de Venta
venta_df = pd.read_csv(venta_path, usecols=["Comprador_Username", "Vendedor_Username", "Producto_ID", "fecha"])

# Escribir directamente al archivo para optimizar memoria
with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Vendedor_Username", "Comprador_Username", "Producto_ID", "FechaPublicada", "comentario", "puntuacion"])
    writer.writeheader()

    buffer = []  # Usar un buffer para acumular datos antes de escribir

    for _, row in venta_df.iterrows():
        # Generar datos para ResenaPublicada
        vendedor_username = row["Vendedor_Username"]
        comprador_username = row["Comprador_Username"]
        producto_id = row["Producto_ID"]

        # Generar una fecha aleatoria después de la fecha de venta
        fecha_venta = pd.to_datetime(row["fecha"]).date()
        fecha_actual = pd.to_datetime("today").date()

        # Asegurar un rango válido
        fecha_publicada = fake.date_between_dates(
            date_start=min(fecha_venta, fecha_actual),  # Fecha mínima válida
            date_end=fecha_actual                      # Fecha máxima válida
        )

        # Generar comentario y puntuación
        comentario = fake.sentence(nb_words=12)
        puntuacion = random.randint(0, 5)

        # Agregar registro al buffer
        buffer.append({
            "Vendedor_Username": vendedor_username,
            "Comprador_Username": comprador_username,
            "Producto_ID": producto_id,
            "FechaPublicada": fecha_publicada,
            "comentario": comentario,
            "puntuacion": puntuacion
        })

        # Escribir el buffer al archivo en bloques
        if len(buffer) >= 50_000:  # Tamaño del bloque para escritura
            writer.writerows(buffer)
            buffer = []

    # Escribir cualquier dato restante en el buffer
    if buffer:
        writer.writerows(buffer)

print(f"Archivo CSV generado con éxito: {output_path}")
