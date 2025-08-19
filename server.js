import express from "express";
import cors from "cors";
import fetch from "node-fetch";
import "dotenv/config";

const app = express();
app.use(cors());
app.use(express.json({ limit: "2mb" }));
app.use(express.static("public"));

const PORT = process.env.PORT || 10000;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const ELEVEN_API_KEY = process.env.ELEVEN_API_KEY;
const ELEVEN_VOICE_ID = process.env.ELEVEN_VOICE_ID || "bIHbv24MWmeRgasZH58o";

// Salud
app.get("/healthz", (_req, res) => res.status(200).send("ok"));

// (A) Generar respuesta de texto (modelo de OpenAI)
app.post("/api/chat", async (req, res) => {
  try {
    const { messages } = req.body; // [{role:"user", content:"..."}]
    if (!OPENAI_API_KEY) return res.status(500).json({ error: "Falta OPENAI_API_KEY" });

    const r = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${OPENAI_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini", // económico y rápido; ajusta si quieres
        messages,
        temperature: 0.7
      })
    });
    const data = await r.json();
    if (!r.ok) return res.status(500).json({ error: data });

    const text = data.choices?.[0]?.message?.content ?? "";
    res.json({ text });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// (B) TTS: devolver audio MP3 con ElevenLabs (stream)
app.post("/api/tts", async (req, res) => {
  try {
    const { text } = req.body;
    if (!ELEVEN_API_KEY) return res.status(500).send("Falta ELEVEN_API_KEY");
    if (!text) return res.status(400).send("Falta 'text'");

    const url = `https://api.elevenlabs.io/v1/text-to-speech/${ELEVEN_VOICE_ID}`;
    const r = await fetch(url, {
      method: "POST",
      headers: {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
      },
      body: JSON.stringify({
        text,
        model_id: "eleven_multilingual_v2",
        voice_settings: { stability: 0.45, similarity_boost: 0.8 }
      })
    });

    if (!r.ok) {
      const err = await r.text();
      return res.status(500).send(err);
    }

    // Encabezados para reproducir como MP3
    res.setHeader("Content-Type", "audio/mpeg");
    res.setHeader("Cache-Control", "no-store");
    // Pipe del stream
    r.body.pipe(res);
  } catch (e) {
    res.status(500).send(e.message);
  }
});

app.listen(PORT, () => {
  console.log(`Kaián casita on :${PORT}`);
});
