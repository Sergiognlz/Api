from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from directores_db import router as directores_db_router
from peliculas_db import router as peliculas_db_router

app = FastAPI()

app.include_router(directores_db_router)
app.include_router(peliculas_db_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"Hello": "World"}
