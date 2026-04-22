# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_ghost_180"

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
        <title>MAIA - NIVEL 180 (GHOST SCAN)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --bg: #020202; }
            body { background:var(--bg); color:#fff; font-family:'Courier New', monospace; margin:0; padding:20px; font-size:12px; }
            .nav { display:flex; gap:10px; border-bottom:1px solid #222; padding-bottom:15px; }
            .btn { background:none; border:1px solid #333; color:#555; padding:10px 20px; cursor:pointer; font-weight:bold; text-transform:uppercase; transition:0.2s; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active { background:var(--neon); color:#000; border-color:var(--neon); box-shadow: 0 0 20px var(--neon); }
            
            #st-cont { width:100%; height:2px; background:#111; margin:20px 0; display:none; }
            #st-bar { height:100%; background:var(--neon); width:0%; transition:0.01s; }

            .bypass-panel { background:#110000; border:1px solid #ff0055; padding:30px; margin-top:20px; text-align:center; }
            .bypass-panel h2 { color:#ff0055; margin:0 0 10px 0; font-size:14px; }
            
            .ficha { background:#0a0a0a; border:1px solid #1a1a1a; padding:30px; margin-top:25px; border-left: 2px solid var(--neon); position: relative; }
            .ficha::after { content: "DATO POSITIVO"; position: absolute; top: 10px; right: 10px; font-size: 8px; color: var(--gold); border: 1px solid var(--gold); padding: 2px 5px; }
            
            .asset-title { color: var(--neon); font-size: 16px; margin-bottom: 15px; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin:15px 0; }
            .label { color:#444; font-size:8px; font-weight: bold; }
            .val { color: #aaa; }
            
            /* CHAT TOTALMENTE MINIMIZADO */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid #222; background:#000; z-index:1000; }
            .chat-h { background:#111; color:var(--neon); padding:10px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b, #cInput { display:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">GHOST SCANNER 180</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">PORTAFOLIO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto;">REINICIAR</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; height:70px; border-color:var(--gold); color:var(--gold);">INFILTRAR NODOS DE SUBASSTA Y METADATOS (MODO GHOST)</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="bypass-panel">
                    <h2>ALERTA: BLOQUEO PERSISTENTE DE CAPA DE RED</h2>
                    <p style="color:#888; font-size:11px;">El cortafuegos detectó la firma de MAIA. Activa el Bypass Manual para inyectar la búsqueda desde tu IP:</p>
                    <a href="https://www.google.com/search?q=site:gov+2026+award+SMR+OR+Hydrogen+OR+Neutrino" target="_blank" style="color:var(--gold); text-decoration:none; border:1px solid var(--gold); padding:10px 20px; display:inline-block; margin-top:10px;">[ FORZAR INYECCIÓN MANUAL ]</a>
                </div>
            {% endif %}

            {% for r in session['history'] %}
            <div class="ficha">
                <div class="asset-title">{{ r.nombre }}</div>
                <div class="grid">
                    <div><span class="label">ID GHOST</span><br><span class="val">{{ r.id }}</span></div>
                    <div><span class="label">ESTADO ACTIVO</span><br><span class="val">{{ r.riesgo }}</span></div>
                    <div><span class="label">ORIGEN</span><br><span class="val">{{ r.movil }}</span></div>
                </div>
                <div style="background:#000; padding:15px; border:1px solid #111; color:#777; line-height:1.5;">
                    {{ r.resumen }}
                    <br><br>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--neon);">[ EXTRAER EXPEDIENTE ]</a>
                </div>
                <form method="POST" style="margin-top:15px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="border-color:var(--gold); color:var(--gold); font-size:9px;">ARCHIVAR POSITIVO</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA CMD</span><span id="ico">[+]</span></div>
            <div id="chat-b" style="padding:15px; height:200px; overflow-y:auto; color:#444;">
                <div>> Nivel 180 Activo. Infiltración silenciosa en curso...</div>
            </div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--neon); padding:12px; box-sizing:border-box; outline:none;">
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
                var itv=setInterval(function(){ w+=2; b.style.width=w+'%'; if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }}, 35);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)