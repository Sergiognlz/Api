from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

# Crear la aplicación de FastAPI
app=FastAPI()

# Definición del modelo User
class User(BaseModel):
    # Atributos del usuario
    id:int
    name:str
    surname:str
    age:int

# Lista de usuarios de ejemplo
user_list= [
        #   Ejemplos de usuarios
        User(id=1, name="Sergio", surname="González",age=38),
        User(id=2, name="Juan Luís", surname="Barrionuevo",age=21), 
        User(id=3, name="Pablo", surname="Iglesias",age=46),
        User(id=4, name="Perro", surname="Sánchez",age=53)  
         
]

# Endpoint para obtener la lista de usuarios
@app.get("/users")

def users():

    return user_list

# Endpoint para obtener un usuario por su ID
@app.get("/users/{id_user}")

def get_user(id_user:int):
    
    return search_user(id_user)

# Endpoint para obtener un usuario por query
@app.get("/users/")

def get_user_query(id_user:int):
  
    return search_user(id_user)

# Endpoint para añadir un nuevo usuario
@app.post("/users", status_code=201, response_model=User)
# Endpoint para añadir un nuevo usuario
def add_user(user:User):
    # Asignar un ID al nuevo usuario
    user.id=next_id()
    # Añadir el usuario a la lista
    user_list.append(user)
    # Devolver el usuario añadido
    return user

# Endpoint para modificar un usuario existente
@app.put("/users/{id_user}", response_model=User)
def  modify_user(id_user:int, user: User):
    # Buscar el usuario por su ID y modificarlo
    for index, saved_user in enumerate(user_list):
        # Si se encuentra el usuario, se actualiza la información
        if saved_user.id==id_user:
            # Actualizar los datos del usuario
            user.id=id_user
            # Reemplazar el usuario en la lista
            user_list[index]=user
            # Devolver el usuario modificado
            return user
        

        
    # Si no se encuentra el usuario, se lanza una excepción HTTP 404
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{id_user}")
def delete_user(id_user:int):
    # Buscar el usuario por su ID y eliminarlo
    for saved_user in user_list:
        # Si se encuentra el usuario, se elimina de la lista
        if saved_user.id==id_user:
            user_list.remove(saved_user)
            return{}
        
    
    # Si no se encuentra el usuario, se lanza una excepción HTTP 404
    raise HTTPException(status_code=404, detail="User not found")

# Función para obtener el siguiente ID disponible
def next_id():
    # Calcular el siguiente ID disponible
    return (max(user_list, key=id).id+1)

# Función para buscar un usuario por su ID
def search_user(id_user:int):
    # Buscar el usuario por su ID
    users=[user for user in user_list if user.id==id_user]

    # Devolver el usuario encontrado o un mensaje de error
    return users[0] if users else {"error":"User not foud"}


