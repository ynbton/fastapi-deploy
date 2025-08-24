from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Any

app = FastAPI()

# Basit veri tabanı (RAM)
db = {}

# CORS ayarı: frontend’in hangi adresten istekte bulunacağını belirleyebilirsin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Her yerden erişim
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/set/{key}")
async def set_key(key: str, request: Request):
    data = await request.json()
    val = data.get("value")

    if not val:
        return {"error": "value boş olamaz"}

    # Eğer anahtar zaten varsa, diziye ekle
    if key in db:
        if isinstance(db[key], list):
            if isinstance(val, list):
                db[key].extend(val)
            else:
                db[key].append(val)
        else:
            db[key] = [db[key]]
            if isinstance(val, list):
                db[key].extend(val)
            else:
                db[key].append(val)
    else:
        # Eğer tek değer gönderilmişse direkt sakla
        db[key] = [val] if not isinstance(val, list) else val

    return {"key": key, "value": db[key]}

@app.get("/get/{key}")
async def get_key(key: str):
    return {"key": key, "value": db.get(key, [])}
