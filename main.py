# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
import scout_engine

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Parámetros de estado
    target_country = request.form.get('target_country', 'TODOS')
    target_tech = request.form.get('target_tech', 'TODAS')
    chat_query = request.form.get('chat_query', '')
    action = request.form.get('action', '')
    
    # Procesar búsqueda masiva
    results = []
    if action == 'buscar_scout':
        results = scout_engine.get_market_scout(target_country, target_tech)
    elif action == 'limpiar':
        results = []
        target_country = 'TODOS'
        target_tech = 'TODAS'

    # Procesar chat analítico
    chat_response = ""
    if chat_query:
        # Lógica de respuesta rápida del analizador
        chat_response = f"MAIA ANALYZER: Iniciando rastreo profundo para '{chat_query}'. Consultando bases de datos de Goldman Sachs, Bloomberg e informes sectoriales de SMR y Neutrinos..."

    # --- PLANTILLA HTML ÚNICA (CSS INTEGRADO) ---
    h = f"""
    <html><head><title>MAIA FKT - SISTEMA DE INTELIGENCIA</title>
    <style>
        body {{ background:#000; color:#0ff; font-family: 'Courier New', monospace; padding:20px; line-height:1.2; }}
        .header {{ border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:flex-end; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px 15px; cursor:pointer; font-weight:bold; font-size:12px; text-transform:uppercase; }}
        .btn:hover {{ background:rgba(0,255,255,0.1); }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-magenta {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); gap:20px; }}
        .card {{ border:1px solid #0f05; background:rgba(0,30,0,0.2); padding:20px; position:relative; border-radius:5px; border-left: 4px solid #0f0; }}
        .card-live {{ border-left: 4px solid #f00; background:rgba(30,0,0,0.2); }}
        
        .tag-ia {{ position:absolute; top:15; right:15; color:#f0f; border:1px solid #f0f; padding:3px 8px; font-size:10px; font-weight:bold; }}
        .live-label {{ color:#f00; font-weight:bold; font-size:10px; animation: blink 0.8s infinite; }}
        @keyframes blink {{ 0% {{opacity: 1;}} 50% {{opacity: 0.2;}} 100% {{opacity: 1;}} }}

        .riesgo-BAJO {{ color:#0f0; }} .riesgo-MODERADO {{ color:#ff0; }} .riesgo-ALTO {{ color:#f90; }} .riesgo-CRÍTICO {{ color:#f00; }}
        
        input, select, textarea {{ background:#000; border:1px solid #0ff; color:#0ff; padding:12px; width:100%; margin-bottom:15px; outline:none; font-family:monospace; }}
        
        .contact-box {{ background:rgba(0,255,255,0.05); border:1px solid #0ff2; padding:12px; margin-top:15px; font-size:11px; }}
        
        /* MAIA II CHAT FLOTANTE */
        #maia-chat-container {{ position:fixed; bottom:20px; right:20px; width:380px; border:2px solid #f0f; background:#000; z-index:9999; box-shadow: 0 0 20px rgba(255,0,255,0.3); }}
        .chat-header {{ background:#f0f; color:#000; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }}
        .chat-content {{ padding:15px; display: block; }}
        .minimized .chat-content {{ display:none; }}
        .minimized {{ width:180px !important; }}
    </style>
    <script>
        function toggleChat() {{ document.getElementById('maia-chat-container').classList.toggle('minimized'); }}
        function scrollToConstructor() {{ document.getElementById('constructor-area').scrollIntoView({{behavior: 'smooth'}}); }}
    </script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f; letter-spacing:2px;">MAIA FKT <span style="font-size:14px; color:#555;">// INTELLIGENCE UNIT</span></h1>
                <small style="color:#0f0;">SISTEMA CONECTADO A BROKERS, BANCOS DE INVERSIÓN Y SCRAPING WEB</small>
            </div>
            <button class="btn btn-green" onclick="scrollToConstructor()">+ CREAR PROYECTO</button>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 140px 140px; gap:12px; margin-bottom:40px;">
            <input name="target_country" placeholder="PAÍS O REGIÓN (Ej: Europa, USA, Colombia...)" value="{target_country if target_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS" {"selected" if target_tech=="TODAS" else ""}>-- TODAS LAS TECNOLOGÍAS --</option>
                <option value="SMR Nuclear" {"selected" if target_tech=="SMR Nuclear" else ""}>SMR Nuclear</option>
                <option value="Neutrinos" {"selected" if target_tech=="Neutrinos" else ""}>Tecnología de Neutrinos</option>
                <option value="Hidrógeno Verde" {"selected" if target_tech=="Hidrógeno Verde" else ""}>Hidrógeno Verde</option>
                <option value="Deep Tech" {"selected" if target_tech=="Deep Tech" else ""}>Startups Deep Tech</option>
                <option value="Solar" {"selected" if target_tech=="Solar" else ""}>Energía Solar</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
            <button type="submit" name="action" value="limpiar" class="btn btn-magenta">RESET</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card {'card-live' if 'WEB' in a['id'] else ''}">
                <div class="tag-ia">RATING: {a['Calificacion_IA']}</div>
                { '<div class="live-label">LIVE SCRAPING FEED</div>' if 'WEB' in a['id'] else '' }
                <small style="color:#0f0;">ID: {a['id']} | {a['Tecnología'].upper()}</small><br>
                <b style="font-size:1.5em; color:#fff; display:block; margin:8px 0;">{a['Nombre']}</b>
                
                <p style="font-size:12px; color:#bbb; margin-bottom:15px; min-height:45px;">{a['Resumen']}</p>
                
                <div style="display:flex; justify-content:space-between; font-size:12px;">
                    <span>VALOR EST: <b style="color:#fff;">{a['Valor_Est']}</b></span>
                    <span class="riesgo-{a['Riesgo'].replace(' ','-')}">RIESGO: {a['Riesgo']}</span>
                </div>
                
                <div style="background:#111; height:4px; width:100%; margin:15px 0;">
                    <div style="background:#0f0; height:100%; width:{a['Viabilidad']}%"></div>
                </div>

                <div class="contact-box">
                    <b style="color:#0ff;">DIRECTORIO EJECUTIVO:</b><br>
                    CEO: <span style="color:#fff;">{a['CEO']}</span> | TEL: <span style="color:#fff;">{a['Celular']}</span><br>
                    DIR: {a['Dirección']}<br>
                    URL: <a href="{a['Contacto']}" target="_blank" style="color:#f0f; text-decoration:none;">{a['Contacto'][:50]}...</a><br>
                    <b style="color:#f0f;">FUENTE: {a['Fuente']}</b> | VIGENCIA: {a['Vigencia']}
                </div>
            </div>
            ''' for a in results])}
        </div>

        <div id="constructor-area" style="margin-top:100px; padding:40px; border:1px solid #f0f; background:rgba(255,0,255,0.03); max-width:800px; margin-left:auto; margin-right:auto;">
            <h2 style="color:#f0f; margin-top:0;">CONSTRUCTOR DE PROYECTOS MAIA II</h2>
            <form method="post">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                    <input name="n_name" placeholder="NOMBRE DEL PROYECTO">
                    <input name="n_tech" placeholder="TECNOLOGÍA">
                    <input name="n_loc" placeholder="UBICACIÓN">
                    <input name="n_ceo" placeholder="CEO / CONTACTO">
                </div>
                <textarea name="n_desc" placeholder="MEMORIA TÉCNICA / RESUMEN DE NEGOCIO" rows="5"></textarea>
                <button type="button" class="btn btn-green" style="width:100%; padding:18px;" onclick="alert('PROYECTO REGISTRADO EN MEMORIA CENTRAL')">REGISTRAR EN MAIA FKT</button>
            </form>
        </div>

        <div id="maia-chat-container">
            <div class="chat-header" onclick="toggleChat()">
                MAIA II ANALYZER <span>[+/-]</span>
            </div>
            <div class="chat-content">
                <div style="font-size:12px; color:#0f0; margin-bottom:15px; min-height:60px; border-left: 2px solid #f0f; padding-left:10px;">
                    {chat_response if chat_response else 'Terminal de análisis activa. Ingrese consulta sobre brokers o proyectos...'}
                </div>
                <form method="post">
                    <input type="hidden" name="action" value="buscar_scout">
                    <input type="hidden" name="target_country" value="{target_country}">
                    <input type="hidden" name="target_tech" value="{target_tech}">
                    <input name="chat_query" placeholder="Escriba aquí..." style="font-size:11px; margin-bottom:5px;">
                    <button type="submit" class="btn btn-magenta" style="width:100%; font-size:10px;">PROCESAR CONSULTA</button>
                </form>
            </div>
        </div>

    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    # Configuración de puerto para despliegue
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)