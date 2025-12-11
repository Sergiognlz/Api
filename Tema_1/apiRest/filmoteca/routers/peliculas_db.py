from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from db import peliculas_collection

# Definición del tipo ObjectId para Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Modelo Pelicula
class Pelicula(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo: str
    duracion: int
    id_director: PyObjectId

    model_config = {
        "json_encoders": {ObjectId: str},
        "arbitrary_types_allowed": True
    }


router = APIRouter(prefix="/peliculas", tags=["peliculas"])

@router.get("/", response_model=list[Pelicula])
def get_peliculas():
    peliculas = list(peliculas_collection.find())
    return [Pelicula(**p) for p in peliculas]

@router.get("/{id}", response_model=Pelicula)
def get_pelicula(id: str):
    pelicula = peliculas_collection.find_one({"_id": ObjectId(id)})
    if pelicula:
        return Pelicula(**pelicula)
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

@router.post("/", response_model=Pelicula)
def create_pelicula(pelicula: Pelicula):
    pelicula_dict = pelicula.model_dump(exclude={"id"})
    result = peliculas_collection.insert_one(pelicula_dict)
    pelicula_dict["_id"] = result.inserted_id
    return Pelicula(**pelicula_dict)

@router.put("/{id}", response_model=Pelicula)
def update_pelicula(id: str, pelicula: Pelicula):
    pelicula_dict = pelicula.model_dump(exclude={"id"})
    result = peliculas_collection.update_one({"_id": ObjectId(id)}, {"$set": pelicula_dict})
    if result.modified_count == 1:
        pelicula_dict["_id"] = ObjectId(id)
        return Pelicula(**pelicula_dict)
    existing = peliculas_collection.find_one({"_id": ObjectId(id)})
    if existing:
        return Pelicula(**existing)
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

@router.delete("/{id}", status_code=204)
def delete_pelicula(id: str):
    result = peliculas_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
