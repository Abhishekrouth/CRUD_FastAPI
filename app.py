from fastapi import FastAPI, status, Request
from typing import Optional
from pydantic import BaseModel, Field

class PriceDetails(BaseModel):
    price: float = Field(..., gt=0)
    currency: str
    discount: float

class Item(BaseModel):
    id: int
    item_name: str = Field(..., min_length=5)
    price: PriceDetails
    description: str | None = None

db = [
    {"id": 1, "item_name": "Laptop", "price": { "price":1200.5, "currency":"USD", "discount":20}, "description": "Gaming laptop"},
    {"id": 2, "item_name": "Mouse", "price": { "price":3400, "currency":"INR", "discount":30}, "description": "Wireless mouse"},
    {"id": 3, "item_name": "Keyboard", "price": { "price":1100, "currency":"USD", "discount":10}, "description": "Mechanical keyboard"},
    {"id": 4, "item_name": "Monitor", "price": { "price":5000, "currency":"USD", "discount":35}, "description": "24-inch monitor"},
    {"id": 5, "item_name": "Headphones", "price": { "price":2000, "currency":"INR", "discount":10}, "description": "Noise-cancelling"}
]

app = FastAPI()

@app.get("/")
def read_record():
    return db

@app.post("/create")
def create_record(create: Item):
    db.append(create.dict())
    return {"message": "Data created successfully", "data": db}
   
@app.put("/update")
def update_record(update: Item):
    for x in db:
        if x["id"] == update.id:
            x.update(update.dict()) 
            return {"message": "Data updated successfully", "data": db}
    return {"message": f"Item with id {update.id} not found"}

@app.delete("/delete")
def delete_record(id: int):
    for x in db:
        if x["id"] == id:
            db.remove(x) 
            return {"message": f"Data with id {id} deleted successfully"}
    return {"message": f"Data with id {id} does not exist"}
