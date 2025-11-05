from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import directores
from routers import peliculas
from routers import auth_users 

# Crear la aplicación de FastAPI
app=FastAPI()

# Incluir los routers de autores y libros
app.include_router(directores.router)  
app.include_router(peliculas.router)   
app.include_router(auth_users.router)

# Configurar la ruta para archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")


def root():
    return{"Hello":"World"}