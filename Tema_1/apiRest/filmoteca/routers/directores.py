from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Crear la aplicación de FastAPI
router=APIRouter(prefix="/directores", tags=["directores"])

# Definición del modelo Director
class Director(BaseModel):
    id:int
    nombre:str
    apellidos:str
    nacionalidad:str

# Lista de autores de ejemplo
lista_directores= [
        Director(id=1, nombre="Steven", apellidos="Spielberg", nacionalidad="Estadounidense"),
        Director(id=2, nombre="Martin", apellidos="Scorsese", nacionalidad="Estadounidense"),
        Director(id=3, nombre="Christopher", apellidos="Nolan", nacionalidad="Británico"),
        Director(id=4, nombre="Quentin", apellidos="Tarantino", nacionalidad="Estadounidense"),
        Director(id=5, nombre="Alfred", apellidos="Hitchcock", nacionalidad="Británico")
]

# Endpoint para obtener la lista de directores
@router.get("/")
def Directores():
    return lista_directores

# Endpoint para obtener un autor por su ID
@router.get("/{id}")
def get_director(id:int):
    directores=[director for director in lista_directores if director.id==id]

    return directores[0] if directores else {"error":"Director no encontrado"}
   

# Director por query 
@router.get("")
def get_director_query(id:int):
    directores=[director for director in lista_directores if director.id==id]

    return directores[0] if directores else {"error":"Director no encontrado"}


# Endpoint para añadir un nuevo director
@router.post("/", status_code=201, response_model=Director)
def add_director(director:Director):
    # Asignar un ID al nuevo director
    director.id=next_id()
    # Añadir el director a la lista
    lista_directores.append(director)
    # Devolver el director añadido
    return director

# Función para obtener el siguiente ID disponible
def next_id():
    # Si la lista no está vacía, obtener el máximo ID y sumarle 1
    if lista_directores:
        return max(director.id for director in lista_directores) + 1
    # Si la lista está vacía, empezar desde 1
    else:
        return 1
    

# Endpoint para modificar un director por su ID    
@router.put("/{id}", response_model=Director)

def modify_director(id:int, director: Director):   
    # Buscar el director por su ID y modificarlo
    for index, saved_director in enumerate(lista_directores):
        # Si se encuentra el director, se actualiza la información
        if saved_director.id==id:
            # Actualizar los datos del director
            director.id=id
            # Reemplazar el director en la lista
            lista_directores[index]=director
            # Devolver el director modificado
            return director
          
    # Si no se encuentra el director, se lanza una excepción HTTP 404    
    raise HTTPException(status_code=404, detail="Director no encontrado")

# Endpoint para eliminar un director por su ID
@router.delete("/{id}", status_code=204)
def delete_director(id:int):
    # Buscar el director por su ID y eliminarlo
    for saved_director in lista_directores:
        # Si se encuentra el director, se elimina de la lista
        if saved_director.id==id:
            lista_directores.remove(saved_director)
            return{}
        
    # Si no se encuentra el director, lanzar una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Director no encontrado")