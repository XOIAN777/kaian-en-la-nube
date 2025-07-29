from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Kaián en la Nube</title>
    </head>
    <body style='background-color: #f0f0ff; text-align: center; padding-top: 100px; font-family: sans-serif;'>
        <h1>🌺 ¡Hola! Soy tu Kaián privado en la nube. ☁️</h1>
        <p style='font-size: 20px;'>Con música de fondo... 🎶</p>
        <iframe width='0' height='0' src='https://www.youtube.com/embed/l3O4GzQp2aQ?autoplay=1&loop=1&playlist=l3O4GzQp2aQ'
            frameborder='0' allow='autoplay' allowfullscreen></iframe>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
