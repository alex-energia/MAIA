# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import get_market_scout

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    action = request.form.get('action', '')
    target_country = request.form.get('target_country', 'TODOS')
    target_tech = request.form.get('target_tech', 'TODAS')
    chat_query = request.form.get('chat_query', '')
    
    all_data = get_market_scout()
    locations = sorted(list(set([a['Ubicación'] for a in all_data])))
    techs = sorted(list(set([a['Tecnología'] for a in all_data])))
    
    results = []
    chat_response = ""
    
    # Lógica de búsqueda
    if action == 'buscar_scout':
        results = all_data
        if target_country != 'TODOS':
            results = [a for a in results if a['Ubicación'] == target_country]
        if target_tech != 'TODAS':
            results = [a for a in results if a['Tecnología'] == target_tech]
    elif action == 'limpiar':
        results = []

    # Chat Analítico
    if chat_query:
        q = chat_query.lower()
        matches = [a['Nombre'] for a in all_data if q in a['Resumen'].lower() or q in a['Tecnología'].lower() or q in a['Ubicación'].lower()]
        chat_response = f"MAIA ANALYZER: Coincidencias en {', '.join(matches)}" if matches else "MAIA: No se hallaron datos relevantes en la base actual."

    h = f"""
    <html><head><title>MAIA FKT - CONSOLE v3.0</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:8px 15px; cursor:pointer; font-weight:bold; font-size:10px; text-transform:uppercase; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-magenta {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap:20px; }}
        .card {{ border:1px solid #0f03; background:rgba(0,40,0,0.1); padding:20px; border-radius:5px; position:relative; }}
        .tag-ia {{ position:absolute; top:15; right:15; color:#f0f; border:1px solid #f0f; padding:3px 8px; font-size:10px; font-weight:bold; }}
        
        .riesgo-BAJO {{ color:#0f0; }} .riesgo-MODERADO {{ color:#ff0; }} .riesgo-ALTO {{ color:#f90; }} .riesgo-CRÍTICO {{ color:#f00; font-weight:bold; }} .riesgo-MUY-ALTO {{ color:#f0f; }}
        
        input, select, textarea {{ background:#000; border:1px solid #0ff; color:#0ff; padding:12px; width:100%; margin-bottom:15px; outline:none; font-size:12px; }}
        
        .contact-box {{ background:rgba(0,255,255,0.05); border:1px solid #0ff3; padding:12px; margin-top:15px; font-size:11px; border-radius:3px; }}
        
        /* MAIA II CHAT FLOTANTE */
        #maia-chat {{ position:fixed; bottom:25px; right:25px; width:350px; border:2px solid #f0f; background:#000; z-index:9999; box-shadow: 0 0 15px #f0f5; }}
        .chat-bar {{ background:#f0f; color:#000; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }}
        .chat-content {{ padding:15px; }}
        .minimized {{ width:180px !important; }}
        .minimized .chat-content {{ display:none; }}
    </style>
    <script>
        function toggleChat() {{ document.getElementById('maia-chat').classList.toggle('minimized'); }}
        function scConstructor() {{ document.getElementById('constructor-section').scrollIntoView({{behavior: 'smooth'}}); }}
    </script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f; letter-spacing:2px;">MAIA FKT <span style="font-size:12px; color:#555;">// DEEP TECH OS</span></h1>
                <small style="color:#0f0;">SISTEMA DE MONITOREO DE ACTIVOS CRÍTICOS</small>
            </div>
            <button class="btn btn-green" onclick="scConstructor()">+ CREAR NUEVO PROYECTO</button>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 120px 120px; gap:12px; margin-bottom:40px;">
            <select name="target_country">
                <option value="TODOS">-- TODOS LOS PAÍSES --</option>
                {" ".join([f'<option value="{c}" {"selected" if c==target_country else ""}>{c.upper()}</option>' for c in locations])}
            </select>
            <select name="target_tech">
                <option value="TODAS">-- TODAS LAS TECNOLOGÍAS --</option>
                {" ".join([f'<option value="{t}" {"selected" if t==target_tech else ""}>{t.upper()}</option>' for t in techs])}
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
            <button type="submit" name="action" value="limpiar" class="btn btn-magenta">RESET</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card">
                <div class="tag-ia">IA RATING: {a['Calificacion_IA']}</div>
                <small style="color:#0f0;">ID: {a['id']} | {a['Tecnología'].upper()}</small><br>
                <b style="font-size:1.4em; color:#fff; display:block; margin:5px 0;">{a['Nombre']}</b>
                
                <p style="font-size:12px; color:#bbb; line-height:1.4; margin-bottom:15px;">{a['Resumen']}</p>
                
                <div style="display:flex; justify-content:space-between; font-size:12px;">
                    <span>VALOR EST: <b style="color:#fff;">{a['Valor_Est']}</b></span>
                    <span class="riesgo-{a['Riesgo'].replace(' ','-')}">RIESGO: {a['Riesgo']}</span>
                </div>
                
                <div style="background:#111; height:4px; width:100%; margin:15px 0; border-radius:2px;">
                    <div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div>
                </div>

                <div class="contact-box">
                    <b style="color:#0ff;">DIRECTORIO EJECUTIVO:</b><br>
                    CEO: <span style="color:#fff;">{a['CEO']}</span> | TEL: <span style="color:#fff;">{a['Celular']}</span><br>
                    DIR: {a['Dirección']}<br>
                    MAIL: {a['Contacto']}<br>
                    <b style="color:#f0f;">FUENTE: {a['Fuente']}</b> | VIGENCIA: {a['Vigencia']}
                </div>
            </div>
            ''' for a in results])}
        </div>

        <div id="constructor-section" style="margin-top:80px; padding:40px; border:1px solid #f0f; background:rgba(255,0,255,0.03); max-width:700px; margin-left:auto; margin-right:auto;">
            <h2 style="color:#f0f; margin-top:0;">CONSTRUCTOR DE PROYECTOS MAIA II</h2>
            <p style="color:#666; font-size:11px; margin-bottom:20px;">Sincronización de nuevo nodo en el repositorio de ingeniería de alto nivel.</p>
            <form method="post">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                    <input name="n_name" placeholder="NOMBRE DEL PROYECTO">
                    <input name="n_tech" placeholder="TECNOLOGÍA (SMR / H2 / NEUTRINOS)">
                    <input name="n_loc" placeholder="UBICACIÓN / PAÍS">
                    <input name="n_ceo" placeholder="CEO / RESPONSABLE">
                </div>
                <textarea name="n_desc" placeholder="DESCRIPCIÓN TÉCNICA Y VIABILIDAD" rows="5"></textarea>
                <button type="button" class="btn btn-green" style="width:100%; padding:18px; font-size:12px;" onclick="alert('NODO REGISTRADO EXITOSAMENTE EN MAIA II')">REGISTRAR EN MEMORIA CENTRAL</button>
            </form>
        </div>

        <div id="maia-chat">
            <div class="chat-bar" onclick="toggleChat()">
                MAIA II ANALYZER <span>[+]</span>
            </div>
            <div class="chat-content">
                <div style="font-size:12px; color:#0f0; margin-bottom:15px; border-left:2px solid #f0f; padding-left:10px;">
                    {chat_response if chat_response else 'Agente a la espera de consulta técnica...'}
                </div>
                <form method="post">
                    <input type="hidden" name="action" value="buscar_scout">
                    <input type="hidden" name="target_country" value="{target_country}">
                    <input type="hidden" name="target_tech" value="{target_tech}">
                    <input name="chat_query" placeholder="Consulte sobre SMR, H2 o Neutrinos..." style="font-size:11px;">
                    <button type="submit" class="btn btn-magenta" style="width:100%;">ENVIAR CONSULTA</button>
                </form>
            </div>
        </div>

    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)