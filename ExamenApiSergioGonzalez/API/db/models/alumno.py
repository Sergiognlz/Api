from typing import Optional
from pydantic import BaseModel

class Alumno(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    curso: str
    repetidor: bool=False
    id_colegio: str

