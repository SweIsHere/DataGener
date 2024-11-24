from faker import Faker
import csv

# Crear instancia de Faker
fake = Faker()

# Configurar cantidad de datos y archivo de salida
num_records = 2_000_000  # Generar 1 millón de registros
output_file = 'user_data_2m.csv'

# Usar un conjunto para garantizar unicidad de usernames
unique_usernames = set()

# Escribir directamente en el archivo para optimizar memoria
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['username', 'nombre', 'email', 'fecha_registro'])

    # Incluir cabeceras
    writer.writeheader()

    while len(unique_usernames) < num_records:
        base_username = fake.user_name()
        username = base_username

        # Agregar sufijo numérico si el nombre ya existe
        suffix = 1
        while username in unique_usernames:
            username = f"{base_username}{suffix}"
            suffix += 1

        unique_usernames.add(username)
        writer.writerow({
            'username': username,
            'nombre': fake.name(),
            'email': fake.email(),
            'fecha_registro': fake.date()
        })

print(f"{num_records} registros únicos escritos en {output_file}.")
