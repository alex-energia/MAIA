# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_level_84_precision"

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
        <title>MAIA - NIVEL 84 (PRECISION)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --white: #ffffff; }
            body { background:#000; color:var(--white); font-family:monospace; margin:0; padding:20px; padding-bottom:180px; }
            .nav { display:flex; gap:10px; border-bottom:1px solid #333; padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--gold); color:var(--gold); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--gold); color:#000; box-shadow: 0 0 15px var(--gold); }
            
            #st-cont { width:100%; height:8px; background:#111; margin:15px 0; display:none; }
            #st-bar { height:100%; background:var(--gold); width:0%; transition:0.1s; }

            .alert-null { border: 2px solid var(--gold); background: rgba(255, 215, 0, 0.05); color: var(--gold); padding: 50px; text-align: center; margin-top: 20px; font-size:18px; }
            .ficha { background:#0a0a0a; border:1px solid #222; padding:30px; margin-top:20px; border-top:4px solid var(--gold); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin:20px 0; }
            .label { color:var(--gold); font-size:11px; display:block; opacity:0.7; }
            
            /* CHAT - CERRADO POR DEFECTO */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid var(--gold); background:#000; z-index:10000; }
            .chat-h { background:var(--gold); color:#000; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { display:none; height:280px; padding:15px; overflow-y:auto; font-size:12px; color:var(--neon); }
            #cInput { display:none; width:100%; background:#111; border:none; border-top:1px solid var(--gold); color:var(--neon); padding:15px; box-sizing: border-box; outline:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">RADAR DE ACTIVOS V84</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">PORTAFOLIO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">RESET</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; height:60px; font-size:16px;">SINCRONIZAR REGISTROS DE FACTIBILIDAD AMÉRICA / EUROPA</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="alert-null">
                    <p>[ ANALIZANDO REGISTROS GUBERNAMENTALES... ]</p>
                    <p style="font-size:12px;">No se han detectado movimientos de capital o activos en venta en los homólogos de la UPME este mes.</p>
                </div>
            {% endif %}
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:var(--gold);">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID PROYECTO</span>{{ r.id }}</div>
                    <div><span class="label">PROMOTOR</span>{{ r.ceo }}</div>
                    <div><span class="label">FASE DE REGISTRO</span>{{ r.riesgo }}</div>
                    <div><span class="label">FUENTE DE DATOS</span>{{ r.movil }}</div>
                    <div><span class="label">E-MAIL</span>{{ r.email }}</div>
                    <div><span class="label">VIGENCIA</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:20px; border:1px solid #222;">
                    <span class="label">DETALLE DEL PROYECTO</span>
                    <p style="color:#ccc; font-size:13px;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--gold); text-decoration:none; font-weight:bold;">[ABRIR REGISTRO OFICIAL]</a>
                </div>
                <form method="POST" style="margin-top:15px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:11px;">MIGRAR A PORTAFOLIO</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA PRECISION COMMAND</span><span id="ico">[+]</span></div>
            <div id="chat-b"></div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()">
        </div>

        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div style='margin-bottom:8px; border-left:1px solid var(--gold); padding-left:10px;'>"+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ w+=5; b.style.width=w+'%'; if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }}, 50);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)