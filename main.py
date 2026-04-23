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
        <title>MAIA - INFILTRACIÓN 300</title>
        <style>
            :root { --cian: #00f2ff; --gold: #ffcc00; --red: #ff0044; --bg: #020202; }
            body { background:var(--bg); color:#fff; font-family:monospace; margin:0; padding:20px; font-size:13px; }
            
            .nav { border-bottom: 2px solid #1a1a1a; padding-bottom:15px; display:flex; gap:15px; }
            .btn-nav { background:none; border:1px solid #333; color:#555; padding:8px 15px; cursor:pointer; }
            .active { border-color:var(--cian); color:var(--cian); box-shadow: 0 0 10px var(--cian); }

            #bar-cont { width:100%; height:12px; background:#0a0a0a; margin:30px 0; display:none; border: 1px solid #333; }
            #bar-fill { height:100%; background: linear-gradient(90deg, var(--red), var(--gold), var(--cian)); width:0%; }
            #status-txt { display:none; color:var(--cian); font-size:10px; margin-bottom:10px; font-weight:bold; }

            .btn-scan { background:#000; border:2px solid var(--cian); color:var(--cian); padding:25px; width:100%; cursor:pointer; font-weight:800; text-transform:uppercase; transition: 0.4s; }
            .btn-scan:hover { background:var(--cian); color:#000; }
            
            .ficha { background:#080808; border:1px solid #1a1a1a; border-left:4px solid var(--cian); padding:25px; margin-top:25px; }
            .pilar-tag { font-size:9px; color:var(--gold); border:1px solid var(--gold); padding:2px 6px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:380px; border:1px solid #222; background:#000; z-index:999; }
            .chat-h { background:#111; color:var(--cian); padding:15px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b, #cInput { display:none; }
            #chat-b { height:220px; padding:15px; overflow-y:auto; font-size:11px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">RADAR 300</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; border-color:var(--red); color:var(--red);">RESETEAR</button>
            </form>
        </div>

        <div id="bar-cont"><div id="bar-fill"></div></div>
        <div id="status-txt">STANDBY...</div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn-scan">INICIAR BARRIDO AGRESIVO</button>
            </form>
            {% for r in session['history'] %}
            <div class="ficha">
                <span class="pilar-tag">{{ r.pilar }}</span>
                <div style="font-size:18px; margin:15px 0;">{{ r.nombre }}</div>
                <div style="color:#777;">{{ r.datos }}</div>
                <div style="margin-top:20px; display:flex; gap:15px;">
                    <a href="{{ r.vinculo }}" target="_blank" style="color:var(--cian); text-decoration:none;">[ EXPEDIENTE ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--gold); cursor:pointer;">[ ARCHIVAR ]</button></form>
                </div>
            </div>
            {% endfor %}
        {% else %}
            {% for s in session['saved'] %}
            <div class="ficha" style="border-left-color:var(--gold);">
                <span class="pilar-tag">{{ s.pilar }}</span>
                <div style="font-size:18px; margin:15px 0;">{{ s.nombre }}</div>
                <div style="color:#777;">{{ s.datos }}</div>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA CONSOLE</span><span id="ico">[+]</span></div>
            <div id="chat-b"></div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--cian); padding:15px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function start() {
                document.getElementById('bar-cont').style.display = 'block';
                document.getElementById('status-txt').style.display = 'block';
                var fill = document.getElementById('bar-fill');
                var w = 0;
                var itv = setInterval(function(){
                    w += 1; fill.style.width = w + '%';
                    if(w >= 100) { clearInterval(itv); document.getElementById('scoutF').submit(); }
                }, 150); // 15 segundos de carga visual antes de la petición
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
