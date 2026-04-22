# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_ultra_agressive_64"

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
            if item: session['saved'].append(item); session.modified = True
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA - NIVEL 64 (INFILTRACIÓN)</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; --red: #ff0033; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; padding-bottom:180px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--red); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--red); color:#fff; border-color:var(--red); box-shadow: 0 0 10px var(--red); }
            
            #st-cont { width:100%; height:15px; background:#111; margin:15px 0; display:none; border:1px solid #444; }
            #st-bar { height:100%; background:var(--red); width:0%; transition:0.2s; }

            .alert-null { border: 3px solid var(--red); background: rgba(255,0,0,0.2); color: #fff; padding: 50px; text-align: center; margin-top: 20px; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--red); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin:15px 0; }
            .label { color:var(--pink); font-size:10px; display:block; }
            
            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:2px solid var(--red); background:#000; z-index:10000; }
            .chat-h { background:var(--red); color:#fff; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { display:none; height:280px; padding:15px; overflow-y:auto; font-size:12px; color:var(--green); border-top:1px solid var(--red); }
            #cInput { display:none; width:100%; background:#111; border:none; border-top:2px solid var(--red); color:var(--green); padding:15px; box-sizing: border-box; font-family:monospace; outline:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">INFILTRACIÓN 64</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">DATA ROOMS ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:gray; color:gray; margin-left:auto;">RESET</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; border-color:var(--red); color:var(--red); height:70px; font-size:18px; text-transform:uppercase;">Ejecutar Escaneo de Documentos de Inversión</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="alert-null">
                    <h1 style="margin:0;">[ FALLO DE DETECCIÓN ]</h1>
                    <p>MAIA no encontró documentos de oferta pública (.pdf/.doc) en el último mes para los parámetros de energía avanzada.</p>
                </div>
            {% endif %}
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID INFILTRACIÓN</span>{{ r.id }}</div>
                    <div><span class="label">PROMOTOR/BROKER</span>{{ r.ceo }}</div>
                    <div><span class="label">TIPO DE ACTIVO</span>{{ r.riesgo }}</div>
                    <div><span class="label">ACCESO</span>{{ r.movil }}</div>
                    <div><span class="label">INTEL E-MAIL</span>{{ r.email }}</div>
                    <div><span class="label">FECHA</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:20px; border:1px solid #222; margin-top:15px;">
                    <span class="label">EXTRACTO DEL DOCUMENTO</span>
                    <p style="color:#ccc; font-size:12px;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--red); font-weight:bold;">[INFILTRAR DOCUMENTO FUENTE]</a>
                </div>
                <form method="POST" style="margin-top:10px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:11px;">GUARDAR EN DATA ROOM</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA INFILTRATION UNIT</span><span id="ico">[+]</span></div>
            <div id="chat-b"></div>
            <input type="text" id="cInput" placeholder="Comando de infiltración..." onkeydown="if(event.key==='Enter') push()">
        </div>

        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div style='color:var(--red); margin-bottom:10px;'># "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ w+=4; b.style.width=w+'%'; if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }}, 40);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
