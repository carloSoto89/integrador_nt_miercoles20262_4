import random
import uuid

from faker import Faker

#1 Escoger el pais y el lenguaje para simular los datos
fake=Faker("es_CO")

#2 Sembrar semillas
Faker.seed(42)
random.seed(42)

# Definir el dato y su tipo a simular
#id (texto (UUID)),
# nombre (texto),
# descripcion (texto),
# fecha_inicio
#fecha_fin (fecha),
# estado (*****),
# id_empresa  (texto (UUID)),
# id_categoria (texto (UUID)),
# id_prioridad (texto (UUID)),

#4 Definir el numero de datos simulados(DATASET)
FILAS=500

ESTADOS=["activo","inactivo","pendiente"]

#5Construir funcion generadora de datos

def generar_datos_usuarios(numero_registros=FILAS):

    filas = []

    for _ in range(numero_registros):

        fecha_inicio = fake.date_between(
            start_date="-1y",
            end_date="+3m"
        )

        fecha_fin = fecha_inicio + timedelta(
            days=random.randint(15, 180)
        )

        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=6).rstrip("."),
            "descripcion": fake.sentence(nb_words=12),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "estado": random.choice(ESTADO),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categorias": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD),
        })

    return filas