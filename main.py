# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = os.urandom(512) # Máxima seguridad de sesión

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
        <title>MAIA - NIVEL 700 (REAL-TIME ASSETS)</title>
        <style>
            :root { --cian: #00ffff; --gold: #ffd700; --red: #ff4d4d; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:'Segoe UI', sans-serif; margin:0; padding:20px; }
            .nav { border-bottom: 2px solid #111; padding-bottom:15px; display:flex; gap:10px; }
            .btn-nav { background:#0a0a0a; border:1px solid #333; color:#555; padding:10px 15px; cursor:pointer; font-weight:bold; font-size:10px; }
            .active { border-color:var(--cian); color:var(--cian); box-shadow: 0 0 15px rgba(0,255,255,0.2); }
            
            #prog-c { width:100%; height:4px; background:#050505; margin:30px 0; display:none; }
            #prog-f { height:100%; background:var(--cian); width:0%; transition: 0.3s; }
            #status { display:none; color:var(--cian); font-size:10px; margin-bottom:10px; font-weight:bold; letter-spacing:1px; }

            .btn-scan { background:#000; border:2px solid var(--cian); color:var(--cian); padding:30px; width:100%; cursor:pointer; font-weight:900; font-size:16px; text-transform:uppercase; transition: 0.3s; }
            .btn-scan:hover { background:var(--cian); color:#000; }
            
            .ficha { background:#030303; border:1px solid #111; border-left:4px solid var(--cian); padding:25px; margin-top:20px; }
            .pilar-tag { font-size:9px; color:var(--gold); border:1px solid var(--gold); padding:2px 6px; font-weight:bold; }
            .title { font-size:18px; margin:15px 0; font-weight:bold; color:#fff; }
            .desc { color:#888; font-size:13px; line-height:1.6; background:rgba(255,255,255,0.02); padding:15px; }

            /* CHAT: 100% LIMPIO Y MINIMIZADO */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:350px; border:1px solid #1a1a1a; background:#000; z-index:999; }
            .chat-h { background:#050505; color:var(--cian); padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; font-size:11px; }
            #chat-b, #cInput { display:none; }
            #chat-b { height:180px; padding:15px; overflow-y:auto; font-size:11px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn-nav {{ 'active' if view == 'scout' }}">SCANNER 700</button>
                <button type="submit" name="view_state" value="memoria" class="btn-nav {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn-nav" style="margin-left:auto; border-color:var(--red); color:var(--red);">RESETEAR</button>
            </form>
        </div>

        <div id="prog-c"><div id="prog-f"></div></div>
        <div id="status">RADAR ACTIVO...</div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn-scan">INFILTRACIÓN GLOBAL DE ACTIVOS 2026</button>
            </form>

            {% for r in session['history'] %}
            <div class="ficha">
                <span class="pilar-tag">{{ r.pilar }}</span>
                <div class="title">{{ r.nombre }}</div>
                <div class="desc">{{ r.datos }}</div>
                <div style="margin-top:20px; display:flex; gap:15px; align-items:center;">
                    <a href="{{ r.vinculo }}" target="_blank" style="color:var(--cian); text-decoration:none; font-weight:bold; font-size:11px;">[ VER CONTRATO ]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" style="background:none; border:none; color:var(--gold); cursor:pointer; font-weight:bold; font-size:11px;">[ GUARDAR ]</button></form>
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
            <div class="chat-h" onclick="toggle()"><span>MAIA CONSOLE v7.0</span><span id="ico">[+]</span></div>
            <div id="chat-b"></div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--cian); padding:15px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function start() {
                document.getElementById('prog-c').style.display = 'block';
                document.getElementById('status').style.display = 'block';
                var fill = document.getElementById('prog-f');
                var txt = document.getElementById('status');
                var w = 0;
                var itv = setInterval(function(){
                    w += 2; fill.style.width = w + '%';
                    if(w < 30) txt.innerText = "ACCEDIENDO A CONTRATOS SMR Y SOLAR (ABRIL 2026)...";
                    else if(w < 70) txt.innerText = "CAPTURANDO LICITACIONES DOE Y UE (PILARES 4-7)...";
                    else txt.innerText = "FINALIZANDO EXTRACCIÓN DE STARTUPS...";
                    if(w >= 100) { clearInterval(itv); document.getElementById('scoutF').submit(); }
                }, 80); 
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