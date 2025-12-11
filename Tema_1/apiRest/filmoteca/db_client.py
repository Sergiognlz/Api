# db.py
from pymongo import MongoClient

# Cliente de MongoDB (localhost:27017 por defecto)
db_client = MongoClient()

# Base de datos
database = db_client["cine_db"]

# Colecciones
directores_collection = database["directores"]
peliculas_collection = database["peliculas"]

