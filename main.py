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
    countries = sorted(list(set([a['Ubicación'] for a in all_data])))
    
    # Lógica de filtrado
    results = []
    if view == 'scout':
        results = all_data if target_country == 'TODOS' else [a for a in all_data if a['Ubicación'] == target_country]

    h = f"""
    <html><head><title>MAIA FKT - SISTEMA SCOUT</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px; cursor:pointer; font-weight:bold; font-size:11px; text-transform:uppercase; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; background:rgba(0,255,0,0.05); }}
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap:20px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,50,0,0.15); padding:20px; position:relative; border-radius:4px; }}
        .tag-potencia {{ position:absolute; top:10; right:10; background:#f0f; color:#000; padding:2px 8px; font-weight:bold; font-size:12px; }}
        .risk-BAJO {{ color: #0f0; }} .risk-MEDIO {{ color: #ff0; }} .risk-ALTO {{ color: #f00; }}
        .contact-box {{ background:rgba(0,255,255,0.1); border:1px dashed #0ff; padding:10px; margin-top:15px; }}
        select {{ background:#000; border:1px solid #f0f; color:#0ff; padding:10px; outline:none; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; letter-spacing:2px; color:#f0f;">MAIA FKT</h1>
                <small style="color:#666;">INTELIGENCIA DE MERCADO ENERGÉTICO</small>
            </div>
            <form method="post" style="display:flex; gap:10px; margin:0; align-items:center;">
                <input type="hidden" name="view" value="scout">
                <select name="target_country">
                    <option value="TODOS">TODOS LOS PAÍSES</option>
                    {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in countries])}
                </select>
                <button type="submit" class="btn btn-scout">EJECUTAR SCOUT GLOBAL</button>
            </form>
        </div>

        <div class="grid">
        {"".join([f'''
        <div class="card">
            {f'<div class="tag-potencia">POTENCIA: {a.get("Potencia", "N/A")}</div>' if "Eléctrico" in a['Tipo'] else ""}
            <small style="color:#0f0;">ID: {a['id']} | {a['Tipo']}</small><br>
            <b style="font-size:1.3em; color:#fff;">{a['Nombre']}</b><br>
            
            <p style="margin:15px 0; font-size:0.95em;">
                <b>NEGOCIO:</b> {a['Detalle']}<br>
                <b>UBICACIÓN:</b> {a['Ubicación']}
            </p>

            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span>VALOR: <b>{a['Valor_Est']}</b></span>
                <span>RIESGO: <b class="risk-{a['Riesgo']}">{a['Riesgo']}</b></span>
            </div>

            <div style="font-size:11px; color:#aaa; margin-bottom:5px;">VIABILIDAD TÉCNICA: {a['Viabilidad']}%</div>
            <div style="background:#111; height:4px; width:100%;"><div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div></div>
            
            <div class="contact-box">
                <b>CONTACTO:</b> {a['Contacto']}<br>
                <b style="color:#f0f;">VIGENCIA INFO:</b> {a['Vigencia']}
            </div>
        </div>
        ''' for a in results])}
        </div>

        {'' if results else '<div style="text-align:center; margin-top:100px; color:#333;"><h3>MAIA FKT: LISTO PARA RASTREO</h3><p>Seleccione origen y ejecute el botón Scout.</p></div>'}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
