from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Crear la aplicación de FastAPI
router=APIRouter(prefix="/peliculas", tags=["peliculas"])

# Definición del modelo Libro
from pydantic import BaseModel

# Definición del modelo Libro
class Pelicula(BaseModel):
    id: int
    titulo: str
    duracion: int
    id_director: int

lista_peliculas = [
    Pelicula(id=1, titulo="Inception", duracion=148, id_director=3),
    Pelicula(id=2, titulo="Pulp Fiction", duracion=154, id_director=4),
    Pelicula(id=3, titulo="Jurassic Park", duracion=127, id_director=1),
    Pelicula(id=4, titulo="The Dark Knight", duracion=152, id_director=3),
    Pelicula(id=5, titulo="Schindler's List", duracion=195, id_director=1),
    Pelicula(id=6, titulo="The Aviator", duracion=170, id_director=1),
    Pelicula(id=7, titulo="Goodfellas", duracion=146, id_director=2),
    Pelicula(id=8, titulo="Dunkirk", duracion=106, id_director=3),
    Pelicula(id=9, titulo="Kill Bill: Vol. 1", duracion=111, id_director=4),
    Pelicula(id=10, titulo="Vertigo", duracion=128, id_director=5)

]


# Endpoint para obtener la lista de libros
@router.get("/")


def Peliculas():
    # Devolver la lista de libros
    return lista_peliculas

# Endpoint para obtener una pelicula por su ID
@router.get("/{id_pelicula}")

# Buscar la pelicula por su ID
def get_pelicula(id_pelicula:int):
    # Buscar la pelicula por su ID
    peliculas=[pelicula for pelicula in lista_peliculas if pelicula.id==id_pelicula]
    # Devolver la pelicula encontrada o un mensaje de error
    return peliculas[0] if peliculas else {"error":"Pelicula no encontrada"}    



# Pelicula por query 
@router.get("/")
def get_pelicula_query(id_pelicula:int):
    peliculas=[pelicula for pelicula in lista_peliculas if pelicula.id==id_pelicula]

    return peliculas[0] if peliculas else {"error":"Pelicula no encontrada"}    


# Endpoint para añadir un nuevo libro
@router.post("/", status_code=201, response_model=Pelicula)
# Añadir una nueva pelicula
def add_pelicula(pelicula:Pelicula):
    # Asignar un ID al nuevo libro
    pelicula.id=next_id()
    # Añadir el libro a la lista
    lista_peliculas.append(pelicula)
    # Devolver el libro añadido
    return pelicula


@router.put("/{id_pelicula}", response_model=Pelicula)  

# Modificar una pelicula existente
def  modify_pelicula(id_pelicula:int, pelicula: Pelicula):  
    # Buscar la pelicula por su ID y modificarlo
    for index, saved_pelicula in enumerate(lista_peliculas):
        # Si se encuentra la pelicula, se actualiza la información
        if saved_pelicula.id==id_pelicula:
            # Actualizar los datos de la pelicula
            pelicula.id=id_pelicula
            # Reemplazar la pelicula en la lista
            lista_peliculas[index]=pelicula
            # Devolver la pelicula modificada
            return pelicula
        
    # Si no se encuentra la pelicula, lanzar una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")


        
# Endpoint para eliminar una pelicula por su ID
@router.delete("/{id_pelicula}", status_code=204)

def delete_pelicula(id_pelicula:int):
    # Buscar la pelicula por su ID y eliminarla
    for index, saved_pelicula in enumerate(lista_peliculas):
        # Si se encuentra la pelicula, se elimina de la lista
        if saved_pelicula.id==id_pelicula:
            lista_peliculas.pop(index)
            return
    # Si no se encuentra la pelicula, lanzar una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

# Función para obtener el siguiente ID disponible
def next_id():  
    # Si la lista no está vacía, obtener el máximo ID y sumarle 1
    if lista_peliculas:
        return max(pelicula.id for pelicula in lista_peliculas) + 1
    # Si la lista está vacía, empezar desde 1
    else:
        return 1
    
