# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)

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
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA - NIVEL 300 (DEEP INFILTRATION)</title>
        <style>
            :root { --cian: #00f2ff; --gold: #ffcc00; --red: #ff0044; --bg: #020202; }
            body { background:var(--bg); color:#fff; font-family:'Segoe UI', monospace; margin:0; padding:20px; font-size:13px; }
            
            .nav { border-bottom: 2px solid #1a1a1a; padding-bottom:15px; display:flex; gap:15px; align-items:center; }
            .btn-nav { background:none; border:1px solid #333; color:#555; padding:8px 15px; cursor:pointer; font-weight:bold; }
            .active { border-color:var(--cian); color:var(--cian); box-shadow: 0 0 10px rgba(0,242,255,0.3); }

            #bar-cont { width:100%; height:12px; background:#0a0a0a; margin:30px 0; display:none; border: 1px solid #333; border-radius: 2px; }
            #bar-fill { height:100%; background: linear-gradient(90deg, var(--red), var(--gold), var(--cian)); width:0%; transition: 0.1s; }
            #status-txt { display:none; color:var(--cian); font-size:10px; margin-bottom:10px; letter-spacing:2px; font-weight:bold; }

            .btn-scan { 
                background: #000; border: 2px solid var(--cian); color: var(--cian); 
                padding: 25px; width: 100%; cursor: pointer; font-weight: 800; font-size: 16px;
                text-transform: uppercase; margin-top:10px; transition: 0.4s;
            }
            .btn-scan:hover { background: var(--cian); color: #000; box-shadow: 0 0 50px var(--cian); }
            
            .ficha { background: #080808; border: 1px solid #1a1a1a; border-left: 4px solid var(--cian); padding:25px; margin-top:25px; position:relative; }
            .pilar-tag { font-size:9px; color:var(--gold); border:1px solid var(--gold); padding:2px 6px; font-weight:bold; }
            .title { font-size:18px; color:#fff; margin:15px 0; font-weight: bold; }
            .desc { color:#999; font-size:13px; line-height:1.6; background:rgba(0,0,0,0.5); padding:15px; border-radius:4px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:380px; border:1px solid #222; background:#000; box-shadow: 0 0 30px rgba(0,0,0,1); z-index:999; }
            .chat-h { background:#111; color:var(--cian); padding:15px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; font-size:11px; }
            #chat-b, #cInput { display:none; }
            #chat-b { height:220px; padding:15px; overflow-y:auto; font-size:11px; color:#444; border-bottom:1px solid #111; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">RADAR 300</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">PORTAFOLIO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; border-color:var(--red); color:var(--red);">RESETEAR</button>
            </form>
        </div>

        <div id="bar-cont"><div id="bar-fill"></div></div>
        <div id="status-txt">PROTOCOLO NIVEL 300: STANDBY</div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn-scan">INICIAR INFILTRACIÓN AGRESIVA DE ACTIVOS</button>
            </form>

            {% for r in session['history'] %}
            <div class="ficha">
                <span class="pilar-tag">{{ r.pilar }}</span>
                <div class="title">{{ r.nombre }}</div>
                <div class="desc">{{ r.datos }}</div>
                <div style="margin-top:20px; display:flex; gap:15px; align-items:center;">
                    <a href="{{ r.vinculo }}" target="_blank" style="color:var(--cian); text-decoration:none; font-weight:bold;">[ EXPEDIENTE ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--gold); cursor:pointer; font-family:inherit; font-weight:bold;">[ CAPTURAR ACTIVO ]</button></form>
                </div>
            </div>
            {% endfor %}
        {% else %}
            {% for s in session['saved'] %}
            <div class="ficha" style="border-left-color:var(--gold);">
                <span class="pilar-tag">{{ s.pilar }}</span>
                <div class="title">{{ s.nombre }}</div>
                <div class="desc">{{ s.datos }}</div>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA DEEP-CORE TERMINAL</span><span id="ico">[+]</span></div>
            <div id="chat-b"></div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--cian); padding:15px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function start() {
                var cont = document.getElementById('bar-cont');
                var fill = document.getElementById('bar-fill');
                var txt = document.getElementById('status-txt');
                cont.style.display = 'block'; txt.style.display = 'block';
                var w = 0;
                var itv = setInterval(function(){
                    w += 0.25; fill.style.width = w + '%';
                    if(w < 12.5) txt.innerText = "PENETRANDO: NODOS HIDROELÉCTRICOS...";
                    else if(w < 25) txt.innerText = "PENETRANDO: ACTIVOS SOLARES UTILITY...";
                    else if(w < 37.5) txt.innerText = "PENETRANDO: ESTRUCTURAS SMR NUCLEAR...";
                    else if(w < 50) txt.innerText = "PENETRANDO: CONTRATOS TÉRMICOS EPC...";
                    else if(w < 62.5) txt.innerText = "PENETRANDO: POZOS GEOTÉRMICOS...";
                    else if(w < 75) txt.innerText = "PENETRANDO: NODOS NEUTRINO ENERGY...";
                    else if(w < 87.5) txt.innerText = "PENETRANDO: PROYECTOS HIDRÓGENO FID...";
                    else txt.innerText = "PENETRANDO: STARTUPS DE TECNOLOGÍA...";
                    
                    if(w >= 100) { clearInterval(itv); document.getElementById('scoutF').submit(); }
                }, 120); 
            }
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div style='color:var(--cian); margin-top:5px;'> > "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
