# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_infra_aggressive_170"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    if 'attempt' not in session: session['attempt'] = False
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.execute_global_scout()
            session['attempt'] = True
            session.modified = True
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item); session.modified = True
        elif action == 'limpiar':
            session.clear()
            return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA - NIVEL 170 (INFRASTRUCTURE INFILTRATION)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --alert: #ff0055; --bg: #030303; }
            body { background:var(--bg); color:#fff; font-family:'Segoe UI', sans-serif; margin:0; padding:20px; }
            .nav { display:flex; gap:10px; border-bottom:1px solid #222; padding-bottom:15px; }
            .btn { background:none; border:1px solid #444; color:#888; padding:10px 20px; cursor:pointer; font-weight:bold; font-size:11px; text-transform:uppercase; transition:0.2s; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active { background:var(--neon); color:#000; border-color:var(--neon); box-shadow: 0 0 15px var(--neon); }
            
            #st-cont { width:100%; height:4px; background:#111; margin:20px 0; display:none; }
            #st-bar { height:100%; background:var(--neon); width:0%; transition:0.01s; }

            .alert-box { background: rgba(255,0,85,0.05); border: 1px solid var(--alert); padding:40px; text-align:center; margin-top:20px; }
            .alert-box h2 { color: var(--alert); margin:0; font-size: 14px; letter-spacing: 3px; }
            
            .ficha { background:#0a0a0a; border:1px solid #1a1a1a; padding:35px; margin-top:25px; border-top: 2px solid var(--neon); }
            .asset-title { color: var(--neon); font-size: 20px; margin-bottom: 20px; font-weight: 800; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin:20px 0; }
            .label { color:#555; font-size:9px; font-weight: bold; text-transform: uppercase; }
            .val { font-size: 13px; color: #ccc; }
            .resumen-box { background:#000; border:1px solid #222; padding:20px; color:#888; font-size:14px; line-height:1.6; margin-top: 15px; }

            /* CHAT ESTRICTAMENTE MINIMIZADO */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid #222; background:#000; z-index:10000; }
            .chat-h { background:#111; color:var(--neon); padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b, #cInput { display:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">GRID SCANNER 170</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">ARCHIVOS ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto; border-color:var(--alert); color:var(--alert);">WIPE</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; height:80px; border-color:var(--gold); color:var(--gold); font-size:15px;">FORZAR INFILTRACIÓN EN REGISTROS DE RED Y PERMISOS ESTATALES</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="alert-box">
                    <h2>[ ERROR: BLOQUEO DE CAPA DE RED ]</h2>
                    <p style="color:#666; font-size:12px; margin-top:10px;">Los activos están protegidos por cortafuegos de sesión gubernamental.<br>
                    <a href="https://www.google.com/search?q=site:gov+filetype:pdf+Interconnection+Queue+Hydrogen+2026" target="_blank" style="color:var(--gold);">[ CLICK AQUÍ PARA BYPASS MANUAL ]</a></p>
                </div>
            {% endif %}

            {% for r in session['history'] %}
            <div class="ficha">
                <div class="asset-title">{{ r.nombre }}</div>
                <div class="grid">
                    <div><span class="label">ID INFRA</span><br><span class="val">{{ r.id }}</span></div>
                    <div><span class="label">ESTADO LEGAL</span><br><span class="val">{{ r.riesgo }}</span></div>
                    <div><span class="label">VIGENCIA</span><br><span class="val">{{ r.fecha }}</span></div>
                </div>
                <div class="resumen-box">
                    {{ r.resumen }}
                    <br><br>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--neon); text-decoration:none;">[ ABRIR EXPEDIENTE TÉCNICO ]</a>
                </div>
                <form method="POST" style="margin-top:15px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="border-color:var(--gold); color:var(--gold); font-size:9px;">ARCHIVAR POSITIVO</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA DEEP CMD</span><span id="ico">[+]</span></div>
            <div id="chat-b" style="padding:20px; height:250px; overflow-y:auto; font-size:12px; color:#444; border-bottom:1px solid #111;">
                <div style="color:var(--gold);">> Infiltración 170 lista.</div>
            </div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--neon); padding:15px; box-sizing: border-box; outline:none;">
        </div>

        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div> > "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ w+=4; b.style.width=w+'%'; if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }}, 30);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)