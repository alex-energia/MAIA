# -*- coding: utf-8 -*-
import os
import time
import re
import sys
from flask import Flask, render_template_string, request, session
from duckduckgo_search import DDGS

# --- CLASE DEL MOTOR DE BÚSQUEDA (INTEGRADA) ---
class MaiaDeepSearch:
    def __init__(self):
        self.pilares = [
            "Energia hidroelectrica", "Startup de tecnologia", "SMR nuclear",
            "Solar", "Termica", "Geotermica", "Neutrinos", "Hidrogeno"
        ]
        self.trash = ["wikipedia", "news", "reuters", "bloomberg", "noticias", "youtube", "dictionary", "britannica"]
        self.targets = "(.gov OR .sa OR .ae OR .sg OR .cl OR .co OR crunchbase.com OR angel.co)"

    def execute_global_scout(self):
        results = []
        with DDGS() as ddgs:
            for pilar in self.pilares:
                # Query de IA Pura: Busca documentos y licitaciones reales
                query = f'"{pilar}" {self.targets} (intitle:tender OR "equity sale" OR "series B" OR licitacion) 2026 "USD" -{ " -".join(self.trash) }'
                try:
                    search_data = list(ddgs.text(query, max_results=5)) # 5 resultados para evitar bloqueos
                    for entry in search_data:
                        body = entry.get('body', '').lower()
                        # Solo aceptamos si hay rastro de dinero o capital
                        if any(k in body for k in ["$", "usd", "million", "billion", "equity", "round"]):
                            val = re.search(r'(\$[0-9,.]+ ?(million|billion|M|B|USD))', body, re.I)
                            pwr = re.search(r'([0-9,.]+ ?(MW|GW|MWh|kW))', body, re.I)
                            tel = re.search(r'(\+?[0-9]{1,4}[\s-]?\(?[0-9]{1,4}\)?[\s-]?[0-9]{3,8}[\s-]?[0-9]{3,8})', body)
                            mail = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', body)

                            results.append({
                                "id": f"TXN-{int(time.time())}-{len(results)}",
                                "pilar": pilar.upper(),
                                "nombre": entry['title'].upper(),
                                "valor": val.group(0).upper() if val else "VERIFICAR EN FUENTE",
                                "potencia": pwr.group(0).upper() if pwr else "VER ESPECIFICACIONES",
                                "ubicacion": "NODO INTERNACIONAL",
                                "contacto": f"{mail.group(0) if mail else 'Email en sitio'} / {tel.group(0) if tel else 'Tel. en sitio'}",
                                "vinculo": entry['href'],
                                "datos": body[:250] + "..."
                            })
                    time.sleep(1.5) # Delay de seguridad
                except: continue
        return results

# --- CONFIGURACIÓN DE LA INTERFAZ WEB ---
app = Flask(__name__)
app.secret_key = os.urandom(2048)
scout_engine = MaiaDeepSearch()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            # Ejecuta la búsqueda real. Si no hay internet o resultados, devuelve []
            res = scout_engine.execute_global_scout()
            session['history'] = res
            session.modified = True
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item); session.modified = True
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA v12.5 - LIVE BUSINESS SCOUT</title>
        <style>
            :root { --cian: #00ffff; --gold: #ffd700; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:monospace; padding:20px; }
            .nav { border-bottom: 2px solid #111; padding-bottom:15px; display:flex; gap:10px; margin-bottom:20px; }
            .btn-nav { background:none; border:1px solid #333; color:#555; padding:8px 15px; cursor:pointer; }
            .active { border-color:var(--cian); color:var(--cian); }
            .btn-scan { background:#000; border:2px solid var(--cian); color:var(--cian); padding:20px; width:100%; cursor:pointer; font-weight:bold; font-size:16px; }
            .ficha { background:#050505; border:1px solid #111; border-left:5px solid var(--cian); padding:20px; margin-top:20px; }
            .val-box { border:1px dashed var(--cian); padding:10px; margin:10px 0; color:var(--cian); font-size:16px; }
            .no-data { text-align:center; padding:40px; color:#444; border:1px dashed #222; margin-top:20px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">BARRIDO REAL</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">ARCHIVADOS</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="color:#ff3366;">WIPE</button>
            </form>
        </div>
        {% if view == 'scout' %}
            <form method="POST"><input type="hidden" name="action" value="run_scout"><button type="submit" class="btn-scan">INICIAR BÚSQUEDA DE ACTIVOS EN VIVO (2026)</button></form>
            {% if not session['history'] %}<div class="no-data">SISTEMA LISTO. PRESIONE INICIAR PARA RASTREO WEB.</div>{% endif %}
            {% for r in session['history'] %}
            <div class="ficha">
                <div style="color:var(--gold); font-size:10px;">{{ r.pilar }}</div>
                <div style="font-size:18px; color:var(--cian);">{{ r.nombre }}</div>
                <div class="val-box"><b>VALOR:</b> {{ r.valor }}</div>
                <div style="margin:10px 0;"><b>POTENCIA:</b> {{ r.potencia }} | <b>UBICACIÓN:</b> {{ r.ubicacion }}</div>
                <div style="color:#fff;"><b>CONTACTO:</b> {{ r.contacto }}</div>
                <div style="color:#666; font-size:11px; margin-top:10px;">{{ r.datos }}</div>
                <a href="{{ r.vinculo }}" target="_blank" style="color:var(--cian);">[ VER FUENTE ]</a>
            </div>
            {% endfor %}
        {% else %}
            {% for s in session['saved'] %}<div class="ficha" style="border-left-color:var(--gold);">{{ s.nombre }}</div>{% endfor %}
        {% endif %}
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)