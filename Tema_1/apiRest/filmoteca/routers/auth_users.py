from datetime import *
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

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
    "disabled": False,
    "password": "$argon2id$v=19$m=65536,t=3,p=4$oehF+fUexmap0ORUbLEYnQ$Tzgwon1w4Z+sxf5+M5rFFClqCIhhcKlWkuMd0YlynQY"
},

"juanluis": {
    "username": "juanluis",
    "full_name": "Juan Lúis",
    "email": "@example3.com",
    "disabled": False,
    "password": "$argon2id$v=19$m=65536,t=3,p=4$TEgH6kpSHqXwZwHBfZAVkA$m4pmlFXbtewB3SMRhm0Q9m5GvnTn7hufO0eboHTWUSU"
}
}




# Endpoint para el registro de nuevos usuarios
@router.post("/register", status_code=201)
def register(user: UserDB):
    # Verificar si el usuario ya existe
    if user.username not in users_db:
        # Hashear la contraseña antes de almacenarla
        hashed_password = password_hash.hash(user.password)
        # Almacenar el nuevo usuario en la "base de datos"
        user.password = hashed_password
        # Agregar el usuario al diccionario de usuarios
        users_db[user.username] = user.model_dump()
        # Devolver el usuario registrado (sin la contraseña)
        return user

    else:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

   # Endpoint para el login de usuarios y generación de tokens JWT
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Verificar si el usuario existe
    user= users_db.get(form.username)

    if user:

        user=UserDB(**user)
        try:
            # Obtener el usuario de la "base de datos"
            if password_hash.verify(form.password, user.password):
                # Crear el token JWT
                expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token= {"sub":user.username, "exp": expire}
                # Generar el token
                token= jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            # Devolver el token
            return {"access_token": token, "token_type": "bearer"}
        except: 
            raise HTTPException(status_code=400, detail="Error en la autentificación")
    
    # Si el usuario no existe o la contraseña es incorrecta    
    raise HTTPException(status_code=401, detail="El usuario o la contraseña son incorrectos")


async def authentication (token: str = Depends(oauth2)):
    # Verificar y decodificar el token JWT
    try:
        
        username= jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales de autentificación inválidas", headers={"WWW-Authenticate": "Bearer"})
        
    # Obtener el usuario de la "base de datos"
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Credenciales de autentificación inválidas", headers={"WWW-Authenticate": "Bearer"})
    # Crear el objeto User
    user= User(**users_db[username])
   # Verificar si el usuario está activo 
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    # Devolver el usuario autenticado
    return user