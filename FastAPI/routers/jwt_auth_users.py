from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "389fcf5aa1d19f71c78f1a8f02176c44afcf89f24114126656d06f520b2f1196"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username : str
    full_name : str
    email : str
    disabled : bool

class UserDB(User):
    password: str

users_db = {
    "danielm": {
        "username": "danielm",
        "full_name": "Daniel Matos",
        "email": "danielmatosrom2912@gmail.com",
        "disabled": False,
        "password": "$2a$12$5eZD1sRcpphEYlYan6lXBe0AZpzYJkuBhan.u45UPpCsmYAyziiPC"
    },

    "diegom": {
        "username": "diegom",
        "full_name": "Diego Matos",
        "email": "diegomatos08@gmail.com",
        "disabled": True,
        "password": "$2a$12$3ttCBTctjQs.f9o/4OGzluU2PRyyEkb4iUyv8YpTsKvLvo2Nw0ESu"
    }
}

def search_user_db(username : str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username : str):
    if username in users_db:
        return User(**users_db[username])

async def user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials", 
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")

        if username is None:
            raise exception
        
    except JWTError:
        raise exception

    return search_user(username)
    
async def current_user(user: User = Depends(user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="The user is not active")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is not correct.")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password is not correct")

    access_token = {"sub": user.username, "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user