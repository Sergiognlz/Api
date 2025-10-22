from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()


class User(BaseModel):
    id:int
    name:str
    surname:str
    age:int

user_list= [
        User(id=1, name="Sergio", surname="González",age=38),
        User(id=2, name="Juan Luís", surname="Barrionuevo",age=21), 
        User(id=3, name="Pablo", surname="Iglesias",age=46),
        User(id=4, name="Perro", surname="Sánchez",age=53)  
         
]


@app.get("/users")

def users():

    return user_list

@app.get("/users/{id_user}")

def get_user(id_user:int):
    
    return search_user(id_user)


@app.get("/users/")

def get_user_query(id_user:int):
  

 
    return search_user(id_user)

def search_user(id_user:int):
    users=[user for user in user_list if user.id==id_user]

 
    return users[0] if users else {"error":"User not foud"}