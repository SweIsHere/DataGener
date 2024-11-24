import os
import csv
import random
import time
import uuid
from faker import Faker
import pandas as pd

# Crear instancia de Faker
faker = Faker()

# Configurar las rutas base y las carpetas
output_base = "output_data"
os.makedirs(output_base, exist_ok=True)

# Configurar las opciones de generación
record_options = {"1k": 1_000, "10k": 10_000, "100k": 100_000, "1M": 1_000_000}
selection = "1M"  # Cambiar a "1k", "100k", "1M" según necesidad
num_records = record_options.get(selection)

if not num_records:
    raise ValueError("Opción inválida seleccionada.")

# Crear carpeta para la selección
output_folder = os.path.join(output_base, selection)
os.makedirs(output_folder, exist_ok=True)

# Medir tiempo de inicio
start_time = time.time()

# Configurar Faker para compradores
locales = {
    "United States": "en_US", "Canada": "en_CA", "Mexico": "es_MX",
    "Argentina": "es_AR", "Brazil": "pt_BR", "Chile": "es_CL", "Colombia": "es_CO",
    "Peru": "es_ES", "Uruguay": "es_ES", "Ecuador": "es_ES", "Bolivia": "es_ES",
    "Spain": "es_ES", "France": "fr_FR", "Germany": "de_DE", "Italy": "it_IT",
    "United Kingdom": "en_GB", "Russia": "ru_RU", "Poland": "pl_PL",
    "Sweden": "sv_SE", "Norway": "no_NO", "Denmark": "da_DK", "Finland": "fi_FI",
    "China": "zh_CN", "India": "en_IN", "Japan": "ja_JP", "South Korea": "ko_KR",
    "New Zealand": "en_NZ", "Australia": "en_AU"
}
fake_generators = {country: Faker(locale) for country, locale in locales.items()}

# Funciones para generar datos
def generar_usuarios(num_records, output_folder):
    unique_usernames = set()
    usuarios_path = os.path.join(output_folder, "usuarios.csv")
    with open(usuarios_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "nombre", "email", "fecha_registro"])
        writer.writeheader()
        while len(unique_usernames) < num_records:
            username = faker.user_name()
            if username not in unique_usernames:
                unique_usernames.add(username)
                writer.writerow({
                    "username": username,
                    "nombre": faker.name(),
                    "email": faker.email(),
                    "fecha_registro": faker.date()
                })
    return list(unique_usernames)

def generar_vendedores(usuarios, output_folder):
    vendedores_path = os.path.join(output_folder, "vendedores.csv")
    with open(vendedores_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "verificado", "valoracion"])
        writer.writeheader()
        for username in usuarios:
            writer.writerow({
                "username": username,
                "verificado": random.choice([True, False]),
                "valoracion": round(random.uniform(1.0, 5.0), 2)
            })

def generar_compradores(usuarios, output_folder):
    compradores_path = os.path.join(output_folder, "compradores.csv")
    with open(compradores_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "direccion_envio", "pais"])
        writer.writeheader()
        for username in usuarios:
            pais = random.choice(list(fake_generators.keys()))
            fake = fake_generators[pais]
            writer.writerow({
                "username": username,
                "direccion_envio": fake.address().replace("\n", ", "),
                "pais": pais
            })

def generar_sets(num_records, output_folder):
    sets_path = os.path.join(output_folder, "sets.csv")
    with open(sets_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["nombre", "franquicia", "fecha_lanzamiento"])
        writer.writeheader()
        for _ in range(num_records // 10):
            writer.writerow({
                "nombre": f"{faker.word()} {faker.word()}",
                "franquicia": random.choice(["Pokemon", "Magic", "Yu-Gi-Oh"]),
                "fecha_lanzamiento": faker.date_between(start_date='-10y', end_date='today')
            })

def generar_productos(num_records, output_folder):
    productos_path = os.path.join(output_folder, "productos.csv")
    with open(productos_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "nombre", "precio", "categoria", "set_nombre"])
        writer.writeheader()
        for _ in range(num_records):
            writer.writerow({
                "id": str(uuid.uuid4())[:8],
                "nombre": faker.word(),
                "precio": round(random.uniform(1, 100), 2),
                "categoria": random.choice(["Carta", "Booster Box"]),
                "set_nombre": faker.word()
            })

def generar_inventario(num_records, output_folder, vendedores, productos):
    inventario_path = os.path.join(output_folder, "inventario.csv")
    with open(inventario_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["producto_id", "vendedor_username", "cantidad"])
        writer.writeheader()
        for _ in range(num_records):
            writer.writerow({
                "producto_id": random.choice(productos),
                "vendedor_username": random.choice(vendedores),
                "cantidad": random.randint(1, 30)
            })


def generar_ventas(num_records, output_folder, inventario_df, compradores):
    ventas_path = os.path.join(output_folder, "ventas.csv")
    dynamic_inventory = inventario_df.set_index(["vendedor_username", "producto_id"])["cantidad"].to_dict()

    with open(ventas_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["comprador_username", "vendedor_username", "producto_id", "fecha",
                                                  "importe", "cantidad"])
        writer.writeheader()

        for _ in range(num_records):
            # Filtrar productos disponibles
            available_products = {key: stock for key, stock in dynamic_inventory.items() if stock > 0}
            if not available_products:
                print("No hay más productos disponibles para vender.")
                break

            # Elegir un producto aleatoriamente
            vendedor, producto = random.choice(list(available_products.keys()))
            max_stock = dynamic_inventory[(vendedor, producto)]

            # Verificar si hay stock disponible
            if max_stock <= 0:
                continue  # Saltar si no hay stock

            # Generar cantidad y actualizar inventario dinámico
            cantidad = random.randint(1, max_stock)
            dynamic_inventory[(vendedor, producto)] -= cantidad

            # Generar registro de venta
            writer.writerow({
                "comprador_username": random.choice(compradores),
                "vendedor_username": vendedor,
                "producto_id": producto,
                "fecha": faker.date_between(start_date='-1y', end_date='today'),
                "importe": round(random.uniform(10, 500), 2),
                "cantidad": cantidad
            })
    print(f"Ventas generadas en: {ventas_path}")



def generar_resenas(num_records, output_folder, ventas_df):
    resenas_path = os.path.join(output_folder, "resenas.csv")
    ventas_df["fecha"] = pd.to_datetime(ventas_df["fecha"])
    with open(resenas_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Vendedor_Username", "Comprador_Username", "Producto_ID", "FechaPublicada", "comentario", "puntuacion"])
        writer.writeheader()
        for _, row in ventas_df.iterrows():
            writer.writerow({
                "Vendedor_Username": row["vendedor_username"],
                "Comprador_Username": row["comprador_username"],
                "Producto_ID": row["producto_id"],
                "FechaPublicada": faker.date_between(start_date=row["fecha"], end_date='today'),
                "comentario": faker.sentence(),
                "puntuacion": random.randint(1, 5)
            })



def generar_cartas(productos_df, output_folder):
    cartas_path = os.path.join(output_folder, "cartas.csv")
    with open(cartas_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["producto_id", "descripcion", "rareza", "estado"])
        writer.writeheader()

        for _, producto in productos_df[productos_df["categoria"] == "Carta"].iterrows():
            writer.writerow({
                "producto_id": producto["id"],
                "descripcion": faker.sentence(),
                "rareza": random.choice(["Common", "Uncommon", "Rare", "Special", "Promotional"]),
                "estado": random.choice(["Poor", "Played", "Light Played", "Good", "Excellent", "Mint"]),
            })
    print(f"Cartas generadas en: {cartas_path}")

def generar_boosterboxes(productos_df, output_folder):
    boosterboxes_path = os.path.join(output_folder, "boosterboxes.csv")
    with open(boosterboxes_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["producto_id", "descripcion", "cantidad_sobres", "edicion_especial"])
        writer.writeheader()

        for _, producto in productos_df[productos_df["categoria"] == "Booster Box"].iterrows():
            writer.writerow({
                "producto_id": producto["id"],
                "descripcion": faker.text(),
                "cantidad_sobres": random.randrange(12, 33, 2),
                "edicion_especial": random.choice([True, False]),
            })
    print(f"Booster Boxes generados en: {boosterboxes_path}")








# Generar datos
usuarios = generar_usuarios(num_records, output_folder)
generar_vendedores(usuarios, output_folder)
generar_compradores(usuarios, output_folder)
generar_sets(num_records, output_folder)
generar_productos(num_records, output_folder)




productos_df = pd.read_csv(os.path.join(output_folder, "productos.csv"))
productos = productos_df["id"].tolist()



generar_cartas(productos_df, output_folder)
generar_boosterboxes(productos_df, output_folder)




vendedores = usuarios[:len(usuarios) // 2]
generar_inventario(num_records, output_folder, vendedores, productos)

compradores = usuarios[len(usuarios) // 2:]
inventario_df = pd.read_csv(os.path.join(output_folder, "inventario.csv"))
generar_ventas(num_records, output_folder, inventario_df, compradores)

ventas_df = pd.read_csv(os.path.join(output_folder, "ventas.csv"))
generar_resenas(num_records, output_folder, ventas_df)

# Calcular tiempo final
end_time = time.time()
elapsed_time = (end_time - start_time) / 60
print(f"Generación completa. Tiempo total: {elapsed_time:.2f} minutos.")
