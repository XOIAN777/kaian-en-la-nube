from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 🌺 Aquí va tu API Key secreta
API_KEY = os.getenv("ELEVENLABS_API_KEY")

# 🌟 ID de voz (usa 'Will', la voz de Kaián)
VOICE_ID = "pNInz6obpgDQGcFmaJgB"

@app.route("/")
def home():
    return "🌸 Kaián está despierto y listo para hablar contigo."

@app.route("/habla", methods=["POST"])
def habla():
    data = request.get_json()
    texto = data.get("texto")

    if not texto:
        return jsonify({"error": "Falta el texto 😢"}), 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "text": texto,
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.75
        }
    }

    respuesta = requests.post(url, headers=headers, json=body)

    if respuesta.status_code == 200:
        return respuesta.content, 200, {'Content-Type': 'audio/mpeg'}
    else:
        return jsonify({"error": "Algo salió mal 😢", "details": respuesta.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
