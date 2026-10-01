import random
import uuid
import pandas as pd
from faker import Faker

#1 escoger el pais y lenguaje para simular los datos 
fake = Faker('es_CO')

#2 Sembrar semilla para generar datos aleatorios consistentes
Faker.seed(42)
random.seed(42)

#Constantes exigidas al inicio por los criterios de aceptación
#Solo hay 10 categorias reales, pero se generan 250 filas: la gracia es que el catalogo llega REPETIDO y con variantes de escritura
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

#3 Definir el dato y su tipo a simular 
#id (texto (UUID)),
#nombre (texto),
#descripcion (texto),
#area_responsable (texto)

#4 Definir el número de datos simulados (DATASET)
FILAS = 250

#5 Construir funcion generadora de datos 
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


#6. Utilizaremos PANDAS para ordenar los datos simulados en un DATAFRAME osea una tabla ordenada
tabla_ordenada_categorias = pd.DataFrame(generar_datos_categorias())


#7. Ensuciar los datos 
#7.1 Generar una función que muestre los datos 
def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index


#7.2 Función que encucia los datos 
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    #Para el atributo nombre: variantes del mismo nombre: 'Logistica', 'LOGISTICA', ' logistica ', 'logística'
    def escribir_mal(texto):
        sin_tilde = (
            texto.replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
        )
        variantes = [
            sin_tilde.capitalize(),  # 'Logistica'
            texto.upper(),           # 'LOGISTICA'
            f" {texto.lower()} ",    # ' logistica '
            texto.lower(),           # 'logística'
        ]
        return random.choice(variantes)

    subconjunto_datos = generar_muestra(datos_df, 0.50)
    datos_df.loc[subconjunto_datos, "nombre"] = datos_df.loc[subconjunto_datos, "nombre"].map(escribir_mal)

    #Para el atributo descripcion: 15% en None (nulos)
    subconjunto_datos = generar_muestra(datos_df, 0.15)
    datos_df.loc[subconjunto_datos, "descripcion"] = None

    #Para el atributo area_responsable: 10% en None
    subconjunto_datos = generar_muestra(datos_df, 0.10)
    datos_df.loc[subconjunto_datos, "area_responsable"] = None

    #Para el 8% de las filas repetidas tal cual (duplicados exactos)
    filas_elegidas = generar_muestra(datos_df, 0.08)
    filas_a_copiar = datos_df.drop(index=filas_elegidas).sample(n=len(filas_elegidas), random_state=random.randint(0, 9999)).index
    datos_df.loc[filas_elegidas] = datos_df.loc[filas_a_copiar].values

    return datos_df


#7.3 Ejecutar el ensuciado de datos
tabla_categorias_sucias = ensuciar(tabla_ordenada_categorias)
