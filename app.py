from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
database = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    value: str

@app.get("/")
def root():
    return {"message": "API calisiyor!"}

@app.get("/get/{key}")
def get_item(key: str):
    return {"key": key, "value": database.get(key, "Bulunamadi")}

@app.post("/set/{key}")
def set_item(key: str, item: Item):
    database[key] = item.value
    return {"message": f"{key} kaydedildi", "value": item.value}
