import random
import uuid
import pandas as pd

from faker import Faker

#1 Escoger el pais y el lenguaje para simular los datos
fake=Faker("es_CO")

#2 Sembrar semillas
Faker.seed(42)
random.seed(42)

#Definir 

#id (texto (UUID))
#fecha_registro (fecha y hora)
#observacion (texto)
#estado (texto)***
#id_usuario (texto (UUID))
#id_reto (texto (UUID)).

#4 Definir el numero de datos simulados(DATASET)
FILAS=800
ESTADOS=["activo","inactivo","pendiente"]

#Construir funcion generadora de datos

def generar_datos_registros(numero_registros=FILAS):

    filas=[]

    for _ in range(numero_registros):
        filas.append({
            "id":str(uuid.uuid4()),
            "fecha_registro":fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion":fake.sentence(nb_words=10),
            "estado":random.choice(ESTADOS),
            "id_usuario":random.choice(IDS_USUARIO),
            "id_reto":random.choice(IDS_RETO),
        })
    return filas

import random
import pandas as pd

def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 999)).index

def escribir_mal(texto):
    return random.choice([texto.lower(), texto.upper(), f" {texto} "])

def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # 20% de `observacion` en nulos
    idx = generar_muestra(datos_df, 0.20)
    datos_df.loc[idx, "observacion"] = None

    # 5% de `estado` con variantes mal escritas
    idx = generar_muestra(datos_df, 0.05)
    datos_df.loc[idx, "estado"] = datos_df.loc[idx, "estado"].map(escribir_mal)

    # 40% de `fecha_registro` en formato latino
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"] = iso
    idx = generar_muestra(datos_df, 0.40)
    datos_df.loc[idx, "fecha_registro"] = latino.loc[idx]

    # 10% con el par id_usuario + id_reto repetido (inscripción doble)
    idx = generar_muestra(datos_df, 0.10)
    repetidas = datos_df.loc[idx].copy()
    # aquí, si tienes una columna id propia (ej. id_inscripcion), dale un valor nuevo
    datos_df = pd.concat([datos_df, repetidas], ignore_index=True)

    # 5% de duplicados exactos (hazlo AL FINAL para que la copia sea idéntica)
    idx = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[idx]], ignore_index=True)

    return datos_df

