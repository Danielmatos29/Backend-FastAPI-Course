from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"], responses={404: {"message": "Not found"}})

products_list = ["Product1", "Product2", "Product3", "Product4", "Product5",]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id: int):
    return products_list[id - 1]

