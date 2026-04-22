# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_level_94_ultra_deep"

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
        <title>MAIA - NIVEL 94 (INFILTRACIÓN)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --pure-white: #ffffff; }
            body { background:#000; color:var(--pure-white); font-family:monospace; margin:0; padding:20px; padding-bottom:180px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid #111; padding-bottom:15px; }
            .btn { background:none; border:1px solid #333; color:#555; padding:10px 20px; cursor:pointer; font-weight:bold; text-transform:uppercase; transition:0.3s; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active { background:var(--neon); color:#000; border-color:var(--neon); box-shadow: 0 0 20px rgba(0,255,255,0.4); }
            
            #st-cont { width:100%; height:4px; background:#111; margin:15px 0; display:none; }
            #st-bar { height:100%; background:var(--neon); width:0%; transition:0.05s; }

            .alert-null { border: 1px solid #222; color: #444; padding: 60px; text-align: center; margin-top: 20px; text-transform:uppercase; letter-spacing:3px; }
            .ficha { background:#050505; border:1px solid #111; padding:35px; margin-top:20px; border-left:2px solid var(--neon); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin:20px 0; border-bottom:1px solid #111; padding-bottom:20px; }
            .label { color:var(--neon); font-size:10px; display:block; margin-bottom:5px; font-weight:bold; }
            
            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid #222; background:#000; z-index:10000; }
            .chat-h { background:#111; color:#555; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { display:none; height:280px; padding:15px; overflow-y:auto; font-size:12px; color:var(--neon); }
            #cInput { display:none; width:100%; background:#000; border:none; border-top:1px solid #111; color:var(--neon); padding:15px; box-sizing: border-box; outline:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">SCANNER 94</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">ACTIVOS ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto;">RESET</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; height:80px; font-size:18px; border-color:var(--neon); color:var(--neon);">INICIAR INFILTRACIÓN DE SEÑALES DE CAPITAL</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="alert-null">
                    <p>[ ESCANEO PROFUNDO COMPLETADO ]</p>
                    <p style="font-size:10px;">0 COINCIDENCIAS EN LA CAPA DE FACTIBILIDAD Y CAPITAL SEMILLA.</p>
                </div>
            {% endif %}
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff; letter-spacing:1px;">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID SEÑAL</span>{{ r.id }}</div>
                    <div><span class="label">ENTIDAD DETECTADA</span>{{ r.ceo }}</div>
                    <div><span class="label">TIPO DE SEÑAL</span>{{ r.riesgo }}</div>
                    <div><span class="label">FUENTES</span>{{ r.movil }}</div>
                    <div><span class="label">INTEL E-MAIL</span>{{ r.email }}</div>
                    <div><span class="label">FECHA</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#000; padding:20px; border:1px solid #111;">
                    <span class="label">ANÁLISIS DE LA OPORTUNIDAD</span>
                    <p style="color:#888; font-size:12px; line-height:1.6;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--neon); text-decoration:none; font-weight:bold; font-size:11px;">[ACCEDER A LA FUENTE DE SEÑAL]</a>
                </div>
                <form method="POST" style="margin-top:20px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:10px; border-color:var(--neon); color:var(--neon);">GURDAR ACTIVO</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA DEEP CMD</span><span id="ico">[+]</span></div>
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
                if(inp.value.trim()!="") { box.innerHTML += "<div style='margin-bottom:10px; border-left:1px solid var(--neon); padding-left:10px;'>"+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ w+=10; b.style.width=w+'%'; if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }}, 30);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)