# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    view = request.form.get('view', 'projects')
    query = request.form.get('search_query', '').upper()
    scout_data = get_market_scout() if view == 'scout' else []

    h = f"""
    <html><head><title>MAIA FKT - SISTEMA CENTRAL</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px; cursor:pointer; font-weight:bold; font-size:11px; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; box-shadow: inset 0 0 5px #0f0; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap:20px; }}
        .card-scout {{ border:1px solid #0f05; background:rgba(0,50,0,0.1); padding:15px; position:relative; }}
        
        .risk-BAJO {{ color: #0f0; }}
        .risk-MEDIO {{ color: #ff0; }}
        .risk-ALTO {{ color: #f00; }}
        .risk-MÍNIMO {{ color: #0ff; }}

        .bar-bg {{ background:#111; height:4px; width:100%; margin-top:10px; }}
        .bar-fill {{ background:#0f0; height:100%; }}
        
        .search-box {{ background:#000; border:1px solid #f0f; color:#0ff; padding:12px; width:100%; max-width:400px; }}
        .result-box {{ border: 1px solid #0ff; padding: 20px; margin-top: 20px; background: rgba(0,255,255,0.05); }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; letter-spacing:2px; color:#f0f;">MAIA FKT</h1>
                <small style="color:#666;">GESTIÓN DE ACTIVOS & INGENIERÍA</small>
            </div>
            <div style="display:flex; gap:10px;">
                <form method="post" style="margin:0;">
                    <input type="hidden" name="view" value="scout">
                    <button type="submit" class="btn btn-scout">EJECUTAR SCOUT [ON]</button>
                </form>
                <button class="btn" style="border-color:#f0f; color:#f0f;" onclick="window.location.href='/'">RESETEAR CONSOLA</button>
            </div>
        </div>

        { f'<div class="grid">' + "".join([f'''
        <div class="card-scout">
            <small style="color:#0f0;">ID: {a['id']}</small><br>
            <b style="font-size:1.1em;">{a['Nombre']}</b><br>
            <span style="font-size:0.9em;">TIPO: {a['Tipo']}</span><br>
            <hr style="border:0; border-top:1px solid #0f02;">
            <span>UBICACIÓN: {a['Ubicación']}</span><br>
            <span>VALOR: <b>{a['Valor_Est']}</b></span> | RIESGO: <b class="risk-{a['Riesgo']}">{a['Riesgo']}</b>
            <div class="bar-bg"><div class="bar-fill" style="width:{a['Viabilidad']}%"></div></div>
        </div>
        ''' for a in scout_data]) + '</div>' if view == 'scout' else '' }

        <div style="margin-top:40px;">
            <h3 style="color:#f0f;">BUSCADOR DE PROYECTOS DE INGENIERÍA</h3>
            <form method="post">
                <input name="search_query" class="search-box" placeholder="Ej: MAIA II, EKF, SENSORES..." value="{query}">
                <button type="submit" class="btn" style="border-color:#f0f; color:#f0f;">BUSCAR</button>
            </form>
            
            {f'''
            <div class="result-box">
                <h4 style="color:#f0f; margin-top:0;">[+] REPORTE DE BÚSQUEDA: {query}</h4>
                <p><b>Estado:</b> Accediendo a Repositorio Externo...</p>
                <p><b>Estructura Detectada:</b> Arquitectura de 14 Nodos de Ingeniería.</p>
                <ul style="color:#0f0; font-size:12px;">
                    <li>Nodo 01: HARDWARE ABSTRACTION LAYER (HAL)</li>
                    <li>Nodo 02: CONTROL & ATTITUDE (EKF FUSION)</li>
                    <li>Nodo 03: NAVIGATION (A-STAR 3D)</li>
                    <li>Nodo 07: RADIOMETRIC THERMAL PROCESSING</li>
                </ul>
                <small style="color:#666;">Sincronizado con maia-ii.render.com</small>
            </div>
            ''' if query else ''}
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)