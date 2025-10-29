from fastapi import FastAPI
from routers import autores, libros

# Crear la aplicación de FastAPI
app=FastAPI()

# Incluir los routers de autores y libros
app.include_router(autores.router)  
app.include_router(libros.router)   

@app.get("/")

def root():
    return{"Hello":"World"}