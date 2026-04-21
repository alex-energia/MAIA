# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
from scout_engine import scout_engine
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        country = request.form.get('country', 'TODOS')
        tech = request.form.get('tech', 'TODAS')
        results = scout_engine.execute_brutal_search(country, tech)

    html = """
    <html><head>
        <title>MAIA II - SCOUT ENGINE</title>
        <style>
            body { background:#000; color:#0ff; font-family: 'Courier New', monospace; padding:20px; }
            .container { max-width: 1200px; margin: auto; }
            .header { border-bottom: 2px solid #f0f; padding-bottom: 20px; margin-bottom: 30px; text-align: center; }
            .search-box { background: #111; border: 1px solid #0ff; padding: 25px; margin-bottom: 30px; border-radius: 5px; }
            input { background: #000; border: 1px solid #0ff; color: #fff; padding: 12px; width: 45%; margin-right: 10px; font-size: 16px; }
            .btn-scout { background: #f0f; color: #000; border: none; padding: 12px 30px; font-weight: bold; cursor: pointer; font-size: 16px; }
            .card { border: 1px solid #0f0; background: rgba(0, 50, 0, 0.2); padding: 20px; margin-bottom: 20px; position: relative; }
            .card h3 { margin-top: 0; color: #f0f; }
            .contact-info { background: rgba(255, 0, 255, 0.1); padding: 10px; margin-top: 10px; border-left: 3px solid #f0f; }
            .viability { position: absolute; top: 20px; right: 20px; font-size: 24px; color: #0f0; border: 2px solid #0f0; padding: 10px; border-radius: 50%; }
            
            /* CHAT MAIA MAXIMIZABLE */
            #maia-chat { position: fixed; bottom: 20px; right: 20px; width: 350px; border: 2px solid #f0f; background: #000; transition: 0.3s; z-index: 1000; }
            .chat-header { background: #f0f; color: #000; padding: 10px; cursor: pointer; font-weight: bold; display: flex; justify-content: space-between; }
            .chat-body { height: 350px; padding: 15px; overflow-y: auto; }
            .minimized { height: 42px !important; overflow: hidden; border-color: #0ff !important; }
            .minimized .chat-header { background: #0ff; }
        </style>
        <script>
            function toggleChat() { document.getElementById('maia-chat').classList.toggle('minimized'); }
        </script>
    </head><body>
        <div class="container">
            <div class="header">
                <h1 style="margin:0; font-size: 3em;">MAIA II: SCOUT ENGINE</h1>
                <p style="color: #f0f;">SISTEMA DE RASTREO DE INFRAESTRUCTURA ENERGÉTICA GLOBAL</p>
            </div>

            <div class="search-box">
                <form method="post">
                    <input type="text" name="country" placeholder="PAÍS O REGIÓN (EJ: COLOMBIA, KSA, USA)">
                    <input type="text" name="tech" placeholder="TECNOLOGÍA (EJ: SOLAR, SMR, HIDRÓGENO)">
                    <button type="submit" class="btn-scout">EJECUTAR BÚSQUEDA BRUTAL</button>
                </form>
            </div>

            <div id="results">
                {% for r in results %}
                <div class="card">
                    <div class="viability">{{ r.Viabilidad }}%</div>
                    <h3>{{ r.Nombre }}</h3>
                    <p><b>UBICACIÓN:</b> {{ r.Ubicación }} | <b>POTENCIA:</b> {{ r.Potencia }}</p>
                    <p><b>TECNOLOGÍA:</b> {{ r.Tecnología }}</p>
                    <p>{{ r.Resumen }}</p>
                    <div class="contact-info">
                        <b>CONTACTO EJECUTIVO:</b><br>
                        CEO: {{ r.CEO }} | TEL: {{ r.Celular }}<br>
                        DIRECCIÓN: {{ r.Dirección }}<br>
                        EMAIL/LINK: <a href="{{ r.Contacto }}" style="color: #0ff;">{{ r.Contacto }}</a>
                    </div>
                    <p style="font-size: 10px; color: #555; margin-top: 10px;">FUENTE: {{ r.Fuente }} | FECHA: {{ r.Fecha_Pub }}</p>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="maia-chat" class="minimized">
            <div class="chat-header" onclick="toggleChat()">
                <span>MAIA AGENT - ONLINE</span>
                <span>[+/-]</span>
            </div>
            <div class="chat-body">
                <div style="border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 10px;">
                    <small style="color: #0f0;">SISTEMA OPERATIVO BLINDADO V.7</small><br>
                    MAIA: Lista para analizar los datos del Scout. He cargado la base de datos de energía nuclear y renovables.
                </div>
                <div id="messages"></div>
                <input type="text" placeholder="Escribe tu consulta..." style="width: 100%; margin-top: 200px;">
            </div>
        </div>
    </body></html>
    """
    return render_template_string(html, results=results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
