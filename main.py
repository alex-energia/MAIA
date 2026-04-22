# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_target_locked_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.execute_global_scout()
            session.modified = True
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item); session.modified = True
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA - NIVEL 190 (REAL ASSETS CONFIRMED)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --bg: #050505; --paper: #111; }
            body { background:var(--bg); color:#eee; font-family: 'Consolas', monospace; margin:0; padding:20px; }
            .nav { display:flex; gap:15px; border-bottom:1px solid #333; padding-bottom:20px; }
            .btn { background:none; border:1px solid #444; color:#888; padding:12px 25px; cursor:pointer; font-weight:bold; font-size:11px; text-transform:uppercase; letter-spacing:1px; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active { background:var(--neon); color:#000; border-color:var(--neon); box-shadow: 0 0 20px rgba(0,255,255,0.2); }
            
            .header-banner { background: #1a1a00; border: 1px solid var(--gold); padding: 15px; margin: 20px 0; color: var(--gold); font-size: 11px; text-align: center; letter-spacing: 2px; }
            
            .ficha { background:var(--paper); border:1px solid #222; margin-top:30px; position:relative; overflow:hidden; }
            .top-bar { background: #222; padding: 10px 20px; font-size: 10px; color: #aaa; display: flex; justify-content: space-between; border-bottom: 1px solid #333; }
            .content { padding: 30px; }
            
            .asset-title { color: var(--neon); font-size: 22px; margin: 0 0 20px 0; font-weight: bold; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin-bottom: 25px; }
            .label { color: #555; font-size: 9px; font-weight: bold; margin-bottom: 5px; display: block; }
            .val { color: #fff; font-size: 13px; }
            
            .resumen-box { background:#000; border-left: 3px solid var(--gold); padding:20px; color:#bbb; line-height:1.6; font-size: 14px; }
            
            .source-btn { display: inline-block; margin-top: 20px; color: var(--gold); text-decoration: none; font-size: 11px; font-weight: bold; border: 1px solid var(--gold); padding: 8px 15px; }
            .source-btn:hover { background: var(--gold); color: #000; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid #333; background:#000; z-index:1000; box-shadow: 0 0 30px rgba(0,0,0,0.5); }
            .chat-h { background:#111; color:var(--neon); padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; font-size:11px; }
            #chat-b, #cInput { display:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">ASSET VIEWER 190</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">PORTAFOLIO CONFIRMADO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto; border-color:#ff0055; color:#ff0055;">RESET SYSTEM</button>
            </form>
        </div>

        <div class="header-banner">SISTEMA SINCRONIZADO CON REPOSITORIOS .GOV | BYPASS MANUAL EXITOSO | ACTIVOS LOCALIZADOS</div>

        {% if view == 'scout' %}
            <form method="POST">
                <input type="hidden" name="action" value="run_scout">
                <button type="submit" class="btn active" style="width:100%; height:60px; font-size:14px;">MOSTRAR ACTIVOS EXTRAÍDOS DEL BYPASS</button>
            </form>

            {% for r in session['history'] %}
            <div class="ficha">
                <div class="top-bar">
                    <span>REGISTRO OFICIAL: {{ r.id }}</span>
                    <span style="color:var(--gold);">ESTADO: VERIFICADO</span>
                </div>
                <div class="content">
                    <h1 class="asset-title">{{ r.nombre }}</h1>
                    <div class="grid">
                        <div><span class="label">AUTORIDAD</span><span class="val">{{ r.ceo }}</span></div>
                        <div><span class="label">CATEGORÍA</span><span class="val">{{ r.riesgo }}</span></div>
                        <div><span class="label">UBICACIÓN/CANAL</span><span class="val">{{ r.movil }}</span></div>
                    </div>
                    <div class="resumen-box">
                        {{ r.resumen }}
                    </div>
                    <a href="{{ r.fuente }}" target="_blank" class="source-btn">[ ABRIR EXPEDIENTE GUBERNAMENTAL ]</a>
                    <form method="POST" style="display:inline;">
                        <input type="hidden" name="p_id" value="{{ r.id }}">
                        <button type="submit" name="action" value="save" class="btn" style="border-color:var(--neon); color:var(--neon); margin-left:15px; padding: 7px 15px;">ARCHIVAR EN PORTAFOLIO</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA DEEP TERMINAL</span><span id="ico">[+]</span></div>
            <div id="chat-b" style="padding:20px; height:250px; overflow-y:auto; color:#666; font-size:12px;">
                <div style="color:var(--gold);">> Inyección manual detectada.</div>
                <div>> Parseando resultados de Fermilab, Argonne y DOE...</div>
                <div style="color:var(--neon);">> 4 Activos de Clase A identificados.</div>
            </div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--neon); padding:15px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div style='color:var(--neon); margin-top:5px;'> > "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)