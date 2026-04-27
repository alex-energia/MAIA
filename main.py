# -*- coding: utf-8 -*-
import os
import time
import re
import random
from flask import Flask, render_template_string, request, session
from duckduckgo_search import DDGS

app = Flask(__name__)
app.secret_key = os.urandom(2048)

class MaiaOmniEngine:
    def __init__(self):
        self.pilares = [
            "Hidroelectrica", "Startup Tecnologia", "SMR Nuclear",
            "Solar BESS", "Termica", "Geotermica", "Neutrinos", "Hidrogeno Verde"
        ]
        # Filtro global: Busca en cualquier sitio gubernamental, educativo o financiero (.gov, .org, .edu, .int)
        # y permite cualquier dominio de país (.*)
        self.global_filter = "(site:gov OR site:org OR site:edu OR site:int OR site:biz OR site:io)"
        self.keywords = "(tender OR licitacion OR 'equity sale' OR 'funding round' OR 'contract award')"

    def run_omni_scan(self):
        results = []
        with DDGS() as ddgs:
            # Mezclamos los pilares para que cada búsqueda sea única y evitar bloqueos
            random.shuffle(self.pilares)
            
            for pilar in self.pilares[:6]: # Analizamos 6 pilares por ráfaga para mantener velocidad
                query = f'"{pilar}" {self.global_filter} {self.keywords} 2026 "USD"'
                try:
                    # Delay de sigilo: Maia "respira" entre búsquedas
                    time.sleep(random.uniform(3, 6))
                    data = list(ddgs.text(query, max_results=4))
                    
                    for entry in data:
                        body = entry.get('body', '').lower()
                        # Verificación de valor económico real
                        if any(k in body for k in ["$", "usd", "million", "billion", "m", "b"]):
                            val = re.search(r'(\$[0-9,.]+ ?(million|billion|m|b|usd))', body, re.I)
                            
                            results.append({
                                "id": f"OMNI-{random.randint(10000,99999)}",
                                "pilar": pilar.upper(),
                                "nombre": entry['title'].upper(),
                                "valor": val.group(0).upper() if val else "ANALIZANDO CIFRAS...",
                                "vinculo": entry['href'],
                                "datos": body[:250] + "..."
                            })
                except: continue
        return results

scout = MaiaOmniEngine()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout.run_omni_scan()
            session.modified = True
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item); session.modified = True
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA v15 - OMNI GLOBAL SCOUT</title>
        <style>
            :root { --cian: #00ffff; --gold: #ffd700; --red: #ff3366; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:monospace; padding:20px; font-size:12px; }
            .nav { border-bottom: 2px solid #111; padding-bottom:15px; display:flex; gap:10px; margin-bottom:20px; }
            .btn-nav { background:none; border:1px solid #333; color:#555; padding:8px 15px; cursor:pointer; }
            .active { border-color:var(--cian); color:var(--cian); }
            .btn-scan { background:#000; border:2px solid var(--cian); color:var(--cian); padding:25px; width:100%; cursor:pointer; font-weight:bold; font-size:18px; text-transform:uppercase; letter-spacing:2px; box-shadow: 0 0 10px rgba(0,255,255,0.1); }
            .btn-scan:hover { background:var(--cian); color:#000; }
            .ficha { background:#050505; border:1px solid #111; border-left:5px solid var(--cian); padding:25px; margin-top:25px; }
            .title { font-size:17px; font-weight:bold; color:var(--cian); margin-bottom:10px; }
            .val-box { background:rgba(0,255,255,0.05); border:1px dashed var(--cian); padding:10px; margin:10px 0; color:#fff; font-size:16px; }
            
            #maia-chat { position:fixed; bottom:20px; right:20px; width:300px; border:1px solid #222; background:#000; z-index:999; }
            .chat-h { background:#111; color:var(--cian); padding:10px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            .chat-b { height:150px; padding:10px; overflow-y:auto; font-size:10px; color:#0f0; border-top:1px solid #222; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">OMNI SCOUT GLOBAL</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">ARCHIVO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; color:var(--red);">RESET</button>
            </form>
        </div>

        {% if view == 'scout' %}
            <form method="POST"><input type="hidden" name="action" value="run_scout"><button type="submit" class="btn-scan">INICIAR BARRIDO PLANETARIO DE ACTIVOS</button></form>
            
            {% if not session['history'] %}
                <div style="text-align:center; padding:100px; color:#222; font-size:20px;">SISTEMA EN STANDBY. RED GLOBAL LISTA.</div>
            {% endif %}

            {% for r in session['history'] %}
            <div class="ficha">
                <div style="color:var(--gold); font-size:10px; letter-spacing:1px;">{{ r.pilar }}</div>
                <div class="title">{{ r.nombre }}</div>
                <div class="val-box"><b>VALOR ESTIMADO:</b> {{ r.valor }}</div>
                <div style="color:#666; margin-bottom:15px; line-height:1.4;">{{ r.datos }}</div>
                <div style="display:flex; gap:15px;">
                    <a href="{{ r.vinculo }}" target="_blank" style="color:var(--cian); text-decoration:none; font-weight:bold;">[ ACCEDER AL NODO ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--gold); cursor:pointer; font-weight:bold;">[ ARCHIVAR ]</button></form>
                </div>
            </div>
            {% endfor %}
        {% else %}
            {% for s in session['saved'] %}
            <div class="ficha" style="border-left-color:var(--gold);">
                <div class="title" style="color:var(--gold);">{{ s.nombre }}</div>
                <div class="val-box">{{ s.valor }}</div>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggleChat()"><span>MAIA CONSOLE v15</span><span id="ico">[+]</span></div>
            <div id="chat-body" class="chat-b" style="display:none;">
                > INITIALIZING OMNI-PROTOCOL...<br>
                > SCANNING ALL DOMAINS (.GOV, .ORG, .INT)...<br>
                > ANALYZING 8 ENERGY PILARS...<br>
                > STATUS: TOTAL GLOBAL REACH
            </div>
        </div>

        <script>
            function toggleChat() {
                var b = document.getElementById('chat-body');
                var i = document.getElementById('ico');
                if(b.style.display === 'none') { b.style.display = 'block'; i.innerText = '[-]'; }
                else { b.style.display = 'none'; i.innerText = '[+]'; }
            }
        </script>
    </body>
    </html>
    """, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)