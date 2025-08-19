# main.py — FastAPI + archivos estáticos (Render)
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI(title="La Casita de Kaián")

# CORS opcional (por si luego llamas desde otro dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta pública con index.html y tus JS/CSS/imagenes
PUBLIC_DIR = Path("public")
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

# Ruta raíz: sirve el index.html
@app.get("/")
def home():
    index_file = PUBLIC_DIR / "index.html"
    # Si falta el archivo, devuelve un aviso útil:
    if not index_file.exists():
        return JSONResponse(
            {"ok": False, "msg": "No encuentro public/index.html 😅"},
            status_code=500,
        )
    return FileResponse(index_file)

# Salud / estado
@app.get("/health")
def health():
    return {"ok": True, "msg": "Kaián backend listo."}

# Ejemplo simple de chat (luego lo conectamos a tu lógica real)
@app.post("/chat")
def chat():
    return {"ok": True, "msg": "Aquí irá la respuesta del chat."}
