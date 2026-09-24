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
#Correo (texto)
#contrasena_hash (texto)
#rol (texto)******
#activo (booleano)
#fecha (fecha y hora)

#4 Definir el numero de datos simulados(DATASET)
FILAS=400