# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import scout_engine

app = Flask(__name__)
MAIA_MEMORIA = []

@app.route('/', methods=['GET', 'POST'])
def home():
    t_country = request.form.get('target_country', 'TODOS')
    t_tech = request.form.get('target_tech', 'TODAS')
    action = request.form.get('action', '')
    c_query = request.form.get('chat_query', '')
    
    results = []
    if action == 'buscar_scout':
        results = scout_engine.execute_brutal_search(t_country, t_tech)
    
    if action == 'guardar_memoria':
        ficha = request.form.to_dict()
        if ficha not in MAIA_MEMORIA: MAIA_MEMORIA.append(ficha)

    chat_resp = f"MAIA: {len(results)} nodos detectados. Potencia nominal identificada en {t_tech}." if c_query else ""

    h = f"""
    <html><head><title>MAIA FKT - COMMAND CENTER</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:30px; }}
        .header {{ border-bottom:3px solid #f0f; padding-bottom:15px; margin-bottom:30px; display:flex; justify-content:space-between; }}
        .btn {{ background:none; border:2px solid #0ff; color:#0ff; padding:10px; cursor:pointer; font-weight:bold; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-magenta {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr)); gap:25px; }}
        .card {{ border:1px solid #0f02; background:rgba(0,30,0,0.1); padding:25px; position:relative; border-left: 6px solid #0f0; }}
        .card-live {{ border-left: 6px solid #f00; background:rgba(40,0,0,0.1); }}
        
        .pwr-tag {{ background:#0f0; color:#000; padding:2px 8px; font-weight:bold; font-size:12px; margin-right:10px; }}
        .contact-box {{ background:rgba(0,255,255,0.05); padding:15px; margin-top:20px; border:1px solid #0ff3; font-size:11px; }}
        input, select {{ background:#000; border:1px solid #0ff; color:#0ff; padding:12px; margin-bottom:10px; width:100%; font-family:monospace; }}
        
        /* CHAT MAIA II DINÁMICO */
        #maia-chat {{ position:fixed; bottom:20px; right:20px; width:350px; border:2px solid #f0f; background:#000; z-index:9999; transition: height 0.3s; }}
        .chat-h {{ background:#f0f; color:#000; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }}
        .chat-b {{ padding:15px; display: block; }}
        .minimized {{ height: 45px !important; overflow: hidden; }}
        .minimized .chat-b {{ display: none; }}
    </style>
    <script>
        function toggleChat() {{ document.getElementById('maia-chat').classList.toggle('minimized'); }}
    </script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f;">MAIA FKT <span style="font-size:12px; color:#555;">// V.4 OPERATIONAL</span></h1>
                <b style="color:#0f0;">SISTEMA BLINDADO: 100% REAL - GEO-LOCALIZADO</b>
            </div>
            <a href="/memoria" class="btn btn-magenta">MEMORIA ({len(MAIA_MEMORIA)})</a>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 150px; gap:10px; margin-bottom:40px;">
            <input name="target_country" placeholder="UBICACIÓN (Ej: Colombia, USA, Europa...)" value="{t_country if t_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS">-- TECNOLOGÍAS --</option>
                <option value="SMR Nuclear" {"selected" if t_tech=="SMR Nuclear" else ""}>SMR Nuclear</option>
                <option value="Hidrógeno Verde" {"selected" if t_tech=="Hidrógeno Verde" else ""}>Hidrógeno Verde</option>
                <option value="Neutrinos" {"selected" if t_tech=="Neutrinos" else ""}>Neutrinos</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card {'card-live' if 'LIVE' in a['id'] else ''}">
                <div style="position:absolute; top:10; right:10; font-size:10px;">{a['Fecha_Pub']}</div>
                <small style="color:#0f0;">{a['id']} | {a['Tecnología'].upper()}</small>
                <h2 style="color:#fff; margin:10px 0;">{a['Nombre']}</h2>
                <div style="margin-bottom:10px;">
                    <span class="pwr-tag">POTENCIA: {a['Potencia']}</span>
                </div>
                <p style="color:#bbb; font-size:12px;">{a['Resumen']}</p>
                <div style="display:flex; justify-content:space-between; font-size:12px;">
                    <span>VALOR: <b>{a['Valor_Est']}</b></span>
                    <span>RIESGO: <b style="color:#f0f;">{a['Riesgo']}</b></span>
                </div>
                <div class="contact-box">
                    CEO: {a['CEO']} | TEL: {a['Celular']}<br>
                    DIR: {a['Dirección']}<br>
                    FUENTE: <a href="{a['Contacto']}" target="_blank" style="color:#f0f;">{a['Fuente']}</a>
                </div>
                <form method="post" style="margin-top:15px;">
                    <input type="hidden" name="Nombre" value="{a['Nombre']}">
                    <input type="hidden" name="Potencia" value="{a['Potencia']}">
                    <input type="hidden" name="Valor" value="{a['Valor_Est']}">
                    <input type="hidden" name="Fuente" value="{a['Fuente']}">
                    <button type="submit" name="action" value="guardar_memoria" class="btn btn-magenta" style="width:100%;">+ SINCRONIZAR MEMORIA</button>
                </form>
            </div>
            ''' for a in results])}
        </div>

        <div id="maia-chat">
            <div class="chat-h" onclick="toggleChat()">MAIA II ANALYZER <span>[+/-]</span></div>
            <div class="chat-b">
                <div style="font-size:11px; color:#0f0; margin-bottom:10px; border-left:2px solid #f0f; padding-left:10px;">
                    {chat_resp if chat_resp else 'Consola lista. Minimice o Maximice según necesidad.'}
                </div>
                <form method="post">
                    <input name="chat_query" placeholder="Consulta profunda..." style="padding:8px; font-size:11px;">
                </form>
            </div>
        </div>
    </body></html>
    """
    return render_template_string(h)

@app.route('/memoria')
def memoria():
    h = f"""
    <html><body style="background:#000; color:#0ff; font-family:monospace; padding:30px;">
        <h1 style="color:#f0f;">MEMORIA DE ACTIVOS</h1>
        <a href="/" style="color:#0f0;">VOLVER</a><br><br>
        {"".join([f'<div style="border:1px solid #f0f; padding:15px; margin-bottom:10px;"><b>{m["Nombre"]}</b><br>POTENCIA: {m["Potencia"]} | VALOR: {m["Valor"]}</div>' for m in MAIA_MEMORIA])}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)