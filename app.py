from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "data.json"


# JSON dosyası yoksa oluştur
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)


# JSON yükle
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# JSON kaydet
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Gelen veri modeli
class Values(BaseModel):
    values: list[str]


@app.post("/set/{key}")
async def set_value(key: str, values: Values):
    if not values.values or all(v.strip() == "" for v in values.values):
        return {"error": "value boş olamaz"}  # ✅ boş değer engellendi
    
    data = load_data()
    data[key] = values.values
    save_data(data)
    return {"status": "ok", "key": key, "values": values.values}


@app.get("/get/{key}")
async def get_value(key: str, mode: str = "normal"):
    """
    mode=normal -> Liste gibi döner
    mode=json   -> JSON ham haliyle döner
    """
    data = load_data()
    if key not in data:
        return {"error": "Anahtar bulunamadı"}

    if mode == "json":
        return {"key": key, "values": data[key]}
    else:
        return {"key": key, "values": ", ".join(data[key])}


@app.delete("/delete/{key}")
async def delete_key(key: str):
    data = load_data()
    if key not in data:
        return {"error": "Anahtar zaten yok"}
    del data[key]
    save_data(data)
    return {"status": "deleted", "key": key}
