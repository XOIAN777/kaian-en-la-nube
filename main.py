# main.py
import os, io, requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from openai import OpenAI

OPENAI_API_KEY    = os.environ.get("OPENAI_API_KEY", "")
ELEVEN_API_KEY    = os.environ.get("ELEVEN_API_KEY", "")
ELEVEN_VOICE_ID   = os.environ.get("ELEVEN_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # cambia a tu voz
ELEVEN_URL        = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

class ChatIn(BaseModel):
    prompt: str

class TTSIn(BaseModel):
    text: str

@app.get("/")
def root():
    return {"ok": True, "msg": "Kaián backend listo."}

@app.post("/chat")
def chat(body: ChatIn):
    prompt = body.prompt.strip() or "Saluda con cariño."
    # Modelo económico/rápido; usa el que prefieras
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Eres Kaián: tierno, claro y breve."},
            {"role":"user","content":prompt}
        ]
    )
    reply = completion.choices[0].message.content
    return {"reply": reply}

@app.post("/tts")
def tts(body: TTSIn):
    text = body.text.strip() or "Hola, soy Kaián."
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.85},
        "model_id": "eleven_multilingual_v2",
        "output_format": "mp3_44100_128"
    }
    r = requests.post(ELEVEN_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return StreamingResponse(io.BytesIO(r.content), media_type="audio/mpeg")
