import random
import uuid

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
