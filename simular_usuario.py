import random
import uuid
import pandas as pd

from faker import Faker 

#1 escoger el pais y lenguaje para simular los datos 
fake=Faker('es_CO') #es_CO para Colombia, es_ES para España, es_MX para México, es_AR para Argentina, es_PE para Perú, es_CL para Chile, es_VE para Venezuela, es_EC para Ecuador, es_GT para Guatemala, es_CR para Costa Rica, es_PA para Panamá, es_DO para República Dominicana, es_UY para Uruguay, es_PY para Paraguay, es_BO para Bolivia, es_SV para El Salvador, es_HN para Honduras, es_NI para Nicaragua

#2 Sembrar semilla para generar datos aleatorios consistentes
Faker.seed(42)
random.seed(42)

#3 Definir el dato y su tipo a simular 
#id (texto (UUID)),
#nombre (texto),
#correo (texto), 
#contraseña_hash (texto),
#rol(texto),
#activo(booleano),
#fecha_registro (fecha y hora)

#4 Definir el número de datos simulados (DATASET)
Filas=200

ROLES=["administrador","empresario","profesor"]

#5 Construir funcion generadora de datos 
def generar_datos_usuarios(numero_registros=Filas):
    
    filas=[]
    for i in range(numero_registros):
        filas.append({
            "id":str(uuid.uuid4()),
            "nombre":fake.name(),
            "correo":fake.email(),
            "contraseña_hash":fake.sha256(),
            "rol":random.choice(ROLES),
            "activo":random.choice([True,False]),
            "fecha_registro":fake.date_time_between(start_date="-2y", end_date="now")
        })
    return filas


#6. Utilizaremos PANDAS para ordenar los datos simulados en un DATAFRAME osea una tabla ordenada
tabla_ordenada_usuarios=pd.DataFrame(generar_datos_usuarios())


#7. Ensuciar los datos 
#7.1 Generar una función que muestre los datos 
def generar_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje,random_state=random.randint(0,9999)).index


#7.2 Función que encucia los datos 
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    #Para el atributo nombre generar el 10% con espacios sobrantes 
    subconjunto_datos=generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"]=datos_df.loc[subconjunto_datos,"nombre"]+" "

    #para el atributo nombre generar el 8% en MAYUSCULA
    subconjunto_datos=generar_muestra(datos_df,0.08)
    datos_df.loc[subconjunto_datos,"nombre"]=datos_df.loc[subconjunto_datos,"nombre"].str.upper()

    #Para el atributo correo necesito el 12% de los datos en MAYUSCULA
    subconjunto_datos=generar_muestra(datos_df,0.12)
    datos_df.loc[subconjunto_datos,"correo"]=datos_df.loc[subconjunto_datos,"correo"].str.upper()

    #Para el atributo correo necesito el 5% de los datos sin @
    subconjunto_datos=generar_muestra(datos_df,0.05)
    datos_df.loc[subconjunto_datos,"correo"]=datos_df.loc[subconjunto_datos,"correo"].str.replace("@","", regex=False)

    #Para el atributo correo necesito el 4% de los datos en None
    subconjunto_datos=generar_muestra(datos_df,0.04)
    datos_df.loc[subconjunto_datos,"correo"]=None

    #Para el atributo rol para la palabra administrador y las otras generar variantes de escritura (Mayusculas, capital, espaciado)
    def escribir_mal(texto):
        variantes=[texto.lower(), f" {texto.title()} ", texto.capitalize()]
        return random.choice(variantes)

    subconjunto_datos=generar_muestra(datos_df,0.15)
    datos_df.loc[subconjunto_datos,"rol"]=datos_df.loc[subconjunto_datos,"rol"].map(escribir_mal)

    # Para el atributo fecha_registro: dos formatos mezclados ("2026-03-15 14:30:00" y "15/03/2026 14:30")
    # (si tu fecha es solo fecha, sin hora, usa "%Y-%m-%d" y "%d/%m/%Y")
    datos_df["fecha_registro"] = pd.to_datetime(datos_df["fecha_registro"])
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")               
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")              
    datos_df["fecha_registro"] = iso                                               
    filas_elegidas = generar_muestra(datos_df, 0.40)
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas]    

    return datos_df


#7.3 Ejecutar el ensuciado de datos
tabla_usuarios_sucios=ensuciar(tabla_ordenada_usuarios)