
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException

# Configuración del router
router = APIRouter()

# Configuración de OAuth2
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Configuración de JWT
ALGORITHM = "HS256"
#tiempo de expiración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#secret key para firmar los tokens
SECRET_KEY = "fce69a0a1b430771903083e7c4c647b51aad3f9e3b60255cce7a4c712289bf6d"

# Objeto que usaremos para el hash de  la contraseña
password_hash = PasswordHash.recommended()



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
    },

"johnsmith": {   
    "username": "johnsmith",
    "full_name": "John Smith",
    "email": "@example3.com",
    "disabled": True,
    "password": "$argon2id$v=19$m=65536,t=3,p=4$oehF+fUexmap0ORUbLEYnQ$Tzgwon1w4Z+sxf5+M5rFFClqCIhhcKlWkuMd0YlynQY"
}
    
}



# Endpoint para el registro de nuevos usuarios
@router.post("/register", status_code=201)
def register(user: UserDB):
    if user.username not in users_db:
    
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user

        return user

    else:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

   # Endpoint para el login de usuarios y generación de tokens JWT
#@router.post("/login")