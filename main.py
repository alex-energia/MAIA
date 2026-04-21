# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # --- GESTIÓN DE ESTADOS ---
    view = request.form.get('view', 'scout') # Vista por defecto
    target_country = request.form.get('target_country', 'TODOS')
    action = request.form.get('action', '') # Para detectar clics específicos
    
    all_data = get_market_scout()
    locations = sorted(list(set([a['Ubicación'] for a in all_data])))
    
    # --- LÓGICA DE FILTRADO (AGENTE SCOUT) ---
    results = []
    if action == 'buscar_scout':
        results = all_data if target_country == 'TODOS' else [a for a in all_data if a['Ubicación'] == target_country]
    elif action == 'limpiar':
        results = []

    h = f"""
    <html><head><title>MAIA FKT - MULTI-AGENTE</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .nav {{ display:flex; gap:15px; border-bottom:1px solid #333; padding-bottom:10px; margin-bottom:20px; }}
        .header {{ display:flex; justify-content:space-between; margin-bottom:20px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:8px 15px; cursor:pointer; font-weight:bold; font-size:11px; text-transform:uppercase; }}
        .btn-active {{ background:#0ff; color:#000; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap:15px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,30,0,0.2); padding:15px; border-radius:5px; position:relative; }}
        .tag-ia {{ position:absolute; top:10; right:10; color:#f0f; border:1px solid #f0f; padding:2px 5px; font-size:10px; }}
        
        .form-nuevo {{ border:1px solid #f0f; padding:20px; background:rgba(255,0,255,0.05); max-width:600px; margin:auto; }}
        input, select, textarea {{ background:#000; border:1px solid #0ff; color:#0ff; padding:10px; width:100%; margin-bottom:10px; outline:none; }}
        .chat-area {{ border:1px solid #f0f; padding:15px; margin-top:20px; background:rgba(0,0,0,0.5); font-size:12px; }}
    </style>
    </head><body>
        <div class="header">
            <h1 style="margin:0; color:#f0f;">MAIA FKT <span style="font-size:12px; color:#666;">MULTI-AGENT OS</span></h1>
            <div style="font-size:10px; color:#0f0;">SISTEMA ACTIVO // ENCRIPCIÓN AES-256</div>
        </div>

        <div class="nav">
            <form method="post" style="margin:0;">
                <input type="hidden" name="view" value="scout">
                <button type="submit" class="btn {'btn-active' if view=='scout' else ''}">🔍 BUSCADOR DE NEGOCIOS</button>
            </form>
            <form method="post" style="margin:0;">
                <input type="hidden" name="view" value="nuevo">
                <button type="submit" class="btn {'btn-active' if view=='nuevo' else ''}">🏗️ CREAR NUEVO PROYECTO</button>
            </form>
        </div>

        {''' ''' if view == 'scout' else ''}
        {f'''
        <div style="margin-bottom:20px; display:flex; gap:10px;">
            <form method="post" style="display:flex; gap:10px; margin:0;">
                <input type="hidden" name="view" value="scout">
                <select name="target_country" style="width:200px; margin:0;">
                    <option value="TODOS">-- TODOS LOS PAÍSES --</option>
                    {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in locations])}
                </select>
                <button type="submit" name="action" value="buscar_scout" class="btn btn-scout">EJECUTAR SCOUT</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:#f0f; color:#f0f;">LIMPIAR</button>
            </form>
        </div>

        <div class="grid">
            {"".join([f'''
            <div class="card">
                <div class="tag-ia">CALIF. IA: {a['Calificacion_IA']}</div>
                <small style="color:#0f0;">ID: {a['id']} | RIESGO: {a['Riesgo']}</small><br>
                <b style="font-size:1.2em; color:#fff;">{a['Nombre']}</b><br>
                <p style="font-size:11px; color:#ccc;"><b>RESUMEN:</b> {a['Resumen']}</p>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin:10px 0;">
                    <span>VALOR: <b>{a['Valor_Est']}</b></span>
                    <span style="color:#f0f;">{a['Potencia']}</span>
                </div>
                <div style="font-size:10px; color:#666; border-top:1px solid #333; padding-top:10px;">
                    <b>FUENTE:</b> {a['Fuente']} | <b>VIGENCIA:</b> {a['Vigencia']}<br>
                    <b>CONTACTO:</b> {a['Contacto']}
                </div>
                <button class="btn" style="font-size:8px; margin-top:10px; border-color:#444;" onclick="alert('Guardado en memoria')">MEMORIA [+]</button>
            </div>
            ''' for a in results])}
        </div>

        <div class="chat-area">
            <b style="color:#f0f;">[MAIA CHAT ESPECIALIZADO]</b><br>
            <small style="color:#666;">Analizando fichas activas...</small>
            <form method="post" style="margin-top:10px;">
                <input type="hidden" name="view" value="scout">
                <input name="chat_query" class="chat-input" style="width:80%;" placeholder="Pregunta sobre la viabilidad de los proyectos encontrados...">
                <button type="submit" class="btn">CONSULTAR</button>
            </form>
        </div>
        ''' if view == 'scout' else ''}

        {''' ''' if view == 'nuevo' else ''}
        {f'''
        <div class="form-nuevo">
            <h2 style="color:#f0f; margin-top:0;">REGISTRO DE NUEVA INGENIERÍA</h2>
            <p style="font-size:11px; color:#666;">Ingrese los datos para el Agente Constructor MAIA II.</p>
            <form action="/" method="post">
                <label class="label">Nombre del Proyecto</label>
                <input name="p_nombre" placeholder="Ej: Central Fotovoltaica Alpha">
                
                <label class="label">País / Ubicación</label>
                <input name="p_pais" placeholder="Ej: Colombia">
                
                <label class="label">Capacidad Estimada (MW)</label>
                <input name="p_potencia" placeholder="Ej: 50 MW">
                
                <label class="label">Descripción Técnica</label>
                <textarea name="p_desc" rows="3" placeholder="Detalle la tecnología y el objetivo del proyecto..."></textarea>
                
                <button type="button" class="btn" style="width:100%; border-color:#0f0; color:#0f0; padding:15px;" onclick="alert('PROYECTO ENVIADO A VALIDACIÓN DE AGENTE DE INGENIERÍA')">REGISTRAR PROYECTO EN MAIA II</button>
            </form>
        </div>
        ''' if view == 'nuevo' else ''}

    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
