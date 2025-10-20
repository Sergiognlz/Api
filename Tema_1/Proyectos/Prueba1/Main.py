from fastapi import FastAPI
from Tema_1.ApiRest.Autores.Autores import app as autores_app

# Crear la aplicación principal
app=FastAPI()


@app.get("/")
# Endpoint raíz
def root():
    return{"mensaje":"Bienvenido a la Api de Autores"}

# Montar la aplicación de autores en el path /api
app.mount("/api", autores_app)
