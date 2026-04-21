# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    view = request.form.get('view', 'init')
    target_country = request.form.get('target_country', 'TODOS')
    all_data = get_market_scout()
    
    # Extraer ubicaciones únicas para el selector
    locations = sorted(list(set([a['Ubicación'] for a in all_data])))
    
    results = []
    if view == 'scout':
        results = all_data if target_country == 'TODOS' else [a for a in all_data if a['Ubicación'] == target_country]
    elif view == 'clear':
        results = []

    h = f"""
    <html><head><title>MAIA FKT - SISTEMA GLOBAL</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px; cursor:pointer; font-weight:bold; font-size:11px; text-transform:uppercase; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; background:rgba(0,255,0,0.05); min-width:120px; }}
        .btn-clear {{ border-color:#f0f; color:#f0f; }}
        .btn-memory {{ border-color:#0ff; color:#0ff; font-size:9px; padding:6px; margin-top:10px; cursor:pointer; display:inline-block; }}
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap:20px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,50,0,0.15); padding:20px; position:relative; }}
        .tag-potencia {{ position:absolute; top:10; right:10; background:#f0f; color:#000; padding:2px 8px; font-weight:bold; font-size:12px; }}
        select {{ background:#000; border:1px solid #f0f; color:#0ff; padding:10px; outline:none; }}
        .contact-box {{ background:rgba(0,255,255,0.05); border:1px dashed #0ff4; padding:10px; margin-top:15px; font-size:12px; }}
    </style>
    <script>function saveMem(id){{ alert("DATOS DE " + id + " SINCRONIZADOS A MEMORIA CENTRAL"); }}</script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; letter-spacing:2px; color:#f0f;">MAIA FKT</h1>
                <small style="color:#666;">TERMINAL SCOUT: MUNDO</small>
            </div>
            
            <div style="display:flex; gap:10px;">
                <form method="post" style="display:flex; gap:10px; margin:0;">
                    <input type="hidden" name="view" value="scout">
                    <select name="target_country">
                        <option value="TODOS">TODOS LOS PAÍSES</option>
                        {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in locations])}
                    </select>
                    <button type="submit" class="btn btn-scout">EJECUTAR BUSCAR</button>
                </form>
                
                <form method="post" style="margin:0;">
                    <input type="hidden" name="view" value="clear">
                    <button type="submit" class="btn btn-clear">LIMPIAR PANTALLA</button>
                </form>
            </div>
        </div>

        <div class="grid">
        {"".join([f'''
        <div class="card">
            <div class="tag-potencia">POTENCIA: {a['Potencia']}</div>
            <small style="color:#0f0;">ID: {a['id']} | FUENTE: {a['Fuente']}</small><br>
            <b style="font-size:1.4em; color:#fff;">{a['Nombre']}</b><br>
            <p style="margin:15px 0;">
                <b>NEGOCIO:</b> {a['Detalle']}<br>
                <b>UBICACIÓN:</b> {a['Ubicación']}
            </p>
            <div style="display:flex; justify-content:space-between;">
                <span>VALOR: <b>{a['Valor_Est']}</b></span>
                <span style="color:#ff0;">VIABILIDAD: {a['Viabilidad']}%</span>
            </div>
            <div class="contact-box">
                <b>CONTACTO:</b> {a['Contacto']}<br>
                <b style="color:#f0f;">VIGENCIA:</b> {a['Vigencia']}
            </div>
            <div class="btn-memory" onclick="saveMem('{a['id']}')">GUARDAR EN MEMORIA [+]</div>
        </div>
        ''' for a in results])}
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
