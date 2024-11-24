import pandas as pd
import csv
import random

# Archivos de entrada y salida
vendedores_file = r"C:\Users\tokio\OneDrive\Escritorio\faker\vendedor.csv"
productos_file = r"C:\Users\tokio\OneDrive\Escritorio\BRENNER\producto\productos.csv"
output_file = r"C:\Users\tokio\OneDrive\Escritorio\faker\inventario.csv"

# Leer los vendedores y productos desde los CSV
vendedores_df = pd.read_csv(vendedores_file, usecols=["username"])
productos_df = pd.read_csv(productos_file, usecols=["ID"])

# Obtener listas de usernames y producto IDs
usernames = vendedores_df["username"].tolist()
producto_ids = productos_df["ID"].tolist()

# Configuración de escritura en bloques
block_size = 10000  # Escribir en bloques de 10,000 registros


# Generador para crear registros del inventario
def generar_inventario(producto_ids, usernames):
    for producto_id in producto_ids:
        yield {
            "Producto_ID": producto_id,
            "Vendedor_Username": random.choice(usernames),
            "Cantidad": random.randint(1, 30)
        }


# Escribir directamente en el archivo CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Producto_ID", "Vendedor_Username", "Cantidad"])
    writer.writeheader()

    # Procesar y escribir datos en bloques
    buffer = []
    for idx, registro in enumerate(generar_inventario(producto_ids, usernames), 1):
        buffer.append(registro)
        if idx % block_size == 0:  # Escribir en el archivo cada 10,000 registros
            writer.writerows(buffer)
            buffer = []  # Vaciar el buffer

    # Escribir cualquier registro restante en el buffer
    if buffer:
        writer.writerows(buffer)

print(f"Inventario generado con éxito en {output_file}")
