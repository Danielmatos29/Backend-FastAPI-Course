from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schema.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/users_db",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

users_list = []

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}")
async def get_user_query(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/")
async def get_user(id: str):
    return search_user("id", ObjectId(id))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    try:
        if type(search_user("email", user.email)) == User:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The user already exists.")
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id" : id}))

    return User(**new_user)

@router.put("/", status_code=status.HTTP_202_ACCEPTED)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "The user hasn't been updated"}

    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id : str):
    found = db_client.users.find_one_and_delete({"_id" : ObjectId(id)})

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user was not found.")
    
def search_user(field : str, key):
    try:
        user = user_schema(db_client.users.find_one({field : key}))
        return User(**user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    