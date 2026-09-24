import random
import uuid
from faker import Faker

# 1. Escoger el país y el lenguaje para simular los datos
fake = Faker("es_CO")

# 2. Sembrar semillas
Faker.seed(42)
random.seed(42)

# Constantes exigidas al inicio por los criterios de aceptación
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
# id (texto (UUID))
# nombre (texto)
# descripcion (texto)
# area_responsable (texto)

# 4. Definir el numero de datos simulados (DATASET)
FILAS = 250

# 5. Construir funcion generadora de datos
def generar_datos_categorias(numero_registros=FILAS):
    filas = []
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": random.choice(CATEGORIAS),
            "descripcion": fake.sentence(nb_words=8),
            # OJO: area_responsable NO está en el modelo de Backend II:
            # es una columna EXTRA solo para este ejercicio de análisis, para poder agrupar.
            "area_responsable": random.choice(AREAS),
        })
    return filas


# Alias para compatibilidad
generar_categorias = generar_datos_categorias


if __name__ == "__main__":
    datos = generar_datos_categorias()
    print(f"Total de registros generados: {len(datos)}")
    print("Ejemplo de las primeras 3 filas:")
    for f in datos[:3]:
        print(f)
