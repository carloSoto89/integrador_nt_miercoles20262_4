import random
import uuid

from faker import Faker

#1 Escoger el pais y el lenguaje para simular los datos
fake=Faker("es_CO")

#2 Sembrar semillas
Faker.seed(42)
random.seed(42)

#Definir 
#id (texto) (UUDI)
#nombre (texto)
#nit (texto)
#sector (texto)
#contacto (texto)
#Correo (texto)
#telefono (texto)
#activo (booleano)


#4 Definir el numero de datos simulados(DATASET)
FILAS=300

