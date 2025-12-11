from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from db import directores_collection

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


# Modelo Director
class Director(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre: str
    apellidos: str
    nacionalidad: str

    model_config = {
        "json_encoders": {ObjectId: str},
        "arbitrary_types_allowed": True
    }


router = APIRouter(prefix="/directores", tags=["directores"])

@router.get("/", response_model=list[Director])
def get_directores():
    directors = list(directores_collection.find())
    return [Director(**d) for d in directors]

@router.get("/{id}", response_model=Director)
def get_director(id: str):
    director = directores_collection.find_one({"_id": ObjectId(id)})
    if director:
        return Director(**director)
    raise HTTPException(status_code=404, detail="Director no encontrado")

@router.post("/", response_model=Director)
def create_director(director: Director):
    director_dict = director.model_dump(exclude={"id"})
    result = directores_collection.insert_one(director_dict)
    director_dict["_id"] = result.inserted_id
    return Director(**director_dict)

@router.put("/{id}", response_model=Director)
def update_director(id: str, director: Director):
    director_dict = director.model_dump(exclude={"id"})
    result = directores_collection.update_one({"_id": ObjectId(id)}, {"$set": director_dict})
    if result.modified_count == 1:
        director_dict["_id"] = ObjectId(id)
        return Director(**director_dict)
    existing = directores_collection.find_one({"_id": ObjectId(id)})
    if existing:
        return Director(**existing)
    raise HTTPException(status_code=404, detail="Director no encontrado")

@router.delete("/{id}", status_code=204)
def delete_director(id: str):
    result = directores_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Director no encontrado")
