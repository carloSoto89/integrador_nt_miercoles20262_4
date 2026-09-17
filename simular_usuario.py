import random
import uuid
from faker import Faker

# 1. Escoger el país y el lenguaje para simular los datos
fake = Faker("es_CO")

# 2. Sembrar semillas
Faker.seed(42)
random.seed(42)

# -----------------------------------------------------------------------------
# Constantes exigidas por Kaizen
# -----------------------------------------------------------------------------
CATEGORIAS = [
    "Innovación y Transformación Digital",
    "Optimización de Procesos",
    "Sostenibilidad Ambiental",
    "Seguridad y Salud en el Trabajo",
    "Calidad y Reducción de Desperdicios",
    "Experiencia del Cliente",
    "Logística y Cadena de Suministro",
    "Cultura Organizacional",
    "Ciberseguridad y Datos",
    "Eficiencia Energética",
]

# OJO: area_responsable NO está en el modelo de Backend II:
# es una columna EXTRA solo para este ejercicio de análisis, para poder agrupar.
AREAS = [
    "Operaciones",
    "Tecnología",
    "Gestión Humana",
    "Logística",
    "Calidad",
    "Servicio al Cliente",
    "Finanzas",
    "Seguridad Ocupacional",
    "Sostenibilidad",
]

# 3. Definir el dato y su tipo a simular
# Se generan 250 filas con estas columnas: id (texto (UUID)), nombre (texto), descripcion (texto), area_responsable (texto).

# 4. Definir el número de datos simulados (DATASET)
FILAS = 250

# 5. Iterar y guardar
filas = []
for _ in range(FILAS):
    filas.append({
        "id": str(uuid.uuid4()),
        "nombre": random.choice(CATEGORIAS),
        "descripcion": fake.sentence(nb_words=8),
        "area_responsable": random.choice(AREAS),
    })

print(f"Total de registros generados: {len(filas)}")
print("Ejemplo de las primeras 3 filas:")
for f in filas[:3]:
    print(f)
