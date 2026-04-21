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
    chat_query = request.form.get('chat_query', '')
    
    all_data = get_market_scout()
    # Extraer ubicaciones para el buscador dinámico
    locations = sorted(list(set([a['Ubicación'] for a in all_data])))
    
    results = []
    chat_response = ""
    
    if view == 'scout':
        if action == 'buscar_scout':
            results = all_data if target_country == 'TODOS' else [a for a in all_data if a['Ubicación'] == target_country]
        elif action == 'limpiar':
            results = []
            target_country = 'TODOS'
            
        if chat_query:
            q = chat_query.lower()
            matches = [a['Nombre'] for a in all_data if q in a['Resumen'].lower() or q in a['Ubicación'].lower() or q in a['Nombre'].lower()]
            chat_response = f"MAIA ANALYZER: Coincidencias en: {', '.join(matches)}" if matches else "MAIA: Sin coincidencias."

    h = f"""
    <html><head><title>MAIA FKT - INTEL SYSTEM</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:1px solid #f0f; padding-bottom:10px; margin-bottom:20px; }}
        .nav {{ display:flex; gap:10px; margin-bottom:20px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:8px 15px; cursor:pointer; font-weight:bold; font-size:10px; text-transform:uppercase; }}
        .btn-active {{ background:#0ff; color:#000; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; background:rgba(0,255,0,0.05); }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap:15px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,30,0,0.15); padding:15px; border-radius:5px; position:relative; }}
        .tag-ia {{ position:absolute; top:10; right:10; color:#f0f; border:1px solid #f0f; padding:2px 6px; font-size:9px; font-weight:bold; }}
        
        input, select, textarea {{ background:#000; border:1px solid #0ff; color:#0ff; padding:10px; width:100%; margin-bottom:10px; outline:none; }}
        .contact-details {{ background:rgba(0,255,255,0.05); border-top:1px solid #0ff3; padding:10px; margin-top:10px; font-size:10px; }}
        .chat-box {{ border:1px solid #f0f; background:rgba(255,0,255,0.05); padding:15px; margin-top:25px; }}
    </style>
    </head><body>
        <div class="header">
            <h1 style="margin:0; color:#f0f; letter-spacing:1px;">MAIA FKT <span style="font-size:12px; color:#666;">// OS v2.5</span></h1>
            <div style="font-size:10px; color:#0f0; text-align:right;">CENTRAL DE MANDO ACTIVA</div>
        </div>

        <div class="nav">
            <form method="post" style="margin:0;">
                <input type="hidden" name="view" value="scout">
                <button type="submit" class="btn {'btn-active' if view=='scout' else ''}">🔍 AGENTE SCOUT</button>
            </form>
            <form method="post" style="margin:0;">
                <input type="hidden" name="view" value="nuevo">
                <button type="submit" class="btn {'btn-active' if view=='nuevo' else ''}">🏗️ NUEVO PROYECTO</button>
            </form>
        </div>

        {''' ''' if view == 'scout' else ''}
        {f'''
        <form method="post" style="display:flex; gap:10px; margin-bottom:20px;">
            <input type="hidden" name="view" value="scout">
            <select name="target_country" style="width:300px; margin:0;">
                <option value="TODOS">-- TODOS LOS PAÍSES (REINICIAR) --</option>
                {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in locations])}
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-scout">BUSCAR</button>
            <button type="submit" name="action" value="limpiar" class="btn" style="border-color:#f0f; color:#f0f;">LIMPIAR</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card">
                <div class="tag-ia">CALIF. IA: {a['Calificacion_IA']}</div>
                <small style="color:#0f0;">ID: {a['id']} | RIESGO: {a['Riesgo']}</small><br>
                <b style="font-size:1.3em; color:#fff;">{a['Nombre']}</b><br>
                
                <p style="margin:10px 0; font-size:11px; color:#ccc;"><b>RESUMEN:</b> {a['Resumen']}</p>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px;">
                    <span>VALOR: <b>{a['Valor_Est']}</b></span>
                    <span style="color:#f0f;">POTENCIA: {a['Potencia']}</span>
                </div>
                
                <div style="background:#111; height:3px; width:100%; margin-bottom:10px;">
                    <div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div>
                </div>

                <div class="contact-details">
                    <b style="color:#0ff;">DIRECTORIO CORPORATIVO:</b><br>
                    CEO: {a['CEO']}<br>
                    TEL: {a['Celular']}<br>
                    DIR: {a['Dirección']}<br>
                    MAIL: {a['Contacto']}<br>
                    <b style="color:#f0f;">FUENTE:</b> {a['Fuente']} | <b>VIGENCIA:</b> {a['Vigencia']}
                </div>
                <button class="btn" style="font-size:8px; margin-top:10px; border-color:#444;" onclick="alert('Sincronizado')">MEMORIA [+]</button>
            </div>
            ''' for a in results])}
        </div>

        <div class="chat-box">
            <b style="color:#f0f;">[MAIA CHAT ANALYZER]</b>
            {f'<div style="color:#0f0; margin-bottom:10px; font-size:12px; border-left:2px solid #0f0; padding-left:10px;">> {chat_response}</div>' if chat_response else ''}
            <form method="post">
                <input type="hidden" name="view" value="scout">
                <input type="hidden" name="action" value="buscar_scout">
                <input type="hidden" name="target_country" value="{target_country}">
                <input name="chat_query" style="width:75%;" placeholder="Consulte viabilidad o detalles de riesgo...">
                <button type="submit" class="btn">CONSULTAR</button>
            </form>
        </div>
        ''' if view == 'scout' else ''}

        {f'''
        <div style="max-width:600px; border:1px solid #f0f; padding:25px; background:rgba(255,0,255,0.05); margin: 0 auto;">
            <h2 style="color:#f0f; margin-top:0;">AGENTE CONSTRUCTOR: REGISTRO MAIA II</h2>
            <form method="post">
                <label style="color:#666; font-size:10px;">NOMBRE PROYECTO</label><input name="p_name">
                <label style="color:#666; font-size:10px;">PAÍS</label><input name="p_loc">
                <label style="color:#666; font-size:10px;">POTENCIA (MW)</label><input name="p_pot">
                <label style="color:#666; font-size:10px;">CEO / RESPONSABLE</label><input name="p_ceo">
                <label style="color:#666; font-size:10px;">DESCRIPCIÓN</label><textarea name="p_desc" rows="4"></textarea>
                <button type="button" class="btn" style="width:100%; border-color:#0f0; color:#0f0; padding:15px; margin-top:10px;" onclick="alert('PROYECTO ENVIADO')">REGISTRAR EN MAIA II</button>
            </form>
        </div>
        ''' if view == 'nuevo' else ''}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)