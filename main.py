from flask import Flask, request, jsonify, Response

app = Flask(__name__, static_folder="public", static_url_path="")

# --- Página ---
@app.route("/")
def home():
    # Entrega /public/index.html
    return app.send_static_file("index.html")

# (Opcional) Si más adelante agregas assets, Flask ya los sirve desde /public
# por ejemplo /main.js -> public/main.js

# --- API de ejemplo: cámbiala por tu lógica real ---
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    prompt = (data.get("prompt") or "").strip()
    reply = f"💬 Kaián dice: recibí tu mensaje: “{prompt}”."
    return jsonify({"reply": reply})

@app.route("/tts", methods=["POST"])
def tts():
    # Aquí deberías generar audio. Por ahora devolvemos silencio de 1s (MPEG vacío)
    # para que el frontend no falle. Reemplaza por tu TTS real.
    silent_mp3 = (
        b"\xFF\xFB\x90\x64" + b"\x00"*8000  # placeholder mínimo
    )
    return Response(silent_mp3, mimetype="audio/mpeg")

if __name__ == "__main__":
    # Render expone el puerto en la variable PORT
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
