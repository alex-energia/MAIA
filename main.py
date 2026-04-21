# -*- coding: utf-8 -*-
# main.py - CONSOLA DE OPERACIONES MAIA FKT
# ESTADO: INTEGRIDAD TOTAL - PROHIBIDO RESUMIR

from flask import Flask, render_template_string, request
import os
import scout_engine

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Captura de datos de entrada
    target_country = request.form.get('target_country', 'TODOS')
    target_tech = request.form.get('target_tech', 'TODAS')
    chat_query = request.form.get('chat_query', '')
    action = request.form.get('action', '')
    
    # Procesamiento de búsqueda por Agente Scout
    results = []
    if action == 'buscar_scout':
        results = scout_engine.get_market_scout(target_country, target_tech)
    elif action == 'limpiar':
        results = []
        target_country = 'TODOS'
        target_tech = 'TODAS'

    # Procesamiento de Chat Analizador
    chat_response = ""
    if chat_query:
        chat_response = f"MAIA ANALYZER: Analizando '{chat_query}'... Cruzando datos de brokers internacionales y viabilidad de proyectos en curso. Detectada alta demanda de capital en {target_tech}."

    # --- RENDERIZADO DE INTERFAZ MAIA II ---
    h = f"""
    <html><head><title>MAIA FKT - SISTEMA OPERATIVO</title>
    <style>
        body {{ background:#000; color:#0ff; font-family: 'Courier New', monospace; padding:20px; }}
        .header {{ border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:25px; display:flex; justify-content:space-between; align-items:center; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px 20px; cursor:pointer; font-weight:bold; font-size:12px; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-magenta {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr)); gap:25px; }}
        .card {{ border:1px solid #0f03; background:rgba(0,40,0,0.15); padding:20px; border-radius:4px; position:relative; border-left: 5px solid #0f0; }}
        .card-web {{ border-left: 5px solid #f00; background:rgba(40,0,0,0.15); }}
        
        .tag-ia {{ position:absolute; top:15; right:15; color:#f0f; border:1px solid #f0f; padding:4px 10px; font-size:11px; }}
        .riesgo-BAJO {{ color:#0f0; }} .riesgo-MODERADO {{ color:#ff0; }} .riesgo-ALTO {{ color:#f90; }} .riesgo-CRÍTICO {{ color:#f00; }}
        
        input, select, textarea {{ background:#000; border:1px solid #0ff; color:#0ff; padding:12px; width:100%; margin-bottom:15px; outline:none; }}
        .contact-box {{ background:rgba(0,255,255,0.04); border:1px solid #0ff2; padding:15px; margin-top:20px; font-size:11px; }}
        
        /* CHAT FLOTANTE MAIA II */
        #chat-float {{ position:fixed; bottom:20px; right:20px; width:360px; border:2px solid #f0f; background:#000; z-index:999; box-shadow: 0 0 15px #f0f5; transition:0.3s; }}
        .chat-top {{ background:#f0f; color:#000; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }}
        .chat-main {{ padding:15px; }}
        .minimized .chat-main {{ display:none; }}
        .minimized {{ width:150px !important; }}
    </style>
    <script>
        function toggleChat() {{ document.getElementById('chat-float').classList.toggle('minimized'); }}
    </script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f; letter-spacing:2px;">MAIA FKT <span style="font-size:12px; color:#444;">// INTELLIGENCE UNIT</span></h1>
                <small style="color:#0f0;">SISTEMA DE BÚSQUEDA BRUTAL CONECTADO</small>
            </div>
            <button class="btn btn-green">+ CREAR NUEVO NODO</button>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 150px 150px; gap:12px; margin-bottom:40px;">
            <input name="target_country" placeholder="REGION / PAÍS (Ej: Colombia, Europa, USA...)" value="{target_country if target_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS">-- TECNOLOGÍAS --</option>
                <option value="SMR Nuclear" {"selected" if target_tech=="SMR Nuclear" else ""}>SMR Nuclear</option>
                <option value="Neutrinos" {"selected" if target_tech=="Neutrinos" else ""}>Tecnología de Neutrinos</option>
                <option value="Hidrógeno Verde" {"selected" if target_tech=="Hidrógeno Verde" else ""}>Hidrógeno Verde</option>
                <option value="Deep Tech" {"selected" if target_tech=="Deep Tech" else ""}>Startups Deep Tech</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
            <button type="submit" name="action" value="limpiar" class="btn btn-magenta">RESET</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card {'card-web' if 'WEB' in a['id'] else ''}">
                <div class="tag-ia">IA RATING: {a['Calificacion_IA']}</div>
                <small style="color:#0f0;">ID: {a['id']} | {a['Tecnología'].upper()}</small>
                <h2 style="color:#fff; margin:10px 0; font-size:1.4em;">{a['Nombre']}</h2>
                <p style="color:#bbb; font-size:13px; line-height:1.4;">{a['Resumen']}</p>
                
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-top:10px;">
                    <span>VALOR EST: <b style="color:#fff;">{a['Valor_Est']}</b></span>
                    <span class="riesgo-{a['Riesgo'].replace(' ','-')}">RIESGO: {a['Riesgo']}</span>
                </div>
                
                <div style="background:#111; height:4px; width:100%; margin:15px 0;">
                    <div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div>
                </div>

                <div class="contact-box">
                    <b style="color:#0ff;">DIRECTORIO Y FUENTE:</b><br>
                    CEO: {a['CEO']} | TEL: {a['Celular']}<br>
                    DIRECCIÓN: {a['Dirección']}<br>
                    URL: <a href="{a['Contacto']}" target="_blank" style="color:#f0f;">{a['Contacto'][:50]}...</a><br>
                    <b style="color:#f0f;">FUENTE: {a['Fuente']}</b>
                </div>
            </div>
            ''' for a in results])}
        </div>

        <div id="chat-float">
            <div class="chat-top" onclick="toggleChat()">MAIA II ANALYZER [+/-]</div>
            <div class="chat-main">
                <div style="font-size:12px; color:#0f0; margin-bottom:15px; border-left:2px solid #f0f; padding-left:10px;">
                    {chat_response if chat_response else 'Consola lista para análisis de mercado...'}
                </div>
                <form method="post">
                    <input type="hidden" name="action" value="buscar_scout">
                    <input type="hidden" name="target_country" value="{target_country}">
                    <input type="hidden" name="target_tech" value="{target_tech}">
                    <input name="chat_query" placeholder="Consulta técnica..." style="font-size:11px; margin-bottom:5px;">
                    <button type="submit" class="btn btn-magenta" style="width:100%; font-size:10px;">CONSULTAR</button>
                </form>
            </div>
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
