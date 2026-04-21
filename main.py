# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_industrial_v34"

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
        <title>MAIA - NIVEL 34 (INDUSTRIAL)</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; padding-bottom:180px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            #st-cont { width:100%; height:12px; background:#111; margin:15px 0; display:none; border:1px solid #333; }
            #st-bar { height:100%; background:var(--green); width:0%; transition:0.3s; }
            .alert-null { border: 3px solid red; background: rgba(255,0,0,0.1); color: #fff; padding: 40px; text-align: center; margin-top: 20px; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--green); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin:15px 0; }
            .label { color:var(--pink); font-size:10px; display:block; }
            #maia-chat { position:fixed; bottom:20px; right:20px; width:380px; border:2px solid var(--pink); background:#000; z-index:10000; }
            .chat-h { background:var(--pink); color:#000; padding:10px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { display:block; height:250px; padding:15px; overflow-y:auto; font-size:12px; color:var(--green); }
            .chat-input { width:100%; background:#111; border:none; border-top:2px solid var(--pink); color:var(--green); padding:15px; box-sizing: border-box; font-family:monospace; outline:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">SCOUT NIVEL 34</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">LIMPIAR SISTEMA</button>
            </form>
        </div>
        <div id="st-cont"><div id="st-bar"></div></div>
        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green); height:60px;">SINCRONIZAR ACTIVOS INDUSTRIALES DISPONIBLES</button>
            </form>
            {% if session['attempt'] and not session['history'] %}
                <div class="alert-null">
                    <h2 style="color:red;">[ ERROR DE FILTRADO RESUELTO ]</h2>
                    <p>MAIA HA EXCLUIDO CONTENIDO CULTURAL. NO SE HAN DETECTADO ACTIVOS DE INVERSIÓN REALES EN LAS ÚLTIMAS 24 HORAS PARA ESTA MATRIZ.</p>
                </div>
            {% endif %}
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID ACTIVO</span>{{ r.id }}</div>
                    <div><span class="label">PUNTO DE CONTACTO</span>{{ r.ceo }}</div>
                    <div><span class="label">EVALUACIÓN</span>{{ r.riesgo }}</div>
                    <div><span class="label">TELÉFONO</span>{{ r.movil }}</div>
                    <div><span class="label">EMAIL</span>{{ r.email }}</div>
                    <div><span class="label">VIGENCIA</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:15px; border:1px solid #222; margin-top:10px;">
                    <span class="label">DETALLE DEL NEGOCIO</span>
                    <p style="color:#ccc; font-size:12px;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[ABRIR DATA-ROOM]</a>
                </div>
                <form method="POST" style="margin-top:10px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:10px;">GURDAR</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}
        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA CORE V34</span><span id="ico">[-]</span></div>
            <div id="chat-b"></div>
            <input type="text" class="chat-input" id="cInput" placeholder="Comando de inteligencia..." onkeydown="if(event.key==='Enter') push()">
        </div>
        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput');
                if(b.style.display=='none'){ b.style.display='block'; i.style.display='block'; }
                else { b.style.display='none'; i.style.display='none'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div>> "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ w+=5; b.style.width=w+'%'; if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }}, 100);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
