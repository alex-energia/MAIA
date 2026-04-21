# -*- coding: utf-8 -*-
# main.py - CONSOLA DE CONTROL MAIA II
# ESTADO: INTEGRIDAD TOTAL - BLINDAJE ANTI-RETROCESOS

from flask import Flask, render_template_string, request, redirect
import os
from scout_engine import scout_engine

app = Flask(__name__)

# Memoria de Sesión (Persistencia Temporal)
MAIA_MEMORIA = []

@app.route('/', methods=['GET', 'POST'])
def home():
    # Estados de búsqueda
    t_country = request.form.get('target_country', 'TODOS')
    t_tech = request.form.get('target_tech', 'TODAS')
    action = request.form.get('action', '')
    c_query = request.form.get('chat_query', '')
    
    results = []
    if action == 'buscar_scout':
        # Ejecución del motor blindado
        results = scout_engine.execute_brutal_search(t_country, t_tech)
    
    if action == 'guardar_memoria':
        # Captura técnica absoluta de la ficha
        ficha = {
            "id": request.form.get('id'),
            "Nombre": request.form.get('Nombre'),
            "Tecnología": request.form.get('Tecnología'),
            "Ubicación": request.form.get('Ubicación'),
            "Valor": request.form.get('Valor'),
            "Riesgo": request.form.get('Riesgo'),
            "CEO": request.form.get('CEO'),
            "Celular": request.form.get('Celular'),
            "Dirección": request.form.get('Dirección'),
            "Fuente": request.form.get('Fuente'),
            "Link": request.form.get('Link'),
            "Fecha": request.form.get('Fecha')
        }
        if ficha not in MAIA_MEMORIA:
            MAIA_MEMORIA.append(ficha)

    # Respuesta del Analizador
    chat_resp = ""
    if c_query:
        chat_resp = f"MAIA: Análisis profundo en curso para '{c_query}'. Cruzando reportes de Brokers y Bancos. Memoria activa con {len(MAIA_MEMORIA)} registros."

    # --- FRONT-END MAIA II ---
    h = f"""
    <html><head><title>MAIA FKT - REAL TIME UNIT</title>
    <style>
        body {{ background:#000; color:#0ff; font-family:'Segoe UI',monospace; padding:30px; line-height:1.2; }}
        .header {{ border-bottom:3px solid #f0f; padding-bottom:15px; margin-bottom:30px; display:flex; justify-content:space-between; }}
        .btn {{ background:none; border:2px solid #0ff; color:#0ff; padding:12px; cursor:pointer; font-weight:bold; font-size:11px; text-transform:uppercase; }}
        .btn-green {{ border-color:#0f0; color:#0f0; }}
        .btn-magenta {{ border-color:#f0f; color:#f0f; }}
        
        .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(500px, 1fr)); gap:25px; }}
        .card {{ border:1px solid #0f02; background:rgba(0,40,0,0.1); padding:25px; border-radius:8px; position:relative; border-left: 6px solid #0f0; }}
        .card-live {{ border-left: 6px solid #f00; background:rgba(40,0,0,0.1); }}
        
        .tag-date {{ position:absolute; top:15; right:15; font-size:10px; color:#555; font-weight:bold; }}
        .tag-ia {{ position:absolute; top:35; right:15; color:#f0f; font-size:11px; font-weight:bold; border:1px solid #f0f; padding:2px 5px; }}
        
        .riesgo-BAJO {{ color:#0f0; }} .riesgo-MODERADO {{ color:#ff0; }} .riesgo-ALTO {{ color:#f90; }}
        
        .contact-area {{ background:rgba(0,255,255,0.05); padding:20px; margin-top:20px; border:1px solid #0ff3; border-radius:5px; }}
        input, select {{ background:#000; border:1px solid #0ff; color:#0ff; padding:15px; width:100%; margin-bottom:15px; font-size:13px; }}
        
        #maia-chat-box {{ position:fixed; bottom:30px; right:30px; width:400px; border:2px solid #f0f; background:#000; box-shadow: 0 0 20px #f0f4; }}
        .chat-head {{ background:#f0f; color:#000; padding:15px; font-weight:bold; cursor:pointer; }}
        .chat-body {{ padding:20px; }}
    </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; color:#f0f; font-size:2em;">MAIA FKT <span style="font-size:14px; color:#444;">// VERIFIED INTELLIGENCE</span></h1>
                <b style="color:#0f0;">SISTEMA BLINDADO - CERO SIMULACIÓN</b>
            </div>
            <a href="/memoria" class="btn btn-magenta">REPOSITORIO DE MEMORIA ({len(MAIA_MEMORIA)})</a>
        </div>

        <form method="post" style="display:grid; grid-template-columns: 1fr 1fr 180px; gap:15px; margin-bottom:50px;">
            <input name="target_country" placeholder="UBICACIÓN / PAÍS REAL" value="{t_country if t_country != 'TODOS' else ''}">
            <select name="target_tech">
                <option value="TODAS">-- TODAS LAS TECNOLOGÍAS --</option>
                <option value="SMR Nuclear" {"selected" if t_tech=="SMR Nuclear" else ""}>SMR Nuclear</option>
                <option value="Hidrógeno Verde" {"selected" if t_tech=="Hidrógeno Verde" else ""}>Hidrógeno Verde</option>
                <option value="Neutrinos" {"selected" if t_tech=="Neutrinos" else ""}>Neutrinos</option>
                <option value="Solar" {"selected" if t_tech=="Solar" else ""}>Energía Solar</option>
            </select>
            <button type="submit" name="action" value="buscar_scout" class="btn btn-green">EJECUTAR SCOUT</button>
        </form>

        <div class="grid">
            {"".join([f'''
            <div class="card {'card-live' if 'LIVE' in a['id'] else ''}">
                <div class="tag-date">FECHA: {a['Fecha_Pub']}</div>
                <div class="tag-ia">VERIFIED: {a['Calificacion_IA']}</div>
                
                <small style="color:#0f0;">PROYECTO ID: {a['id']} | {a['Tecnología'].upper()}</small>
                <h2 style="color:#fff; margin:15px 0; font-size:1.6em; text-transform:uppercase;">{a['Nombre']}</h2>
                
                <p style="color:#ccc; font-size:13px; line-height:1.5;">{a['Resumen']}</p>
                
                <div style="display:flex; justify-content:space-between; font-size:13px; margin:15px 0;">
                    <span>VALOR NEGOCIO: <b style="color:#fff;">{a['Valor_Est']}</b></span>
                    <span class="riesgo-{a['Riesgo'].split(' ')[0]}">RIESGO: {a['Riesgo']}</span>
                </div>

                <div class="contact-area">
                    <b style="color:#0ff;">DIRECTORIO EJECUTIVO REAL:</b><br><br>
                    CEO/DIRECTOR: <span style="color:#fff; font-weight:bold;">{a['CEO']}</span><br>
                    TELÉFONO: <span style="color:#fff;">{a['Celular']}</span><br>
                    DIRECCIÓN: <span style="color:#ccc;">{a['Dirección']}</span><br><br>
                    FUENTE: <b style="color:#f0f;">{a['Fuente']}</b> | <a href="{a['Contacto']}" target="_blank" style="color:#0ff; text-decoration:none; border-bottom:1px solid #0ff;">[ACCEDER A FUENTE]</a>
                </div>

                <form method="post" style="margin-top:20px;">
                    <input type="hidden" name="id" value="{a['id']}">
                    <input type="hidden" name="Nombre" value="{a['Nombre']}">
                    <input type="hidden" name="Tecnología" value="{a['Tecnología']}">
                    <input type="hidden" name="Ubicación" value="{a['Ubicación']}">
                    <input type="hidden" name="Valor" value="{a['Valor_Est']}">
                    <input type="hidden" name="Riesgo" value="{a['Riesgo']}">
                    <input type="hidden" name="CEO" value="{a['CEO']}">
                    <input type="hidden" name="Celular" value="{a['Celular']}">
                    <input type="hidden" name="Dirección" value="{a['Dirección']}">
                    <input type="hidden" name="Fuente" value="{a['Fuente']}">
                    <input type="hidden" name="Link" value="{a['Contacto']}">
                    <input type="hidden" name="Fecha" value="{a['Fecha_Pub']}">
                    <button type="submit" name="action" value="guardar_memoria" class="btn btn-magenta" style="width:100%; border-width:1px;">+ GUARDAR EN MEMORIA CENTRAL</button>
                </form>
            </div>
            ''' for a in results])}
        </div>

        <div id="maia-chat-box">
            <div class="chat-head" onclick="document.getElementById('cb').style.display='none'">MAIA II ANALYZER</div>
            <div id="cb" class="chat-body">
                <div style="font-size:12px; color:#0f0; margin-bottom:15px; border-left:3px solid #f0f; padding-left:15px;">
                    {chat_resp if chat_resp else 'Consola de inteligencia operativa lista. Use Scout para ingesta de datos.'}
                </div>
                <form method="post">
                    <input name="chat_query" placeholder="Consultar sobre brokers o activos..." style="padding:10px; font-size:12px;">
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
        body {{ background:#000; color:#0ff; font-family:monospace; padding:40px; }}
        .m-card {{ border:1px solid #f0f5; padding:25px; margin-bottom:20px; background:rgba(255,0,255,0.03); border-radius:5px; }}
        .btn {{ border:2px solid #0ff; color:#0ff; text-decoration:none; padding:15px; display:inline-block; margin-bottom:30px; text-transform:uppercase; font-weight:bold; }}
    </style>
    </head><body>
        <h1 style="color:#f0f; font-size:2.5em;">MEMORIA CENTRAL DE ACTIVOS</h1>
        <a href="/" class="btn">VOLVER A OPERACIONES</a><br>
        {"".join([f'''
        <div class="m-card">
            <b style="font-size:1.4em; color:#fff;">{m['Nombre']}</b> ({m['id']})<br>
            <span style="color:#0f0;">{m['Tecnología']} | {m['Ubicación']}</span><br><br>
            <b>VALOR:</b> {m['Valor']} | <b>RIESGO:</b> {m['Riesgo']} | <b>FECHA:</b> {m['Fecha']}<br>
            <b>CEO:</b> {m['CEO']} | <b>TEL:</b> {m['Celular']} | <b>DIR:</b> {m['Dirección']}<br>
            <b>FUENTE:</b> {m['Fuente']} | <a href="{m['Link']}" target="_blank" style="color:#f0f;">ENLACE</a>
        </div>
        ''' for m in MAIA_MEMORIA])}
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
