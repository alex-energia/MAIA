# -*- coding: utf-8 -*-
import os
import time
from flask import Flask, render_template_string, request, session
# IMPORTANTE: Asegúrate de que el archivo scout_engine.py esté en la misma carpeta
from scout_engine import scout_engine 

app = Flask(__name__)
app.secret_key = os.urandom(2048)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            # EJECUCIÓN DEL MOTOR DE BÚSQUEDA TRANSACCIONAL REAL
            # Aquí no hay datos guardados; o encuentra en la web o devuelve vacío.
            raw_results = scout_engine.execute_global_scout()
            
            # Convertimos el formato del motor al formato de la interfaz Flask
            processed = []
            if raw_results:
                for r in raw_results:
                    processed.append({
                        "id": r['id'],
                        "nombre": r['nombre'],
                        "pilar": r['pilar'],
                        "valor": r['valor_inversion'],
                        "potencia": r['potencia'],
                        "ubicacion": r['ubicacion'],
                        "riesgo": r['riesgo'],
                        "contacto": f"{r['contacto_directo']['email']} / {r['contacto_directo']['tel']}",
                        "vinculo": r['contacto_directo']['web'],
                        "datos": r['extracto']
                    })
            
            session['history'] = processed
            session.modified = True
            
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item)
                session.modified = True
        elif action == 'limpiar':
            session.clear()
            return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA v12 - AI BUSINESS SCOUT</title>
        <style>
            :root { --cian: #00ffff; --gold: #ffd700; --red: #ff3366; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:monospace; padding:20px; font-size:12px; }
            .nav { border-bottom: 2px solid #111; padding-bottom:15px; display:flex; gap:10px; margin-bottom:20px; }
            .btn-nav { background:none; border:1px solid #333; color:#555; padding:8px 15px; cursor:pointer; }
            .active { border-color:var(--cian); color:var(--cian); }
            .btn-scan { background:#000; border:2px solid var(--cian); color:var(--cian); padding:25px; width:100%; cursor:pointer; font-weight:bold; font-size:18px; text-transform:uppercase; letter-spacing:2px; }
            .ficha { background:#050505; border:1px solid #111; border-left:5px solid var(--cian); padding:25px; margin-top:25px; }
            .title { font-size:19px; margin:10px 0; font-weight:bold; color:var(--cian); }
            .tech-table { width:100%; border-collapse: collapse; margin:15px 0; }
            .tech-table td { border: 1px solid #1a1a1a; padding: 12px; vertical-align: top; }
            .tech-table b { color:var(--gold); display:block; margin-bottom:5px; font-size:10px; text-transform:uppercase; }
            .val-box { background:rgba(0,255,255,0.05); border:1px dashed var(--cian); padding:15px; margin:10px 0; }
            .val-box b { color:var(--cian); }
            .no-data { text-align:center; padding:50px; color:#333; border:1px dashed #222; margin-top:20px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">BARRIDO REAL 2026</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">ARCHIVADOS ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; color:var(--red);">WIPE SYSTEM</button>
            </form>
        </div>

        {% if view == 'scout' %}
            <form method="POST">
                <input type="hidden" name="action" value="run_scout">
                <button type="submit" class="btn-scan">INICIAR BÚSQUEDA DE ACTIVOS EN VIVO</button>
            </form>

            {% if not session['history'] %}
                <div class="no-data">NO HAY DATOS EN MEMORIA. PRESIONE EJECUTAR PARA ESCANEAR LA RED.</div>
            {% endif %}

            {% for r in session['history'] %}
            <div class="ficha">
                <div style="color:var(--gold); font-size:10px;">{{ r.pilar }}</div>
                <div class="title">{{ r.nombre }}</div>
                <div class="val-box">
                    <b>VALOR ESTIMADO:</b>
                    <span style="font-size:18px; color:#fff;">{{ r.valor }}</span>
                </div>
                <table class="tech-table">
                    <tr>
                        <td><b>POTENCIA:</b>{{ r.potencia }}</td>
                        <td><b>LOCALIZACIÓN:</b>{{ r.ubicacion }}</td>
                    </tr>
                    <tr>
                        <td><b>CALIFICACIÓN RIESGO:</b>{{ r.riesgo }}</td>
                        <td><b>CONTACTO:</b><span style="color:#fff;">{{ r.contacto }}</span></td>
                    </tr>
                </table>
                <div style="color:#666; font-size:11px; margin-bottom:15px; border-top:1px solid #111; padding-top:10px;">{{ r.datos }}</div>
                <div style="display:flex; gap:15px;">
                    <a href="{{ r.vinculo }}" target="_blank" style="color:var(--cian); text-decoration:none; font-weight:bold;">[ VER FUENTE ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--gold); cursor:pointer; font-weight:bold;">[ ARCHIVAR ]</button></form>
                </div>
            </div>
            {% endfor %}
        {% else %}
            {% for s in session['saved'] %}
            <div class="ficha" style="border-left-color:var(--gold);">
                <div class="title" style="color:var(--gold);">{{ s.nombre }}</div>
                <div class="val-box"><b>VALOR REGISTRADO:</b> {{ s.valor }}</div>
                <div style="color:#999;">{{ s.datos }}</div>
            </div>
            {% endfor %}
        {% endif %}
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
