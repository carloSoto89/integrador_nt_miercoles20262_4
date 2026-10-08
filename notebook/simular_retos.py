import random
import uuid
import pandas as pd

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

# Utilizamos PANDAS para ordenar los datos simulados en un DATAFRAME
tabla_ordenada_usuarios=pd.DataFrame(generar_datos_usuarios())

#7. Ensuciar los datos

#7.1 Generar una funcion que muestre los datos
def  generar_muestra(datos,porcentaje):
    return datos.sample(fraccion=porcentaje,random_state=random.randint(0,9999)).index

#7.2 Funcion que ensucia los datos
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    #para el atributo nombre generar el 10% con espacios sobrantes
    subconjunto_datos=generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"]=" "+datos_df.loc[subconjunto_datos,"nombre"]+" "

    #Para el atributo descripcion necesito el 12% de los datos en None
    subconjunto_datos=generar_muestra(datos_df,0.12)
    datos_df.loc[subconjunto_datos,"descripcion"]=None

     # Para el atributo fecha_registro: dos formatos mezclados ("2026-03-15 14:30:00" y "15/03/2026 14:30")
     # (si tu fecha es solo fecha, sin hora, usa "%Y-%m-%d" y "%d/%m/%Y")

    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")               
        latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")              
        datos_df["fecha_registro"] = iso                                               
        filas_elegidas = generar_muestra(datos_df, 0.40)
        datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas] 