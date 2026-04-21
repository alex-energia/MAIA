# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    view = request.form.get('view', 'projects')
    target_country = request.form.get('target_country', 'TODOS')
    
    # Obtener datos y filtrar
    all_data = get_market_scout()
    countries = sorted(list(set([a['Pais'] for a in all_data])))
    
    if view == 'scout':
        if target_country == 'TODOS':
            scout_results = all_data
        else:
            scout_results = [a for a in all_data if a['Pais'] == target_country]
    else:
        scout_results = []

    h = f"""
    <html><head><title>MAIA FKT - INTEL V2</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px; cursor:pointer; font-weight:bold; font-size:11px; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; box-shadow: inset 0 0 5px #0f0; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap:20px; }}
        .card-scout {{ border:1px solid #0f05; background:rgba(0,50,0,0.1); padding:15px; border-radius:5px; }}
        
        .risk-BAJO {{ color: #0f0; }} .risk-MEDIO {{ color: #ff0; }} .risk-ALTO {{ color: #f00; }} .risk-MÍNIMO {{ color: #0ff; }}

        .bar-bg {{ background:#111; height:4px; width:100%; margin:10px 0; }}
        .bar-fill {{ background:#0f0; height:100%; }}
        
        select, .search-box {{ background:#000; border:1px solid #f0f; color:#0ff; padding:12px; outline:none; }}
        .contact-box {{ background:rgba(0,255,255,0.1); border:1px dashed #0ff; padding:8px; margin-top:10px; font-size:12px; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; letter-spacing:2px; color:#f0f;">MAIA FKT</h1>
                <small style="color:#666;">INTELIGENCIA E INGENIERÍA // FILTRO GEOGRÁFICO</small>
            </div>
            <div style="display:flex; gap:10px; align-items:center;">
                <form method="post" style="display:flex; gap:10px; margin:0;">
                    <input type="hidden" name="view" value="scout">
                    <select name="target_country">
                        <option value="TODOS">-- SELECCIONAR PAÍS --</option>
                        {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in countries])}
                    </select>
                    <button type="submit" class="btn btn-scout">BUSCAR EN PAÍS</button>
                </form>
            </div>
        </div>

        {"<p style='color:#f0f;'>[+] RESULTADOS EN: " + target_country + "</p>" if view == 'scout' else ""}
        
        <div class="grid">
        {"".join([f'''
        <div class="card-scout">
            <small style="color:#0f0;">ID: {a['id']} | {a['Tipo']}</small><br>
            <b style="font-size:1.2em; color:#fff;">{a['Nombre']}</b><br>
            <p style="margin:10px 0; font-size:0.9em; color:#ccc;">
                <b>NEGOCIO:</b> {a['Detalle']}
            </p>
            <div style="display:flex; justify-content:space-between; font-size:0.9em;">
                <span>VALOR: {a['Valor_Est']}</span>
                <span>RIESGO: <b class="risk-{a['Riesgo']}">{a['Riesgo']}</b></span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:{a['Viabilidad']}%"></div></div>
            <div class="contact-box">
                <b style="color:#0ff;">CONTACTO DIRECTO:</b><br>{a['Contacto']}
            </div>
        </div>
        ''' for a in scout_results])}
        </div>

        <div style="margin-top:40px; border-top:1px solid #333; padding-top:20px;">
            <h3 style="color:#f0f;">CONSULTA DE REPOSITORIO MAIA II</h3>
            <p style="font-size:12px; color:#666;">Ingrese términos de ingeniería para validar contra nodos remotos.</p>
            <form method="post">
                <input name="search_query" class="search-box" style="width:300px;" placeholder="Ej: EKF, A-Star, PCL...">
                <button type="submit" class="btn" style="border-color:#f0f; color:#f0f;">CONSULTAR</button>
            </form>
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)