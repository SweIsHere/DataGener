import pandas as pd
import random
from faker import Faker

# Configurar Faker
fake_generators = {
    country: Faker(locale) for country, locale in {
        # América del Norte
        "United States": "en_US",
        "Canada": "en_CA",
        "Mexico": "es_MX",

        # América Latina
        "Argentina": "es_AR",
        "Brazil": "pt_BR",
        "Chile": "es_CL",
        "Colombia": "es_CO",
        "Peru": "es_ES",  # Español genérico
        "Uruguay": "es_ES",  # Español genérico
        "Ecuador": "es_ES",  # Español genérico
        "Bolivia": "es_ES",  # Español genérico

        # Europa Occidental
        "Spain": "es_ES",
        "France": "fr_FR",
        "Germany": "de_DE",
        "Italy": "it_IT",
        "United Kingdom": "en_GB",

        # Europa del Este y Rusia
        "Russia": "ru_RU",
        "Poland": "pl_PL",

        # Países Nórdicos
        "Sweden": "sv_SE",
        "Norway": "no_NO",
        "Denmark": "da_DK",
        "Finland": "fi_FI",

        # Asia
        "China": "zh_CN",
        "India": "en_IN",
        "Japan": "ja_JP",
        "South Korea": "ko_KR",

        # Oceanía
        "New Zealand": "en_NZ",
        "Australia": "en_AU",
    }.items()
}

# Ruta del archivo CSV
csv_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\user_data_2m.csv"

# Leer la cabecera y luego omitir filas a partir de la 1000001
usuarios_df = pd.read_csv(csv_path, usecols=["username"], skiprows=range(1, 1000001), header=0)
usuarios = usuarios_df["username"].tolist()

# Generar países y direcciones
compradores = []
for username in usuarios:
    pais = random.choice(list(fake_generators.keys()))
    fake = fake_generators[pais]
    compradores.append({
        "Username": username,
        "Direccion_Envio": fake.address().replace("\n", ", "),
        "Pais": pais,
    })

# Convertir los datos a un DataFrame
compradores_df = pd.DataFrame(compradores)

# Exportar a un archivo CSV
output_path = r"C:\Users\tokio\OneDrive\Escritorio\faker\compradores1m.csv"
compradores_df.to_csv(output_path, index=False)

print(f"Registros generados para la tabla Comprador y guardados en: {output_path}")
