import pandas as pd
from faker import Faker
import random

# Configurar Faker
fake = Faker()

# Ruta del archivo CSV
csv_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\user_data_2m.csv"


# Leer solo las primeras 1000000 filas del archivo CSV
usuarios_df = pd.read_csv(csv_path, usecols=["username"], nrows=1000000)
usuarios = usuarios_df["username"].tolist()  # Obtener los primeros 1000000 usernames



"""
# Leer la cabecera y luego omitir filas a partir de la 1001 (sin perder la cabecera)
usuarios_df = pd.read_csv(csv_path, usecols=["username"], skiprows=range(1, 1001), header=0)
usuarios = usuarios_df["username"].tolist()  # Obtener los usernames desde la fila 1001
"""

# Lista para almacenar los registros generados para Vendedor
vendedores = []

# Generar registros para la tabla Vendedor
for username in usuarios:
    vendedor = {
        "Username": username,
        "Verificado": random.choice([True, False]),
        "Valoracion": round(random.uniform(1.0, 5.0), 2),  # Generar valoración entre 1.0 y 5.0
    }
    vendedores.append(vendedor)

# Convertir la lista de vendedores a un DataFrame
vendedores_df = pd.DataFrame(vendedores)

# Exportar los registros generados a un archivo CSV
output_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\vendedores1m.csv"
vendedores_df.to_csv(output_path, index=False)

print(f"1000 000 registros generados y guardados en: {output_path}")
