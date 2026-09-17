"""
Script: src/simular_categorias.py
Historia de usuario: E4-CAT-F01
Título: Simular 250 filas de `categorias` con Faker y ensuciarlas a proposito.
"""

import random
import uuid
import pandas as pd
from faker import Faker

# Inicializar Faker con localización colombiana y sembrar semillas para reproducibilidad
fake = Faker("es_CO")
Faker.seed(42)
fake.seed_instance(42)
random.seed(42)

# -----------------------------------------------------------------------------
# Constantes exigidas por la historia Kaizen
# -----------------------------------------------------------------------------
CATEGORIAS = [
    "Logística",
    "Tecnología",
    "Operaciones",
    "Gestión Humana",
    "Calidad",
    "Finanzas",
    "Sostenibilidad",
    "Servicio al Cliente",
    "Innovación",
    "Seguridad y Salud",
]

# OJO: area_responsable NO esta en el modelo de Backend II:
# es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar.
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
    "Dirección General",
]


def _ensuciar_nombre(nombre: str) -> str:
    """
    Genera variantes de escritura para ensuciar el nombre de la categoría:
    mayúsculas, minúsculas, espacios sobrantes y versiones sin tildes.
    Ejemplo: 'Logística' -> 'Logistica', 'LOGISTICA', ' logistica ', 'logística'.
    """
    sin_tilde = (
        nombre.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
    )
    variantes = [
        nombre,
        sin_tilde,
        nombre.upper(),
        sin_tilde.upper(),
        nombre.lower(),
        sin_tilde.lower(),
        f" {nombre} ",
        f" {sin_tilde.lower()} ",
        f"  {nombre}",
        f"{sin_tilde}  ",
    ]
    return random.choice(variantes)


def generar_categorias(n: int = 250) -> pd.DataFrame:
    """
    Genera un DataFrame con n filas simuladas de la tabla categorias,
    ensuciadas a proposito segun los criterios de aceptacion de Kaizen:
      - id: UUID como texto (str(uuid.uuid4())).
      - nombre: categorias elegidas al azar con variantes de escritura.
      - descripcion: frases falsas de 8 palabras, con 15% de valores nulos (None).
      - area_responsable: area elegida al azar, con 10% de valores nulos (None).
      - 8% de filas duplicadas tal cual (duplicados exactos).

    Retorna el DataFrame listo para analisis o posterior exportacion.
    """
    # Fijar semillas para asegurar reproducibilidad exacta
    Faker.seed(42)
    fake.seed_instance(42)
    random.seed(42)

    # 8% de las filas repetidas tal cual (duplicados exactos)
    num_duplicados = int(n * 0.08)
    num_base = n - num_duplicados

    # Generacion de filas base con columnas requeridas
    filas = []
    for _ in range(num_base):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": _ensuciar_nombre(random.choice(CATEGORIAS)),
            "descripcion": fake.sentence(nb_words=8),
            # OJO: area_responsable NO esta en el modelo de Backend II:
            # es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar.
            "area_responsable": random.choice(AREAS),
        })

    # Seleccion de indices a duplicar (pares exactos) e indices unicos
    indices_a_duplicar = random.sample(range(num_base), k=num_duplicados)
    indices_unicos = [i for i in range(num_base) if i not in set(indices_a_duplicar)]

    # Se ensucia descripcion: 15% en None (nulos)
    target_desc_nulls = int(round(n * 0.15))
    pares_desc_nulls = int(round(num_duplicados * 0.15))
    unicos_desc_nulls = target_desc_nulls - (2 * pares_desc_nulls)
    indices_desc_pares = random.sample(indices_a_duplicar, k=pares_desc_nulls)
    indices_desc_unicos = random.sample(indices_unicos, k=unicos_desc_nulls)
    for idx in set(indices_desc_pares + indices_desc_unicos):
        filas[idx]["descripcion"] = None

    # Se ensucia area_responsable: 10% en None (nulos)
    target_area_nulls = int(round(n * 0.10))
    pares_area_nulls = int(round(num_duplicados * 0.10))
    unicos_area_nulls = target_area_nulls - (2 * pares_area_nulls)
    indices_area_pares = random.sample(indices_a_duplicar, k=pares_area_nulls)
    indices_area_unicos = random.sample(indices_unicos, k=unicos_area_nulls)
    for idx in set(indices_area_pares + indices_area_unicos):
        filas[idx]["area_responsable"] = None

    # Duplicados exactos tal cual (8% de filas)
    duplicados = [filas[i].copy() for i in indices_a_duplicar]
    filas.extend(duplicados)

    # Mezclar orden de forma reproducible
    random.shuffle(filas)

    df = pd.DataFrame(filas)
    return df


if __name__ == "__main__":
    df = generar_categorias()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
