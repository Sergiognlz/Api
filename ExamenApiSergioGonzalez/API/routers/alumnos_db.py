from fastapi import APIRouter, Depends, HTTPException
from .auth_users import auth_user
from db.client import db_client

from db.models.alumno import Alumno        
from db.schemas.alumno import alumno_schema

from bson import ObjectId

router = APIRouter(prefix="/alumnosdb", tags=["alumnosdb"])


# GET ALL
@router.get("/", response_model=list[Alumno])
async def get_alumno():
    return alumno_schema(db_client.test.alumnos.find())



# GET BY QUERY ?id=
@router.get("", response_model=Alumno)
async def get_alumno(id: str):
    return search_alumno_id(id)


# GET ALUMNOS ID_COLEGIO
@router.get("/{id_colegio}/alumnos", response_model=list[Alumno])
async def alumnos(id_colegio:str):
    # devuelve los alumnos según su id de colegio
    return alumno_schema(db_client.test.colegios.find(id_colegio))





# GET BY ID /{id}
@router.get("/{id}", response_model=Alumno)
async def get_alumno_path(id: str):
    return search_alumno_id(id)



@router.get("/{id}", response_model=Alumno)
async def get_alumno_path(id: str):
    return search_alumno_id(id)



# POST – ADD Alumno
@router.post("/", status_code=201, response_model=Alumno)
async def add_alumno(alumno: Alumno, user=Depends(auth_user)):

    alumno_dict = alumno.model_dump()
    del alumno_dict["id"]   # Mongo lo genera

    inserted_id = db_client.test.alumnos.insert_one(alumno_dict).inserted_id
    alumno_dict["id"] = str(inserted_id)

    return Alumno(**alumno_dict)



# PUT – MODIFY Alumno
@router.put("/{id}", response_model=Alumno)
async def modify_alumno(id: str, alumno: Alumno):

    alumno_dict = alumno.model_dump()
    del alumno_dict["id"]

    try:
        db_client.test.alumnos.find_one_and_replace(
            {"_id": ObjectId(id)},
            alumno_dict
        )
        return search_alumno_id(id)

    except:
        raise HTTPException(status_code=404, detail="Alumno not found")



# DELETE – Borra Alumno
@router.delete("/{id}", response_model=Alumno)
async def delete_alumno(id: str):

    found = db_client.test.alumnos.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Alumno not found")

    return Alumno(**alumno_schema(found))




def search_alumno_id(id: str):
    try:
        alumno = alumno_schema(
            db_client.test.alumnos.find_one({"_id": ObjectId(id)})
        )
        return Alumno(**alumno)
    except:
        raise HTTPException(status_code=404, detail="Alumno not found")
