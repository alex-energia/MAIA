# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import os
from scout_engine import scout_engine

app = Flask(__name__)

# Base de datos temporal para Memoria
MAIA_MEMORIA = []

@app.route('/', methods=['GET', 'POST'])
def home():
    target_country = request.form.get('target_country', 'TODOS')
    target_tech = request.form.get('target_tech', 'TODAS')
    chat_query = request.form.get('chat_query', '')
    action = request.form.get('action', '')
    
    results = []
    if action == 'buscar_scout':
        results = scout_engine.execute_scout(target_country, target_tech)
    
    if action == 'guardar_memoria':
        # Capturamos todos los campos para la memoria
        ficha = {
            "Nombre": request.form.get('Nombre'),
            "Tecnología": request.form.get('Tecnología'),
            "Ubicación": request.form.get('Ubicación'),
            "Valor": request.form.get('Valor'),
            "CEO": request.form.get('CEO'),
            "Fuente": request.form.get('Fuente')
        }
        if ficha not in MAIA_MEMORIA:
            MAIA_MEMORIA.append(ficha)

    chat_response = ""
    if chat_query:
        chat_response = f"MAIA ANALYZER: Cruce de datos finalizado. {len(results)} nodos detectados. La memoria ahora contiene {len(MAIA_MEMORIA)} activos estratégicos."

    h = f"""
    <html><head><title>MAIA FKT - COMMAND CENTER</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; }}
        .btn {{ background:none; border:1px solid #0ff; color:#0ff; padding:10px; cursor:pointer; font-weight:bold; font-size:11px; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-mem {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr)); gap:25px; }}
        .card {{ border:1px solid #0f03; background:rgba(0,30,0,0.1); padding:20px; border-radius:5px; position:relative; border-left: 5px solid #0f0; }}
        .card-live {{ border-left: 5px solid #f00; }}
        
        .tag-date {{ position:absolute; top:10; right:10; font-size:10px; color:#555; }}
        .tag-ia {{ position:absolute; top:25; right:10; color:#f0f; font-size:10px; font-weight:bold; }}
        
        .riesgo-BAJO {{ color:#0f0; }} .riesgo-MODERADO {{ color:#ff0; }} .riesgo-ALTO {{ color:#f90; }} .riesgo-POR-VALIDAR {{ color:#f0f; }}
        
        .contact-box {{ background:rgba(0,255,255,0.05); padding:15px; margin-top:15px; border:1px solid #0ff2; font-size:11px; }}
        input, select {{ background:#000; border:1px solid #0ff; color:#0ff; padding:12px; margin-bottom:10px; width:100%; }}
        
        #maia-chat {{ position:fixed; bottom:20px; right:20px; width:350px; border:2px solid #f0f; background:#000; z-index:1000; }}
        .chat-h {{ background:#f0f; color:#000; padding:12px; font-weight:bold; cursor:pointer; }}
        .chat-b {{ padding:15px; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f; letter-spacing:2px;">MAIA FKT <span style="font-size:12px; color:#555;">// V.3.5 REAL-TIME</span></h1>
                <small style="color:#0f0;">SISTEMA DE MONITOREO DE ACTIVOS ESTRATÉGICOS</small>
            </div>
            <a href="/memoria" class="btn btn-mem">MEMORIA CENTRAL ({len(MAIA_MEMORIA)})</a>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 150px; gap:10px; margin-bottom:40px;">
            <input name="target_country" placeholder="UBICACIÓN / PAÍS" value="{target_country if target_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS">-- TECNOLOGÍAS --</option>
                <option value="SMR Nuclear">SMR Nuclear</option>
                <option value="Hidrógeno Verde">Hidrógeno Verde</option>
                <option value="Neutrinos">Neutrinos</option>
                <option value="Solar">Solar / Fotovoltaica</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card {'card-live' if 'LIVE' in a['id'] else ''}">
                <div class="tag-date">FECHA: {a['Fecha_Pub']}</div>
                <div class="tag-ia">IA: {a['Calificacion_IA']}</div>
                
                <small style="color:#0f0;">ID: {a['id']} | {a['Tecnología'].upper()}</small>
                <h2 style="color:#fff; margin:10px 0; font-size:1.4em;">{a['Nombre']}</h2>
                
                <p style="color:#bbb; font-size:12px; line-height:1.4;">{a['Resumen']}</p>
                
                <div style="display:flex; justify-content:space-between; font-size:12px;">
                    <span>VALOR: <b style="color:#fff;">{a['Valor_Est']}</b></span>
                    <span class="riesgo-{a['Riesgo'].replace(' ','-')}">RIESGO: {a['Riesgo']}</span>
                </div>

                <div class="contact-box">
                    <b style="color:#0ff;">DIRECTORIO EJECUTIVO:</b><br>
                    CEO: <span style="color:#fff;">{a['CEO']}</span> | TEL: <span style="color:#fff;">{a['Celular']}</span><br>
                    DIR: {a['Dirección']}<br>
                    <b style="color:#f0f;">FUENTE: {a['Fuente']}</b> | <a href="{a['Contacto']}" target="_blank" style="color:#0ff; text-decoration:none;">VER RECURSO ORIGINAL</a>
                </div>

                <form method="post" style="margin-top:15px;">
                    <input type="hidden" name="Nombre" value="{a['Nombre']}">
                    <input type="hidden" name="Tecnología" value="{a['Tecnología']}">
                    <input type="hidden" name="Ubicación" value="{a['Ubicación']}">
                    <input type="hidden" name="Valor" value="{a['Valor_Est']}">
                    <input type="hidden" name="CEO" value="{a['CEO']}">
                    <input type="hidden" name="Fuente" value="{a['Fuente']}">
                    <button type="submit" name="action" value="guardar_memoria" class="btn btn-mem" style="width:100%;">+ SINCRONIZAR A MEMORIA</button>
                </form>
            </div>
            ''' for a in results])}
        </div>

        <div id="maia-chat">
            <div class="chat-h" onclick="document.getElementById('cb').style.display='none'">MAIA II ANALYZER</div>
            <div id="cb" class="chat-b">
                <div style="font-size:11px; color:#0f0; margin-bottom:10px; border-left:2px solid #f0f; padding-left:10px;">
                    {chat_response if chat_response else 'Agente listo. Ejecute Scout para iniciar análisis...'}
                </div>
                <form method="post">
                    <input name="chat_query" placeholder="Consulta técnica..." style="width:100%; padding:8px; background:#000; border:1px solid #0ff; color:#0ff; font-size:11px;">
                </form>
            </div>
        </div>
    </body></html>
    """
    return render_template_string(h)

@app.route('/memoria')
def memoria():
    h = f"""
    <html><head><title>MAIA - MEMORIA</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .card {{ border:1px solid #f0f; padding:20px; margin-bottom:15px; background:rgba(255,0,255,0.05); }}
        .btn {{ border:1px solid #0ff; color:#0ff; text-decoration:none; padding:10px; display:inline-block; }}
    </style>
    </head><body>
        <h1 style="color:#f0f;">REPOSITORIO DE MEMORIA CENTRAL</h1>
        <a href="/" class="btn">VOLVER A CONSOLA</a><br><br>
        {"".join([f'''
        <div class="card">
            <b style="font-size:1.2em; color:#fff;">{m['Nombre']}</b><br>
            <small>{m['Tecnología']} | {m['Ubicación']}</small><br>
            VALOR: {m['Valor']} | CEO: {m['CEO']} | FUENTE: {m['Fuente']}
        </div>
        ''' for m in MAIA_MEMORIA])}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
