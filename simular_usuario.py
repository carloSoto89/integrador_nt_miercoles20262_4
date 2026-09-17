import random
import uuid

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