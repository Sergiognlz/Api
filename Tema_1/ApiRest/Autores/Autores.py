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

# Endpoint para añadir un nuevo autor
@app.post("/autores", status_code=201, response_model=Autor)
def add_autor(autor:Autor):
    # Asignar un ID al nuevo autor
    autor.id=next_id()
    # Añadir el autor a la lista
    lista_autores.append(autor)
    # Devolver el autor añadido
    return autor

# Función para obtener el siguiente ID disponible
def next_id():
    # Si la lista no está vacía, obtener el máximo ID y sumarle 1
    if lista_autores:
        return max(autor.id for autor in lista_autores) + 1
    # Si la lista está vacía, empezar desde 1
    else:
        return 1
    
# Endpoint para modificar un autor existente
@app.put("/autores/{id_autor}", response_model=Autor)

def modify_autor(id_autor:int, autor: Autor):
    # Buscar el autor por su ID y modificarlo
    for index, saved_autor in enumerate(lista_autores):
        # Si se encuentra el autor, se actualiza la información
        if saved_autor.id==id_autor:
            # Actualizar los datos del autor
            autor.id=id_autor
            # Reemplazar el autor en la lista
            lista_autores[index]=autor
            # Devolver el autor modificado
            return autor
    # Si no se encuentra el autor, se lanza una excepción HTTP 404    
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# Endpoint para eliminar un autor por su ID
@app.delete("/autores/{id_autor}", status_code=204)

def delete_autor(id_autor:int):
    # Buscar el autor por su ID y eliminarlo
    for saved_autor in lista_autores:
        # Si se encuentra el autor, se elimina de la lista
        if saved_autor.id==id_autor:
            # Eliminar el autor de la lista
            lista_autores.remove(saved_autor)
            # Devolver una respuesta vacía
            return{}
        # Si no se encuentra el autor, se lanza una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Autor no encontrado")
