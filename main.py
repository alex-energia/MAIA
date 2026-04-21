# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine

app = Flask(__name__)
app.secret_key = "maia_platinum_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.execute_global_scout()
            view = 'scout'
        elif action == 'save_memoria':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item: session['saved'].append(item)
            view = 'scout'
        elif action == 'run_builder':
            session['calc'] = builder_engine.calcular_modelo_pro(request.form)
            view = 'builder'
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA II - PLATINUM 2026</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; }
            .nav { display:flex; gap:15px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; text-transform:uppercase; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            #progress { width:100%; height:5px; background:#111; margin:10px 0; display:none; }
            #bar { height:100%; background:var(--green); width:0%; transition:0.3s; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:4px solid var(--neon); }
            .grid-data { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin:15px 0; font-size:12px; }
            label { color:var(--pink); font-size:9px; display:block; }
            #maia-chat { position:fixed; bottom:0; right:20px; width:320px; border:2px solid var(--pink); background:#000; z-index:1000; }
            .chat-h { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; }
            #chat-b { height:180px; padding:15px; overflow-y:auto; font-size:11px; color:var(--green); }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">Scout Negocios</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">Memoria ({{ session['saved']|length }})</button>
                <button type="submit" name="view_state" value="builder" class="btn {{ 'active' if view == 'builder' }}">Constructor</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">Limpiar</button>
            </form>
        </div>

        <div id="progress"><div id="bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" onsubmit="load()"><button type="submit" name="action" value="run_scout" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green);">EJECUTAR BÚSQUEDA REAL 2026</button></form>
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid-data">
                    <div><label>ID PROYECTO</label>{{ r.id }}</div>
                    <div><label>CEO/RESPONSABLE</label>{{ r.ceo }}</div>
                    <div><label>ESTADO</label>{{ r.estado }}</div>
                    <div><label>FECHA DETECCIÓN</label>{{ r.fecha_deteccion }}</div>
                    <div><label>CONTACTO</label>{{ r.email }}</div>
                    <div><label>FUENTE</label><a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">Link Oficial</a></div>
                </div>
                <div style="background:#111; padding:15px; border-top:1px solid var(--pink);">
                    <label>RESUMEN DE NEGOCIO PROFUNDO</label>
                    <p style="font-size:13px; color:#ccc;">{{ r.resumen_profundo }}</p>
                </div>
                <form method="POST" style="margin-top:15px;"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save_memoria" class="btn" style="font-size:10px;">GUARDAR EN MEMORIA</button></form>
            </div>
            {% endfor %}

        {% elif view == 'builder' %}
            <div class="ficha">
                <h2 style="color:var(--pink); margin:0 0 20px 0;">CONSTRUCTOR FINANCIERO P50</h2>
                <form method="POST">
                    <div class="grid-data">
                        <input type="text" name="capex" value="90389977843" style="background:#111; color:#fff; border:1px solid var(--neon); padding:10px;">
                        <input type="number" step="0.01" name="capacidad" value="23.42" style="background:#111; color:#fff; border:1px solid var(--neon); padding:10px;">
                        <input type="number" name="ppa" value="323" style="background:#111; color:#fff; border:1px solid var(--neon); padding:10px;">
                    </div>
                    <button type="submit" name="action" value="run_builder" class="btn" style="width:100%; background:var(--green); color:#000;">CALCULAR PROYECCIÓN</button>
                </form>
            </div>
            {% if session.get('calc') %}
            <div class="grid-data" style="margin-top:20px;">
                <div class="ficha">VPN: {{ session['calc'].vpn }}</div>
                <div class="ficha">FCL: {{ session['calc'].fcl }}</div>
                <div class="ficha">ÉXITO: {{ session['calc'].probabilidad }}</div>
            </div>
            {% endif %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()">MAIA II PLATINUM [-]</div>
            <div id="chat-b">
                > Sistema V.21 Online.<br>> Búsqueda forzada a fuentes oficiales.<br>> Modelo financiero con tax/depreciación.<br>> Listo para el siguiente nivel.
            </div>
        </div>

        <script>
            function toggle(){ var b=document.getElementById('chat-b'); b.style.display=(b.style.display=='none')?'block':'none'; }
            function load(){ document.getElementById('progress').style.display='block'; var b=document.getElementById('bar'); var w=0; setInterval(function(){ w+=5; if(w<=100) b.style.width=w+'%'; }, 100); }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)