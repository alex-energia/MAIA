# -*- coding: utf-8 -*-
import os
import time
import re
import random
from flask import Flask, render_template_string, request, session
from duckduckgo_search import DDGS

app = Flask(__name__)
app.secret_key = os.urandom(2048)

class MaiaUltimateScout:
    def __init__(self):
        self.targets = ["site:gov", "site:energy.gov", "site:doe.gov", "site:nrc.gov"]
        
    def run(self):
        results = []
        # Queries simplificadas para evitar el baneo por complejidad
        queries = [
            '"SMR" contract award 2026 USD',
            'small modular reactor funding 2026',
            'SMR investment opportunity USA 2026'
        ]
        
        with DDGS() as ddgs:
            for q in queries:
                try:
                    # SIMULACIÓN DE COMPORTAMIENTO HUMANO (Crucial)
                    wait = random.uniform(5, 10)
                    time.sleep(wait) 
                    
                    # Buscamos en el índice general pero filtrando por dominios oficiales
                    search_data = list(ddgs.text(q, max_results=5))
                    
                    for entry in search_data:
                        body = entry.get('body', '').lower()
                        url = entry.get('href', '').lower()
                        
                        # FILTRO DE VERDAD: Si no es un sitio oficial o financiero, se descarta
                        if not any(t in url for t in [".gov", ".edu", ".org", "energy", "nuclear"]):
                            continue

                        # Extracción Regex de Capital
                        val = re.search(r'(\$[0-9,.]+ ?(million|billion|M|B|USD))', body, re.I)
                        
                        results.append({
                            "id": f"LIVE-{int(time.time())}-{random.randint(100,999)}",
                            "pilar": "SMR NUCLEAR USA",
                            "nombre": entry['title'].upper(),
                            "valor": val.group(0).upper() if val else "VER EN DOCUMENTO OFICIAL",
                            "vinculo": entry['href'],
                            "datos": body[:200] + "..."
                        })
                except Exception as e:
                    continue
        return results

scout_engine = MaiaUltimateScout()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.run()
            session.modified = True
        elif action == 'limpiar':
            session.clear()
            return "<script>window.location='/';</script>"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA v13.5 - ESTRATEGIA SMR</title>
        <style>
            body { background:#000; color:#0f0; font-family:monospace; padding:30px; }
            .btn { background:#000; border:1px solid #0f0; color:#0f0; padding:20px; width:100%; cursor:pointer; font-weight:bold; }
            .btn:hover { background:#0f0; color:#000; }
            .ficha { border:1px solid #333; padding:20px; margin-top:20px; border-left:4px solid #0f0; }
            .val { color:#ff0; font-size:16px; margin:10px 0; }
            a { color:#0ff; }
        </style>
    </head>
    <body>
        <form method="POST"><button type="submit" name="action" value="run_scout" class="btn">INICIAR ESCANEO DE CAPITAL SMR (USA 2026)</button></form>
        <form method="POST" style="margin-top:10px;"><button type="submit" name="action" value="limpiar" style="background:none; border:none; color:red; cursor:pointer;">[ REINICIAR SISTEMA ]</button></form>
        
        {% if not session['history'] %}
            <p style="text-align:center; color:#444; margin-top:50px;">ESPERANDO INSTRUCCIÓN DE BÚSQUEDA...</p>
        {% endif %}

        {% for r in session['history'] %}
        <div class="ficha">
            <div style="font-size:14px; font-weight:bold;">{{ r.nombre }}</div>
            <div class="val">VALOR DETECTADO: {{ r.valor }}</div>
            <div style="color:#888; font-size:11px;">{{ r.datos }}</div>
            <br><a href="{{ r.vinculo }}" target="_blank">[ VER FUENTE OFICIAL ]</a>
        </div>
        {% endfor %}
    </body>
    </html>
    """, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
