from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Daniel", surname="Matos", url="https://moure.dev", age=18),
              User(id=2, name="Diego", surname="Matos", url="https://mouredev.com", age=21),
              User(id=3, name="Manuel", surname="Suarez", url="https://moure.dev", age=18)]

# Inicia el server: python -m uvicorn users:app --reload
@router.get("/usersjson")
async def usersjson():
    return [{"name": "Daniel", "surname": "Matos", "url": "https://moure.dev"},
            {"name": "Diego", "surname": "Matos", "url": "https://mouredev.com"},
            {"name": "Manuel", "surname": "Suarez", "url": "https://manuelsua.com"},]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

@router.get("/user")
async def user(id: int):
    return search_user(id)

@router.post("/user")
async def user(user: User, status_code=201):
    if type((search_user(user.id)) == User):
        raise HTTPException(status_code=409, detail="The user already exists.")
    else:
        return users_list.append(user)

@router.put("/user")
async def user(user: User, status_code=202):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return user

    if not found:
        raise HTTPException(status_code=404, detail="The user was not found")

@router.delete("/user/{id}")
async def user(id : int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return saved_user

    if not found:
        raise HTTPException(status_code=404, detail="The user was not found.")
    
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        raise HTTPException(status_code=404, detail="User not found")