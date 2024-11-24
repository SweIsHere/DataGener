import pandas as pd
import csv
import random
from faker import Faker

# Crear instancia de Faker
fake = Faker()

# Rutas de los archivos
inventario_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\inventario.csv"
producto_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\producto.csv"
comprador_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\comprador.csv"
output_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\venta.csv"

# Leer los CSVs de Inventario, Producto y Comprador
inventario_df = pd.read_csv(inventario_path, usecols=["producto_id", "vendedor_username", "cantidad"])
producto_df = pd.read_csv(producto_path, usecols=["id", "precio"])
comprador_df = pd.read_csv(comprador_path, usecols=["username"])

# Combinar las dos fuentes en base a Producto_ID
inventario_df = inventario_df.rename(columns={"producto_id": "id"})
merged_df = pd.merge(inventario_df, producto_df, on="id")

# Configurar parámetros
num_records = 1_200_000  # Número de registros a generar
chunk_size = 50_000  # Tamaño del bloque para escritura en buffer

# Obtener lista de compradores
compradores = comprador_df["username"].tolist()

# Crear un diccionario para simular el inventario dinámico
dynamic_inventory = merged_df.set_index(["vendedor_username", "id"])["cantidad"].to_dict()

# Para evitar duplicados
generated_keys = set()

# Escribir directamente al archivo para optimizar memoria
with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Comprador_Username", "Vendedor_Username", "Producto_ID", "fecha", "importe", "cantidad"])
    writer.writeheader()

    buffer = []  # Usar un buffer para acumular datos antes de escribir
    i = 0  # Índice inicial en el inventario

    while len(generated_keys) < num_records:
        # Incrementar el índice al azar (simulando el salto)
        jump = random.randint(1, 10)
        i = (i + jump) % len(merged_df)  # Saltar aleatoriamente dentro de los índices

        row = merged_df.iloc[i]

        # Datos de inventario y producto
        vendedor_username = row["vendedor_username"]
        producto_id = row["id"]
        precio = row["precio"]

        # Verificar el inventario dinámico
        current_stock = dynamic_inventory.get((vendedor_username, producto_id), 0)
        if current_stock <= 0:
            continue  # Saltar si no hay stock

        # Seleccionar aleatoriamente un comprador
        comprador_username = random.choice(compradores)

        # Generar una cantidad aleatoria respetando el stock disponible
        cantidad = random.randint(1, current_stock)

        # Calcular el importe
        importe = round(precio * cantidad, 2)

        # Generar una fecha aleatoria
        fecha = fake.date_between(start_date='-1y', end_date='today')

        # Crear una clave única para evitar duplicados
        key = (comprador_username, vendedor_username, producto_id)
        if key in generated_keys:
            continue  # Saltar si ya se generó esta combinación

        # Actualizar el inventario dinámico
        dynamic_inventory[(vendedor_username, producto_id)] -= cantidad

        # Agregar la clave al conjunto de generados
        generated_keys.add(key)

        # Agregar registro al buffer
        buffer.append({
            "Comprador_Username": comprador_username,
            "Vendedor_Username": vendedor_username,
            "Producto_ID": producto_id,
            "fecha": fecha,
            "importe": importe,
            "cantidad": cantidad
        })

        # Escribir el buffer al archivo en bloques
        if len(buffer) >= chunk_size:
            writer.writerows(buffer)
            buffer = []

    # Escribir cualquier dato restante en el buffer
    if buffer:
        writer.writerows(buffer)

print(f"Archivo CSV generado con éxito: {output_path}")
