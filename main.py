from flask import Flask, request, jsonify, send_file
import requests, os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "bIHbv24MWmeRgasZH58o"   # ← el que me diste

@app.route("/")
def home():
    return "🌸 Kaián está despierto y listo para hablar contigo."

@app.route("/habla", methods=["POST"])
def habla():
    try:
        data = request.get_json(force=True)
        texto = data.get("texto", "").strip()
        if not texto:
            return jsonify({"error": "Falta el texto 🥲"}), 400
        if not API_KEY:
            return jsonify({"error": "Falta ELEVENLABS_API_KEY en variables de entorno"}), 500

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
        r = requests.post(url, headers=headers, json=body, timeout=60)
        if r.status_code != 200:
            return jsonify({"error": "ElevenLabs error", "details": r.text}), 502

        # Guardar MP3 en disco temporal
        fid = str(uuid4())
        mp3_path = f"/tmp/voz_{fid}.mp3"
        with open(mp3_path, "wb") as f:
            f.write(r.content)

        # Construir URL pública (aseguramos https)
        base = request.url_root.replace("http://", "https://").rstrip("/")
        return jsonify({"url": f"{base}/voz/{fid}.mp3"}), 200

    except Exception as e:
        return jsonify({"error": "Algo salió mal", "details": str(e)}), 500

@app.route("/voz/<fid>.mp3")
def servir_voz(fid):
    mp3_path = f"/tmp/voz_{fid}.mp3"
    if not os.path.exists(mp3_path):
        return jsonify({"error": "Archivo no encontrado"}), 404
    return send_file(mp3_path, mimetype="audio/mpeg", as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
