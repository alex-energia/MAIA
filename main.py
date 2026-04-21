# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    view = request.form.get('view', 'scout')
    action = request.form.get('action', '')
    target_country = request.form.get('target_country', 'TODOS')
    target_tech = request.form.get('target_tech', 'TODAS')
    chat_query = request.form.get('chat_query', '')
    
    all_data = get_market_scout()
    locations = sorted(list(set([a['Ubicación'] for a in all_data])))
    techs = sorted(list(set([a['Tecnología'] for a in all_data])))
    
    results = []
    chat_response = ""
    
    if view == 'scout':
        if action == 'buscar_scout':
            results = all_data
            if target_country != 'TODOS':
                results = [a for a in results if a['Ubicación'] == target_country]
            if target_tech != 'TODAS':
                results = [a for a in results if a['Tecnología'] == target_tech]
        elif action == 'limpiar':
            results = []

        if chat_query:
            q = chat_query.lower()
            matches = [a['Nombre'] for a in all_data if q in a['Resumen'].lower() or q in a['Tecnología'].lower()]
            chat_response = f"MAIA ANALYZER: Relevancia en: {', '.join(matches)}" if matches else "MAIA: No hay coincidencias."

    h = f"""
    <html><head><title>MAIA FKT - DEEP TECH SYSTEM</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:1px solid #f0f; padding-bottom:10px; margin-bottom:20px; }}
        .nav {{ display:flex; gap:10px; margin-bottom:20px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:8px 15px; cursor:pointer; font-weight:bold; font-size:10px; text-transform:uppercase; }}
        .btn-active {{ background:#0ff; color:#000; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap:15px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,30,0,0.15); padding:15px; border-radius:5px; position:relative; }}
        .tag-ia {{ position:absolute; top:10; right:10; color:#f0f; border:1px solid #f0f; padding:2px 6px; font-size:9px; font-weight:bold; }}
        
        /* Etiquetas de Riesgo */
        .riesgo-BAJO {{ color: #0f0; }}
        .riesgo-MODERADO {{ color: #ff0; }}
        .riesgo-ALTO {{ color: #f90; }}
        .riesgo-CRÍTICO {{ color: #f00; font-weight:bold; }}
        .riesgo-MUY-ALTO {{ color: #f0f; }}

        input, select, textarea {{ background:#000; border:1px solid #0ff; color:#0ff; padding:10px; width:100%; margin-bottom:10px; outline:none; font-size:11px; }}
        .contact-details {{ background:rgba(0,255,255,0.05); border-top:1px solid #0ff3; padding:10px; margin-top:10px; font-size:10px; line-height:1.5; }}
        .chat-box {{ border:1px solid #f0f; background:rgba(255,0,255,0.05); padding:15px; margin-top:25px; }}
    </style>
    </head><body>
        <div class="header">
            <h1 style="margin:0; color:#f0f; letter-spacing:1px;">MAIA FKT <span style="font-size:12px; color:#666;">// DEEP TECH OS</span></h1>
            <div style="font-size:10px; color:#0f0; text-align:right;">MONITOREO DE NEUTRINOS & SMR ACTIVO</div>
        </div>

        <div class="nav">
            <form method="post" style="margin:0;"><input type="hidden" name="view" value="scout"><button type="submit" class="btn {'btn-active' if view=='scout' else ''}">🔍 AGENTE SCOUT</button></form>
            <form method="post" style="margin:0;"><input type="hidden" name="view" value="nuevo"><button type="submit" class="btn {'btn-active' if view=='nuevo' else ''}">🏗️ AGENTE CONSTRUCTOR</button></form>
        </div>

        {f'''
        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 100px 100px; gap:10px; margin-bottom:20px;">
            <input type="hidden" name="view" value="scout">
            <select name="target_country">
                <option value="TODOS">-- TODOS LOS PAÍSES --</option>
                {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in locations])}
            </select>
            <select name="target_tech">
                <option value="TODAS">-- TODAS LAS TECNOLOGÍAS --</option>
                {" ".join([f'<option value="{t}" {"selected" if t==target_tech else ""}>{t.upper()}</option>' for t in techs])}
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-scout">SCOUT</button>
            <button type="submit" name="action" value="limpiar" class="btn" style="border-color:#f0f; color:#f0f;">CLEAR</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card">
                <div class="tag-ia">CALIF. IA: {a['Calificacion_IA']}</div>
                <small style="color:#0f0;">ID: {a['id']} | TECNOLOGÍA: <span style="color:#fff;">{a['Tecnología']}</span></small><br>
                <b style="font-size:1.3em; color:#fff;">{a['Nombre']}</b><br>
                
                <p style="margin:10px 0; font-size:11px; color:#ccc;"><b>RESUMEN:</b> {a['Resumen']}</p>
                
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px;">
                    <span>VALOR: <b>{a['Valor_Est']}</b></span>
                    <span class="riesgo-{a['Riesgo'].replace(' ','-')}">RIESGO: {a['Riesgo']}</span>
                </div>
                
                <div style="background:#111; height:3px; width:100%; margin-bottom:10px;"><div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div></div>

                <div class="contact-details">
                    <b style="color:#0ff;">DIRECTORIO EJECUTIVO:</b><br>
                    CEO: {a['CEO']} | CEL: {a['Celular']}<br>
                    DIR: {a['Dirección']}<br>
                    MAIL: {a['Contacto']} | <b style="color:#f0f;">{a['Fuente']}</b>
                </div>
            </div>
            ''' for a in results])}
        </div>
        ''' if view == 'scout' else ''}

        {f'''
        <div style="max-width:600px; border:1px solid #f0f; padding:25px; background:rgba(255,0,255,0.05); margin: 0 auto;">
            <h2 style="color:#f0f; margin-top:0;">CONSTRUCTOR MAIA II: NUEVO NODO</h2>
            <form method="post">
                <label class="label">TECNOLOGÍA (Neutrinos / SMR / H2 / Startup)</label><input name="p_tech">
                <label class="label">PAÍS / UBICACIÓN</label><input name="p_loc">
                <label class="label">RESUMEN TÉCNICO</label><textarea name="p_desc" rows="4"></textarea>
                <button type="button" class="btn" style="width:100%; border-color:#0f0; color:#0f0; padding:15px; margin-top:10px;" onclick="alert('Nodo Integrado')">REGISTRAR NODO</button>
            </form>
        </div>
        ''' if view == 'nuevo' else ''}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
