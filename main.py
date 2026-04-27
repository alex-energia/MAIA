# -*- coding: utf-8 -*-
import os
import time
import re
import sys
from flask import Flask, render_template_string, request, session
from duckduckgo_search import DDGS

# --- NÚCLEO DE INTELIGENCIA MAIA v13.0 (USA SMR EDITION) ---
class MaiaDeepSearch:
    def __init__(self):
        # Configuración para SMR en USA (Gratuito y Real)
        self.pilar = "SMR Nuclear United States"
        self.trash = ["wikipedia", "news", "reuters", "bloomberg", "noticias", "youtube", "dictionary"]

    def execute_global_scout(self):
        results = []
        # Queries de alta intención transaccional para USA
        queries = [
            f'site:gov "SMR" contract award 2026 "USD"',
            f'site:energy.gov "small modular reactor" funding announcement 2026',
            f'intitle:"tender" "SMR" USA 2026 million'
        ]

        print(f"\n[SISTEMA] Iniciando rastreo profundo en nodos de USA...")
        
        with DDGS() as ddgs:
            for q in queries:
                try:
                    # Pausa humana para evitar bloqueos de IP (Crucial para sitios .gov)
                    time.sleep(5) 
                    search_data = list(ddgs.text(q, max_results=4))
                    
                    if not search_data:
                        continue

                    for entry in search_data:
                        body = entry.get('body', '').lower()
                        title = entry.get('title', '').upper()
                        url = entry.get('href', '')

                        # Solo procesamos si hay indicios de capital o contratos
                        if any(k in body for k in ["$", "million", "award", "contract", "funding"]):
                            # Extracción de montos y contactos mediante lógica de IA
                            val = re.search(r'(\$[0-9,.]+ ?(million|billion|M|B|USD))', body, re.I)
                            mail = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', body)
                            
                            results.append({
                                "id": f"USA-SMR-{int(time.time())}-{len(results)}",
                                "pilar": "NUCLEAR SMR / USA",
                                "nombre": title,
                                "valor": val.group(0).upper() if val else "VERIFICAR EN EXPEDIENTE FEDERAL",
                                "potencia": "Escala Industrial SMR (300MW+)",
                                "ubicacion": "NODO USA / FEDERAL",
                                "contacto": f"{mail.group(0) if mail else 'Consultar en portal DOE'}",
                                "vinculo": url,
                                "datos": body[:300] + "..."
                            })
                except Exception as e:
                    print(f"[!] Error de conexión en nodo: {e}")
                    continue
        
        return results

# --- INTERFAZ MAIA v13.0 ---
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
            # Ejecuta la búsqueda real 100% web
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
        <title>MAIA v13 - USA BUSINESS INTELLIGENCE</title>
        <style>
            :root { --cian: #00ffff; --gold: #ffd700; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:monospace; padding:20px; font-size:12px; }
            .nav { border-bottom: 2px solid #111; padding-bottom:15px; display:flex; gap:10px; margin-bottom:20px; }
            .btn-nav { background:none; border:1px solid #333; color:#555; padding:8px 15px; cursor:pointer; }
            .active { border-color:var(--cian); color:var(--cian); }
            .btn-scan { background:#000; border:2px solid var(--cian); color:var(--cian); padding:25px; width:100%; cursor:pointer; font-weight:bold; font-size:18px; text-transform:uppercase; letter-spacing:2px; }
            .ficha { background:#050505; border:1px solid #111; border-left:5px solid var(--cian); padding:25px; margin-top:25px; }
            .title { font-size:17px; font-weight:bold; color:var(--cian); margin-bottom:15px; }
            .val-box { background:rgba(0,255,255,0.05); border:1px dashed var(--cian); padding:15px; margin:10px 0; font-size:16px; }
            .no-data { text-align:center; padding:60px; color:#333; border:1px dashed #222; margin-top:20px; font-size:14px; }
            a { color:var(--gold); text-decoration:none; font-weight:bold; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">BARRIDO REAL 2026</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">ARCHIVO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; color:#ff3366;">WIPE SYSTEM</button>
            </form>
        </div>

        {% if view == 'scout' %}
            <form method="POST">
                <input type="hidden" name="action" value="run_scout">
                <button type="submit" class="btn-scan">EJECUTAR ESCANEO DE CAPITAL SMR (USA)</button>
            </form>

            {% if not session['history'] %}
                <div class="no-data">SISTEMA SIN HALLAZGOS EN MEMORIA.<br>PRESIONE EJECUTAR PARA INICIAR RASTREO FEDERAL.</div>
            {% endif %}

            {% for r in session['history'] %}
            <div class="ficha">
                <div style="color:var(--gold); font-size:10px; margin-bottom:5px;">{{ r.pilar }}</div>
                <div class="title">{{ r.nombre }}</div>
                <div class="val-box"><b>VALOR ADJUDICADO:</b> {{ r.valor }}</div>
                <div style="margin:15px 0;">
                    <b>UBICACIÓN:</b> {{ r.ubicacion }} | <b>POTENCIA:</b> {{ r.potencia }}<br>
                    <b>CONTACTO DETECTADO:</b> <span style="color:#fff;">{{ r.contacto }}</span>
                </div>
                <div style="color:#666; font-size:11px; margin-bottom:15px;">{{ r.datos }}</div>
                <div style="display:flex; gap:20px;">
                    <a href="{{ r.vinculo }}" target="_blank">[ IR AL PORTAL OFICIAL ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--cian); cursor:pointer; font-weight:bold;">[ GUARDAR ]</button></form>
                </div>
            </div>
            {% endfor %}
        {% else %}
            {% for s in session['saved'] %}
            <div class="ficha" style="border-left-color:var(--gold);">
                <div class="title" style="color:var(--gold);">{{ s.nombre }}</div>
                <div class="val-box"><b>VALOR:</b> {{ s.valor }}</div>
                <a href="{{ s.vinculo }}" target="_blank">[ VER FUENTE ]</a>
            </div>
            {% endfor %}
        {% endif %}
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)