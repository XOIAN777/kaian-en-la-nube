from flask import Flask, request, jsonify, Response
import os
import requests
from dotenv import load_dotenv

# Carga variables de entorno (.env en local; en Render configúralas en Dashboard)
load_dotenv()

app = Flask(__name__)

# 🔐 Tu API Key de ElevenLabs (configúrala como variable de entorno: ELEVENLABS_API_KEY)
API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# 🎙️ ID de voz (ejemplo). Pon aquí la tuya:
VOICE_ID = "bIHbv24MWmeRgasZH58o"

@app.route("/")
def home():
    return "🌸 Kaián está despierto y listo para hablar contigo."

@app.route("/healthz")
def healthz():
    return jsonify({"ok": True})

@app.route("/habla", methods=["POST"])
def habla():
    if not API_KEY:
        return jsonify({"error": "Falta ELEVENLABS_API_KEY en variables de entorno"}), 500

    data = request.get_json(silent=True) or {}
    texto = data.get("texto", "").strip()

    if not texto:
        return jsonify({"error": "Falta el texto 🫣"}), 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    body = {
        "text": texto,
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.75
        }
    }

    try:
        r = requests.post(url, headers=headers, json=body, timeout=60)
    except requests.RequestException as e:
        return jsonify({"error": "Fallo al llamar a ElevenLabs", "details": str(e)}), 502

    if r.status_code == 200:
        # Devolvemos audio MP3 binario
        return Response(r.content, mimetype="audio/mpeg")
    else:
        return jsonify({
            "error": "ElevenLabs respondió con error",
            "status": r.status_code,
            "details": r.text
        }), 502

# Nota: NO usamos app.run() aquí porque en Render lanzamos con Gunicorn.
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000, debug=False)
