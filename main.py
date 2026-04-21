# -*- coding: utf-8 -*-
# main.py - CONSOLA DE CONTROL MAIA II (V.5 BUIDER READY)
# ESTADO: BLINDAJE NIVEL 5 - CONTROLADORES AISLADOS

from flask import Flask, render_template_string, request, redirect, url_for
import os
from scout_engine import scout_engine
from builder_engine import builder_engine

app = Flask(__name__)
MAIA_MEMORIA = []

@app.route('/', methods=['GET', 'POST'])
def home():
    t_country = request.form.get('target_country', 'TODOS')
    t_tech = request.form.get('target_tech', 'TODAS')
    action = request.form.get('action', '')
    
    results = []
    if action == 'buscar_scout':
        results = scout_engine.execute_brutal_search(t_country, t_tech)
    
    if action == 'guardar_memoria':
        ficha = request.form.to_dict()
        if ficha not in MAIA_MEMORIA: MAIA_MEMORIA.append(ficha)

    # UI CON BOTÓN DE NUEVO PROYECTO
    h = f"""
    <html><head><title>MAIA FKT - COMMAND CENTER</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; }}
        .header {{ border-bottom:3px solid #f0f; padding-bottom:15px; margin-bottom:30px; display:flex; justify-content:space-between; }}
        .btn {{ background:none; border:2px solid #0ff; color:#0ff; padding:12px; cursor:pointer; font-weight:bold; text-decoration:none; display:inline-block; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-magenta {{ border-color:#f0f; color:#f0f; }}
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr)); gap:25px; }}
        .card {{ border:1px solid #0f02; background:rgba(0,30,0,0.1); padding:25px; border-left: 6px solid #0f0; }}
        input, select {{ background:#000; border:1px solid #0ff; color:#0ff; padding:12px; width:100%; margin-bottom:10px; }}
        #maia-chat {{ position:fixed; bottom:20px; right:20px; width:350px; border:2px solid #f0f; background:#000; }}
        .chat-h {{ background:#f0f; color:#000; padding:12px; font-weight:bold; cursor:pointer; }}
        .minimized {{ height: 45px; overflow:hidden; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f;">MAIA FKT <span style="font-size:12px; color:#555;">// V.5</span></h1>
                <b style="color:#0f0;">SISTEMA BLINDADO: MÓDULOS AISLADOS</b>
            </div>
            <div>
                <a href="/builder" class="btn btn-green">+ NUEVO PROYECTO</a>
                <a href="/memoria" class="btn btn-magenta">MEMORIA ({len(MAIA_MEMORIA)})</a>
            </div>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 150px; gap:10px; margin-bottom:40px;">
            <input name="target_country" placeholder="UBICACIÓN" value="{t_country if t_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS">-- TECNOLOGÍAS --</option>
                <option value="SMR Nuclear">SMR Nuclear</option>
                <option value="Hidrógeno Verde">Hidrógeno Verde</option>
                <option value="Neutrinos">Neutrinos</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card">
                <small style="color:#0f0;">{a['id']}</small>
                <h2 style="color:#fff;">{a['Nombre']}</h2>
                <p style="color:#bbb; font-size:12px;">{a['Resumen']}</p>
                <button class="btn btn-magenta" style="width:100%;">SINCRONIZAR</button>
            </div>
            ''' for a in results])}
        </div>

        <div id="maia-chat" class="minimized" onclick="this.classList.toggle('minimized')">
            <div class="chat-h">MAIA II ANALYZER [+/-]</div>
            <div style="padding:15px;">Consola lista para integración de modelo financiero...</div>
        </div>
    </body></html>
    """
    return render_template_string(h)

@app.route('/builder', methods=['GET', 'POST'])
def builder():
    # Esta ruta llama exclusivamente al motor del constructor
    form_html = builder_engine.generate_form_html()
    h = f"""
    <html><body style="background:#000; color:#0f0; font-family:monospace; padding:40px;">
        <h1 style="color:#f0f;">MAIA PROJECT BUILDER</h1>
        <p>Cargue los datos del modelo financiero para generar la viabilidad técnica.</p>
        <form style="max-width:600px;">
            {form_html}
            <button type="button" class="btn btn-green" style="border:1px solid #0f0; color:#0f0; padding:10px; margin-top:20px; background:none;">SIMULAR PROYECTO</button>
        </form>
        <br><a href="/" style="color:#0ff;">VOLVER A CONSOLA</a>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)