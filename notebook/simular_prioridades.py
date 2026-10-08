import os
import random
import uuid
import pandas as pd
from faker import Faker

# 1. Escoger el país y lenguaje para simular los datos
fake = Faker('es_CO')

# 2. Sembrar semilla para generar datos aleatorios consistentes
Faker.seed(42)
random.seed(42)

# 3. Definir variables y constantes
Filas = 200
NIVELES = ["Alto", "Medio", "Bajo"]

# 5. Construir función generadora de datos de prioridades
def generar_datos_prioridades(numero_registros=Filas):
    filas = []
    for i in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.name(),
            "nivel": random.randint(1, 5),
            "dias_max_respuesta": random.randint(1, 30)
        })
    return filas

# 6. Crear el DataFrame con Pandas
tabla_ordenada_prioridades = pd.DataFrame(generar_datos_prioridades(Filas))

# 7. Ensuciar los datos
def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # A. Ensuciar 'nombre': mayúsculas, minúsculas con espacios, o tipo título
    def ensuciar_nombre_variantes(texto):
        variantes = [texto.upper(), f" {texto.lower()} ", texto.capitalize()]
        return random.choice(variantes)

    subconjunto_nombres = generar_muestra(datos_df, 0.25)
    datos_df.loc[subconjunto_nombres, "nombre"] = datos_df.loc[subconjunto_nombres, "nombre"].map(ensuciar_nombre_variantes)

    # B. Ensuciar 'nivel': convertir a palabra y 7% en None
    mapa_palabras = {1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco"}

    subconjunto_palabras = generar_muestra(datos_df, 0.15)
    datos_df.loc[subconjunto_palabras, "nivel"] = datos_df.loc[subconjunto_palabras, "nivel"].map(
        lambda x: mapa_palabras.get(x, str(x))
    )

    subconjunto_nulos_nivel = generar_muestra(datos_df, 0.07)
    datos_df.loc[subconjunto_nulos_nivel, "nivel"] = None

    # C. Ensuciar 'dias_max_respuesta': 5% en None y 3% valor absurdo (999)
    subconjunto_nulos_dias = generar_muestra(datos_df, 0.05)
    datos_df.loc[subconjunto_nulos_dias, "dias_max_respuesta"] = None

    subconjunto_absurdos = generar_muestra(datos_df, 0.03)
    datos_df.loc[subconjunto_absurdos, "dias_max_respuesta"] = 999

    # D. Duplicados exactos (8%)
    subconjunto_duplicados = generar_muestra(datos_df, 0.08)
    filas_duplicadas = datos_df.loc[subconjunto_duplicados].copy()
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    return datos_df

# =============================================================================
# EJECUCIÓN Y EXPORTACIÓN DEL ARCHIVO RAW
# =============================================================================
if __name__ == "__main__":
    tabla_prioridades_sucia = ensuciar(tabla_ordenada_prioridades)
    
    print("--- MUESTRA DE DATOS ENSUCIADOS DE PRIORIDADES ---")
    print(tabla_prioridades_sucia.head(15))
    
    os.makedirs('data', exist_ok=True)
    ruta_salida = 'data/prioridades_raw.csv'
    tabla_prioridades_sucia.to_csv(ruta_salida, index=False, encoding='utf-8')
    
    print(f"\n✅ Archivo generado exitosamente en: '{ruta_salida}'")
    print(f"📊 Registros totales exportados (con duplicados): {len(tabla_prioridades_sucia)}")