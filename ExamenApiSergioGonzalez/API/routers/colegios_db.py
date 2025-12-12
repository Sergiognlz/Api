from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .auth_users import auth_user
from db.models.colegio import Colegio
from db.client import db_client
from db.schemas.colegio import colegio_schema, colegios_schema

from bson import ObjectId

router = APIRouter(prefix="/colegiosdb", tags=["colegiosdb"])



# la siguiente lista pretende simular una base de datos para probar nuestra API
colegios_list = []

@router.get("/", response_model=list[Colegio])
async def colegios():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return colegios_schema(db_client.test.colegios.find())



# Método get tipo query. Sólo busca por id
@router.get("", response_model=Colegio)
async def colegio(id: str):
    return search_colegio_id(id)


# Método get por id
@router.get("/{id}", response_model=Colegio)
async def colegio(id: str):
    return search_colegio_id(id)


@router.post("/", response_model=Colegio, status_code=201)
async def add_colegio(colegio: Colegio):
    #print("dentro de post")
    if type(search_colegio(colegio.nombre, colegio.distrito, colegio.tipo, colegio.direccion)) == Colegio:
        raise HTTPException(status_code=409, detail="User already exists")
    
    colegio_dict = colegio.model_dump()
    del colegio_dict["id"]
    # Añadimos el colegio a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro colegio
    id= db_client.test.colegios.insert_one(colegio_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    colegio_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio colegio añadido
    # Creamos un objeto de tipo Colegio a partir del diccionario colegio_dict
    return Colegio(**colegio_dict)
    
@router.put("/{id}", response_model=Colegio)
async def modify_user(id: str, new_colegio: Colegio):
    # Convertimos el usuario a un diccionario
    colegio_dict = new_colegio.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del colegio_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.colegios.find_one_and_replace({"_id":ObjectId(id)}, colegio_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_colegio_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Colegio not found")
    

@router.delete("/{id}", response_model=Colegio)
async def delete_colegio(id:str):
    found = db_client.test.colegios.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Colegio not found")
    return Colegio(**colegio_schema(found))
   
# El id de la base de datos es un string, ya no es un entero
def search_colegio_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        colegio = colegio_schema(db_client.test.colegios.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto Colegio. 
        return Colegio(**colegio)
    except:
        return {"error": "Colegio not found"}



def search_colegio(nombre: str, distrito: str, tipo:str, direccion:str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto Colegio. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        colegio = colegio_schema(db_client.test.colegios.find_one({"nombre":nombre, "distrito":distrito, "tipo":tipo, "direccion":direccion}))
        return Colegio(**colegio)
    except:
        return {"error": "User not found"}


def next_id():
    # Calculamos el colegio con el id más alto 
    # y le sumamos 1 a su id
    return (max(colegio.id for colegio in colegios_list))+1