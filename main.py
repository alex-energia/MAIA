# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = os.urandom(256)

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
        <title>MAIA - NIVEL 600: BUSINESS RADAR</title>
        <style>
            :root { --blue: #00ffff; --gold: #ffd700; --red: #ff3e3e; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:'Segoe UI', sans-serif; margin:0; padding:20px; font-size:13px; }
            
            .header { border-bottom: 2px solid #111; padding-bottom:15px; display:flex; gap:15px; align-items:center; }
            .btn-nav { background:none; border:1px solid #222; color:#444; padding:8px 15px; cursor:pointer; font-weight:bold; font-size:10px; }
            .active { border-color:var(--blue); color:var(--blue); }

            #bar-cont { width:100%; height:8px; background:#050505; margin:30px 0; display:none; border: 1px solid #222; }
            #bar-fill { height:100%; background: linear-gradient(90deg, var(--red), var(--gold), var(--blue)); width:0%; transition: 0.1s; }
            #status-txt { display:none; color:var(--blue); font-size:10px; margin-bottom:10px; font-weight:bold; }

            .btn-scan { background:#000; border:2px solid var(--blue); color:var(--blue); padding:25px; width:100%; cursor:pointer; font-weight:900; text-transform:uppercase; letter-spacing:2px; }
            .btn-scan:hover { background:var(--blue); color:#000; box-shadow: 0 0 20px var(--blue); }
            
            .ficha { background:#030303; border:1px solid #111; border-left:4px solid var(--blue); padding:25px; margin-top:25px; }
            .pilar-tag { font-size:9px; color:var(--gold); border:1px solid var(--gold); padding:2px 6px; font-weight:bold; }
            .title { font-size:17px; color:#fff; margin:15px 0; font-weight:bold; }
            .desc { color:#666; font-size:13px; line-height:1.6; background:rgba(0,0,0,0.5); padding:15px; }

            /* CHAT TOTALMENTE MINIMIZADO Y VACÍO */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:360px; border:1px solid #1a1a1a; background:#000; z-index:9999; }
            .chat-h { background:#050505; color:var(--blue); padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; font-size:11px; }
            #chat-b, #cInput { display:none; }
            #chat-b { height:180px; padding:15px; overflow-y:auto; font-size:11px; border-bottom:1px solid #111; }
        </style>
    </head>
    <body>
        <div class="header">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">RADAR 600</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; border-color:var(--red); color:var(--red);">WIPE SESSION</button>
            </form>
        </div>

        <div id="bar-cont"><div id="bar-fill"></div></div>
        <div id="status-txt">SISTEMA NIVEL 600: OPERATIVO</div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn-scan">EJECUTAR INFILTRACIÓN DE NEGOCIOS Y PROYECTOS</button>
            </form>

            {% for r in session['history'] %}
            <div class="ficha">
                <span class="pilar-tag">{{ r.pilar }}</span>
                <div class="title">{{ r.nombre }}</div>
                <div class="desc">{{ r.datos }}</div>
                <div style="margin-top:20px; display:flex; gap:15px;">
                    <a href="{{ r.vinculo }}" target="_blank" style="color:var(--blue); text-decoration:none; font-weight:bold;">[ ACCEDER AL PROYECTO ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--gold); cursor:pointer; font-family:inherit; font-weight:bold;">[ ARCHIVAR ]</button></form>
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
            <div class="chat-h" onclick="toggle()"><span>MAIA CONSOLE v6.0</span><span id="ico">[+]</span></div>
            <div id="chat-b"></div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--blue); padding:15px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function start() {
                document.getElementById('bar-cont').style.display = 'block';
                document.getElementById('status-txt').style.display = 'block';
                var fill = document.getElementById('bar-fill');
                var txt = document.getElementById('status-txt');
                var w = 0;
                var itv = setInterval(function(){
                    w += 1; fill.style.width = w + '%';
                    if(w < 20) txt.innerText = "ACCEDIENDO A NODOS DE LICITACIÓN (PILAR 1-3)...";
                    else if(w < 50) txt.innerText = "CAPTURANDO CONTRATOS EPC (PILAR 4-5)...";
                    else if(w < 80) txt.innerText = "ESCANEANDO ACUERDOS DE INVERSIÓN (PILAR 6-8)...";
                    else txt.innerText = "COMPILANDO RESULTADOS DE NEGOCIO...";
                    if(w >= 100) { clearInterval(itv); document.getElementById('scoutF').submit(); }
                }, 100); 
            }
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div style='color:var(--blue); margin-top:5px;'> > "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)