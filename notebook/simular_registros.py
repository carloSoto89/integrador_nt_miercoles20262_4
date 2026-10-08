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

    # Se ensucia `observacion`: 20% en None (nulos).
    idx = generar_muestra(datos_df, 0.20)
    datos_df.loc[idx, "observacion"] = None

    # Se ensucia `estado`: variantes: 'inscrito', 'EN PROCESO', ' Finalizado '.
    idx = generar_muestra(datos_df, 0.05)
    datos_df.loc[idx, "estado"] = datos_df.loc[idx, "estado"].map(escribir_mal)

    # Se ensucia `fecha_registro`: dos formatos mezclados: "2026-03-15 14:30:00" y "15/03/2026 14:30".
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"] = iso
    idx = generar_muestra(datos_df, 0.40)
    datos_df.loc[idx, "fecha_registro"] = latino.loc[idx]

    # 10% con el par `id_usuario` + `id_reto` REPETIDO: el mismo usuario inscrito dos veces en el mismo reto (eso el back lo prohibe con 409).
    idx = generar_muestra(datos_df, 0.10)
    repetidas = datos_df.loc[idx].copy()
    datos_df = pd.concat([datos_df, repetidas], ignore_index=True)

    #5% de las filas repetidas tal cual (duplicados exactos).
    idx = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[idx]], ignore_index=True)

    return datos_df

