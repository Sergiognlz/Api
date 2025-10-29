from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import autores, libros

# Crear la aplicación de FastAPI
app=FastAPI()

# Incluir los routers de autores y libros
app.include_router(autores.router)  
app.include_router(libros.router)   

# Configurar la ruta para archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")


def root():
    return{"Hello":"World"}