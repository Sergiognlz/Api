from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Crear la aplicación de FastAPI
app=FastAPI()

# Definición del modelo Autor
class Autor(BaseModel):
    id:int
    dni:str
    nombre:str
    apellidos:str

# Lista de autores de ejemplo
lista_autores= [
        Autor(id=1, dni="12345678A", nombre="H.P.", apellidos="Loveftcraft"),
        Autor(id=2, dni="12345678B", nombre="Frank Belknap", apellidos="Long"),
        Autor(id=3, dni="12345678C", nombre="Clark Ashton", apellidos="Smith"),
        Autor(id=4, dni="12345678D", nombre="Robert E.", apellidos="Howard"),
        Autor(id=5, dni="12345678E", nombre="Robert", apellidos="Bloch")
         
]

# Endpoint para obtener la lista de autores
@app.get("/autores")
def Autores():
    return lista_autores

# Endpoint para obtener un autor por su ID
@app.get("/autores/{id_autor}")
def get_autor(id_autor:int):
    autores=[autor for autor in lista_autores if autor.id==id_autor]

    return autores[0] if autores else {"error":"Autor no encontrado"}

# Autor por query 
@app.get("/autor/")
def get_autor_query(id_autor:int):
    autores=[autor for autor in lista_autores if autor.id==id_autor]

    return autores[0] if autores else {"error":"Autor no encontrado"}
