from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Crear la aplicación de FastAPI
app=FastAPI()

# Definición del modelo Libro
from pydantic import BaseModel

# Definición del modelo Libro
class Libro(BaseModel):
    id: int
    ISBN: str
    titulo: str
    num_paginas: int
    id_autor: int

lista_libros = [
    # Libros de H.P. Lovecraft (id=1)
    Libro(id=1, ISBN="978-1-23456-001-0", titulo="La Llamada de Cthulhu", num_paginas=128, autor_id=1),
    Libro(id=2, ISBN="978-1-23456-002-7", titulo="En las montañas de la locura", num_paginas=200, autor_id=1),
    Libro(id=3, ISBN="978-1-23456-003-4", titulo="La sombra sobre Innsmouth", num_paginas=150, autor_id=1),

    # Libros de Frank Belknap Long (id=2)
    Libro(id=4, ISBN="978-1-23456-004-1", titulo="El hombre de arena", num_paginas=180, autor_id=2),
    Libro(id=5, ISBN="978-1-23456-005-8", titulo="Los dioses de Nehwon", num_paginas=160, autor_id=2),
    Libro(id=6, ISBN="978-1-23456-006-5", titulo="Los fantasmas de Ulthar", num_paginas=140, autor_id=2),

    # Libros de Clark Ashton Smith (id=3)
    Libro(id=7, ISBN="978-1-23456-007-2", titulo="El valle del sueño", num_paginas=180, autor_id=3),
    Libro(id=8, ISBN="978-1-23456-008-9", titulo="La ciudad sin nombre", num_paginas=210, autor_id=3),
    Libro(id=9, ISBN="978-1-23456-009-6", titulo="El reino de los hechizos", num_paginas=190, autor_id=3),

    # Libros de Robert E. Howard (id=4)
    Libro(id=10, ISBN="978-1-23456-010-2", titulo="Conan el bárbaro", num_paginas=220, autor_id=4),
    Libro(id=11, ISBN="978-1-23456-011-9", titulo="La reina de la Costa Negra", num_paginas=200, autor_id=4),
    Libro(id=12, ISBN="978-1-23456-012-6", titulo="El dios en el cuenco", num_paginas=180, autor_id=4),

    # Libros de Robert Bloch (id=5)
    Libro(id=13, ISBN="978-1-23456-013-3", titulo="El demonio de la perversión", num_paginas=150, autor_id=5),
    Libro(id=14, ISBN="978-1-23456-014-0", titulo="Psicosis", num_paginas=210, autor_id=5),
    Libro(id=15, ISBN="978-1-23456-015-7", titulo="El extraño", num_paginas=170, autor_id=5)
]


# Endpoint para obtener la lista de libros
@app.get("/libros")

def Libros():
    # Devolver la lista de libros
    return lista_libros

# Endpoint para obtener un libro por su ID
@app.get("/libros/{id_libro}")

def get_libro(id_libro:int):
    # Buscar el libro por su ID
    libros=[libro for libro in lista_libros if libro.id==id_libro]
    # Devolver el libro encontrado o un mensaje de error
    return libros[0] if libros else {"error":"Libro no encontrado"}

# Libro por query 
@app.get("/libros/") 

def get_libro_query(id_libro:int):
    # Buscar el libro por su ID
    libros=[libro for libro in lista_libros if libro.id==id_libro]
    # Devolver el libro encontrado o un mensaje de error
    return libros[0] if libros else {"error":"Libro no encontrado"}

# Endpoint para añadir un nuevo libro
@app.post("/libros", status_code=201, response_model=Libro)

def add_libro(libro:Libro):
    # Asignar un ID al nuevo libro
    libro.id=next_id()
    # Añadir el libro a la lista
    lista_libros.append(libro)
    # Devolver el libro añadido
    return libro

@app.put("/libros/{id_libro}", response_model=Libro)

def  modify_libro(id_libro:int, libro: Libro):  
    # Buscar el libro por su ID y modificarlo
    for index, saved_libro in enumerate(lista_libros):
        # Si se encuentra el libro, se actualiza la información
        if saved_libro.id==id_libro:
            # Actualizar los datos del libro
            libro.id=id_libro
            # Reemplazar el libro en la lista
            lista_libros[index]=libro
            # Devolver el libro modificado
            return libro
        
    # Si no se encuentra el libro, lanzar una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Endpoint para eliminar un libro por su ID
@app.delete("/libros/{id_libro}", status_code=204)

def delete_libro(id_libro:int):
    # Buscar el libro por su ID y eliminarlo
    for saved_libro in lista_libros:
        # Si se encuentra el libro, se elimina de la lista
        if saved_libro.id==id_libro:
            lista_libros.remove(saved_libro)
            return{}
        
    # Si no se encuentra el libro, lanzar una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Libro no encontrado")


# Función para obtener el siguiente ID disponible
def next_id():
    # Si la lista no está vacía, obtener el máximo ID y sumarle 1
    if lista_libros:
        return max(libro.id for libro in lista_libros) + 1
    # Si la lista está vacía, empezar desde 1
    else:
        return 1
    
