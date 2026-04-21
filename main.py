# -*- coding: utf-8 -*-
# main.py - Orquestador de Gestión MAIA FKT
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    view = request.form.get('view', 'projects')
    query = request.form.get('search_query', '')
    
    # Carga de datos del motor Scout si se activa
    scout_data = get_market_scout() if view == 'scout' else []

    h = f"""
    <html><head><title>MAIA FKT - CONTROL</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; line-height:1.5; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; }}
        .nav {{ display:flex; gap:15px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px 20px; cursor:pointer; font-weight:bold; text-transform:uppercase; font-size:11px; }}
        .btn:hover {{ background:rgba(0,255,255,0.1); }}
        .btn-scout {{ border-color:#0f0; color:#0f0; }}
        .btn-scout:hover {{ background:rgba(0,255,0,0.1); box-shadow: 0 0 10px #0f0; }}
        .card {{ border-left:4px solid #0f0; background:rgba(0,255,0,0.05); padding:15px; margin-top:10px; border-radius:0 5px 5px 0; }}
        .search-box {{ background:#000; border:1px solid #f0f; color:#0ff; padding:12px; width:350px; outline:none; }}
        .status-bar {{ position:fixed; bottom:0; left:0; width:100%; background:#f0f; color:#000; padding:3px 20px; font-size:10px; font-weight:bold; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; letter-spacing:2px; color:#f0f;">MAIA FKT</h1>
                <small style="color:#666;">CENTRAL DE GESTIÓN // ALEX PROTOCOL</small>
            </div>
            <div class="nav">
                <form method="post" style="margin:0;">
                    <input type="hidden" name="view" value="scout">
                    <button type="submit" class="btn btn-scout">EJECUTAR SCOUT</button>
                </form>
                <button class="btn" style="border-color:#0ff; color:#0ff;" onclick="window.location.href='/'">NUEVO PROYECTO</button>
            </div>
        </div>

        {"".join([f'''
        <div class="card">
            <b style="color:#0f0; font-size:1.2em;">ACTIVO DETECTADO: {a["Nombre"]}</b><br>
            <span style="color:#ccc;">UBICACIÓN: {a["Ubicación"]} | VALOR ESTIMADO: <b style="color:#fff;">{a["Valor_Est"]}</b></span>
        </div>
        ''' for a in scout_data])}

        <div style="margin-top:40px;">
            <h3 style="color:#f0f;">BUSCADOR DE PROYECTOS INGENIERÍA</h3>
            <form method="post" style="display:flex; gap:10px;">
                <input name="search_query" class="search-box" placeholder="Ingrese nombre del proyecto o ID..." value="{query}">
                <button type="submit" class="btn" style="border-color:#f0f; color:#f0f;">BUSCAR</button>
            </form>
            {f'<div style="margin-top:20px; color:#0f0;">[+] Resultados para: "{query}" ... Repositorio MAIA II vinculado.</div>' if query else ''}
        </div>

        <div class="status-bar">SISTEMA OPERATIVO - CONSOLA DE GESTIÓN PURIFICADA</div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)