from fastapi import FastAPI
from routers import auth_users, alumnos_db, colegios_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(auth_users.router)
app.include_router(alumnos_db.router)
app.include_router(colegios_db.router)


@app.get("/")
def root():
    return {"Examen Api": "Sergio González"}


