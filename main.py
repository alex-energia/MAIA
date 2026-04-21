# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Parámetros de control
    view = request.form.get('view', 'init')
    target_country = request.form.get('target_country', 'TODOS')
    chat_query = request.form.get('chat_query', '')
    
    all_data = get_market_scout()
    locations = sorted(list(set([a['Ubicación'] for a in all_data])))
    
    # Lógica de limpieza y búsqueda
    results = []
    if view == 'scout':
        results = all_data if target_country == 'TODOS' else [a for a in all_data if a['Ubicación'] == target_country]
    elif view == 'clear':
        target_country = 'TODOS'
        results = []

    # Lógica del Chat MAIA
    chat_response = ""
    if chat_query:
        # Simulación de análisis de IA sobre las fichas
        keywords = chat_query.lower()
        matched = [a['Nombre'] for a in all_data if keywords in a['Resumen'].lower() or keywords in a['Nombre'].lower()]
        if matched:
            chat_response = f"MAIA ANALYZER: He encontrado relevancia en {', '.join(matched)}. Estos proyectos cumplen con tus criterios técnicos."
        else:
            chat_response = "MAIA ANALYZER: No hay coincidencias exactas en la base actual. ¿Deseas que amplíe el rango de búsqueda?"

    h = f"""
    <html><head><title>MAIA FKT - CENTRAL DE INTELIGENCIA</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ display:flex; justify-content:space-between; border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:20px; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:8px; cursor:pointer; font-weight:bold; font-size:10px; text-transform:uppercase; }}
        .btn-scout {{ border-color:#0f0; color:#0f0; background:rgba(0,255,0,0.05); }}
        .btn-clear {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap:15px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,30,0,0.2); padding:15px; position:relative; border-radius:5px; }}
        .tag-ia {{ position:absolute; top:10; right:10; color:#f0f; border:1px solid #f0f; padding:2px 5px; font-size:10px; font-weight:bold; }}
        
        .chat-container {{ border:1px solid #f0f; background:rgba(255,0,255,0.05); padding:15px; margin-top:30px; border-radius:5px; }}
        .chat-input {{ background:#000; border:1px solid #0ff; color:#0ff; padding:10px; width:70%; outline:none; }}
        
        select {{ background:#000; border:1px solid #f0f; color:#0ff; padding:8px; outline:none; cursor:pointer; }}
        .label {{ color:#666; font-size:10px; text-transform:uppercase; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f; letter-spacing:1px;">MAIA FKT <span style="font-size:12px; color:#666;">// SCOUT & CHAT</span></h1>
            </div>
            
            <form method="post" style="display:flex; gap:10px; margin:0; align-items:center;">
                <select name="target_country">
                    <option value="TODOS">-- REINICIAR / TODOS --</option>
                    {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in locations])}
                </select>
                <button type="submit" name="view" value="scout" class="btn btn-scout">EJECUTAR SCOUT</button>
                <button type="submit" name="view" value="clear" class="btn btn-clear">LIMPIAR PANTALLA</button>
            </form>
        </div>

        <div class="grid">
        {"".join([f'''
        <div class="card">
            <div class="tag-ia">CALIF. IA: {a['Calificacion_IA']}</div>
            <small style="color:#0f0;">ID: {a['id']} | RIESGO: {a['Riesgo']}</small><br>
            <b style="font-size:1.2em; color:#fff;">{a['Nombre']}</b><br>
            
            <div style="margin:10px 0; font-size:11px; color:#ccc; min-height:40px;">
                <b style="color:#0ff;">RESUMEN:</b> {a['Resumen']}
            </div>

            <div style="display:flex; justify-content:space-between; font-size:12px;">
                <span>VALOR: <b>{a['Valor_Est']}</b></span>
                <span style="color:#f0f;">POTENCIA: {a['Potencia']}</span>
            </div>

            <div style="background:#111; height:3px; width:100%; margin:10px 0;">
                <div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div>
            </div>
            
            <div style="font-size:10px; color:#666;">
                <b>FUENTE:</b> {a['Fuente']} | <b>VIGENCIA:</b> {a['Vigencia']}<br>
                <b>CONTACTO:</b> {a['Contacto']}
            </div>
            <button class="btn" style="font-size:8px; margin-top:10px; border-color:#555;" onclick="alert('Datos sincronizados')">MEMORIA [+]</button>
        </div>
        ''' for a in results])}
        </div>

        <div class="chat-container">
            <h3 style="margin:0 0 10px 0; color:#f0f; font-size:14px;">[+] CHAT ESPECIALIZADO MAIA</h3>
            <p style="font-size:11px; color:#666;">Consulta detalles específicos sobre las fichas activas en la base de datos.</p>
            
            {f'<div style="color:#0f0; margin-bottom:10px; font-size:12px; padding:5px; border-left:2px solid #0f0;">> {chat_response}</div>' if chat_response else ''}
            
            <form method="post">
                <input type="hidden" name="view" value="{view}">
                <input type="hidden" name="target_country" value="{target_country}">
                <input name="chat_query" class="chat-input" placeholder="Pregunta sobre proyectos (ej: ¿Qué hay en España?, Licitaciones, Texas...)" value="{chat_query}">
                <button type="submit" class="btn" style="border-color:#f0f; color:#f0f;">CONSULTAR IA</button>
            </form>
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
