# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, redirect, url_for
import os
from scout_engine import scout_engine

app = Flask(__name__)

# Memoria volátil (se limpia al reiniciar el servidor, ideal para desarrollo)
# En producción se conectaría a un archivo JSON o SQLite
MAIA_MEMORIA = []

@app.route('/', methods=['GET', 'POST'])
def home():
    target_country = request.form.get('target_country', 'TODOS')
    target_tech = request.form.get('target_tech', 'TODAS')
    chat_query = request.form.get('chat_query', '')
    action = request.form.get('action', '')
    
    results = []
    if action == 'buscar_scout':
        results = scout_engine.execute_scout(target_country, target_tech)
    
    # Lógica para guardar en Memoria
    if action == 'guardar_memoria':
        ficha_data = request.form.to_dict()
        if ficha_data not in MAIA_MEMORIA:
            MAIA_MEMORIA.append(ficha_data)

    chat_response = ""
    if chat_query:
        chat_response = f"MAIA ANALYZER: Procesando '{chat_query}'. Los datos guardados en Memoria ahora suman {len(MAIA_MEMORIA)} activos."

    h = f"""
    <html><head><title>MAIA FKT - OS</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:20px; display:flex; justify-content:space-between; }}
        .nav {{ margin-bottom:20px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:8px 12px; cursor:pointer; font-weight:bold; font-size:11px; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-mem {{ border-color:#f0f; color:#f0f; }}
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); gap:20px; }}
        .card {{ border:1px solid #0f03; background:rgba(0,30,0,0.1); padding:20px; border-radius:5px; position:relative; }}
        .tag-date {{ position:absolute; top:10; right:10; font-size:10px; color:#666; }}
        .contact-box {{ background:rgba(0,255,255,0.05); padding:10px; margin-top:10px; font-size:11px; }}
        
        #maia-chat {{ position:fixed; bottom:20px; right:20px; width:300px; border:1px solid #f0f; background:#000; z-index:1000; }}
        .chat-h {{ background:#f0f; color:#000; padding:10px; font-weight:bold; cursor:pointer; }}
        .chat-b {{ padding:15px; display:block; }}
    </style>
    </head><body>
        <div class="header">
            <h1 style="margin:0; color:#f0f;">MAIA FKT <span style="font-size:12px; color:#555;">// INTELLIGENCE UNIT</span></h1>
            <a href="/memoria" class="btn btn-mem">VER MEMORIA ({len(MAIA_MEMORIA)})</a>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 150px; gap:10px; margin-bottom:30px;">
            <input name="target_country" placeholder="PAÍS" value="{target_country if target_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS">-- TECNOLOGÍAS --</option>
                <option value="SMR Nuclear">SMR Nuclear</option>
                <option value="Hidrógeno Verde">Hidrógeno Verde</option>
                <option value="Neutrinos">Neutrinos</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">SCOUT</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card">
                <div class="tag-date">PUB: {a['Fecha_Pub']}</div>
                <small style="color:#0f0;">{a['id']} | {a['Tecnología']}</small>
                <h3 style="color:#fff; margin:5px 0;">{a['Nombre']}</h3>
                <p style="font-size:12px; color:#ccc;">{a['Resumen']}</p>
                <div class="contact-box">
                    CEO: {a['CEO']} | FUENTE: <b style="color:#f0f;">{a['Fuente']}</b><br>
                    <a href="{a['Contacto']}" target="_blank" style="color:#0ff;">ENLACE DIRECTO</a>
                </div>
                <form method="post" style="margin-top:10px;">
                    <input type="hidden" name="id" value="{a['id']}">
                    <input type="hidden" name="Nombre" value="{a['Nombre']}">
                    <input type="hidden" name="Tecnología" value="{a['Tecnología']}">
                    <input type="hidden" name="Fuente" value="{a['Fuente']}">
                    <button type="submit" name="action" value="guardar_memoria" class="btn btn-mem" style="width:100%;">+ MEMORIA</button>
                </form>
            </div>
            ''' for a in results])}
        </div>

        <div id="maia-chat">
            <div class="chat-h" onclick="document.getElementById('cb').style.display='none'">MAIA II ANALYZER</div>
            <div id="cb" class="chat-b">
                <p style="font-size:11px; color:#0f0;">{chat_response if chat_response else 'Esperando órdenes...'}</p>
                <form method="post">
                    <input name="chat_query" placeholder="Consulta..." style="width:100%; background:#000; border:1px solid #0ff; color:#0ff; padding:5px;">
                </form>
            </div>
        </div>
    </body></html>
    """
    return render_template_string(h)

@app.route('/memoria')
def memoria():
    h = f"""
    <html><head><title>MAIA - MEMORIA</title>
    <style>
        body {{ background:#000; color:#f0f; font-family:monospace; padding:20px; }}
        .card {{ border:1px solid #f0f; padding:15px; margin-bottom:10px; background:rgba(255,0,255,0.05); }}
        .btn {{ border:1px solid #0ff; color:#0ff; text-decoration:none; padding:10px; display:inline-block; margin-bottom:20px; }}
    </style>
    </head><body>
        <h1>MEMORIA DE ACTIVOS MAIA FKT</h1>
        <a href="/" class="btn">VOLVER A CONSOLA</a>
        {"".join([f'<div class="card"><b>{m["Nombre"]}</b> - {m["Tecnología"]} <br> <small>FUENTE: {m["Fuente"]}</small></div>' for m in MAIA_MEMORIA])}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
