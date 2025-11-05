
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter

# Configuración del router
router = APIRouter(
    prefix="/users",         # prefijo de ruta para todos los endpoints
    tags=["Users"]           # etiqueta para documentación
)

# Configuración de OAuth2
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Configuración de JWT
ALGORITHM = "HS256"
#tiempo de expiración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#secret key para firmar los tokens
SECRET_KEY = "fce69a0a1b430771903083e7c4c647b51aad3f9e3b60255cce7a4c712289bf6d"

# Objeto que usaremos para el hash de  la contraseña
password_hash = PasswordHash().recommended



# Definición del modelo User
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Definición del modelo UserDB que extiende User e incluye la contraseña
class UserDB(User):
    password: str



# Lista de usuarios de ejemplo
users_db = {
"johndoe": {
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "@example.com",
    "disabled": False,  
    "password": "secret"
},
"janedoe": {
    "username": "janedoe",
    "full_name": "Jane Doe",
    "email": "@example2.com",
    "disabled": True,
    "password": "secret2"   
}


}