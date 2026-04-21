# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)
app.secret_key = "maia_fixed_v14"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
        elif action == 'save_memoria':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item: session['saved'].append(item)
        elif action == 'hacer_modelo':
            session['calc'] = builder_engine.run_model(request.form)
            view = 'builder'
        elif action == 'clear':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html><head>
        <title>MAIA II - V.14 FIXED</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; --red: #ff003c; --yellow: #ffea00; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:20px; }
            .nav { position:sticky; top:0; background:#000; padding:10px; border-bottom:2px solid var(--pink); display:flex; gap:10px; z-index:100; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px; cursor:pointer; }
            .btn-active { background:var(--pink); color:#000; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-bottom:20px; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin:15px 0; }
            .ALTO { color:var(--red); border:1px solid var(--red); padding:5px; }
            .MODERADO { color:var(--yellow); border:1px solid var(--yellow); padding:5px; }
            .BAJO { color:var(--green); border:1px solid var(--green); padding:5px; }
            #maia-chat { position:fixed; bottom:20px; right:20px; width:300px; border:2px solid var(--pink); background:#000; z-index:1000; }
            .chat-head { background:var(--pink); color:#000; padding:10px; font-weight:bold; cursor:pointer; }
            #progress { width:100%; height:5px; background:#111; display:none; }
            #bar { height:100%; background:var(--green); width:0%; transition:0.3s; }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <input type="hidden" name="view_state" value="scout">
                <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'scout' }}">SCOUT GLOBAL</button>
                <input type="hidden" name="view_state" value="memoria">
                <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <input type="hidden" name="view_state" value="builder">
                <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'builder' }}">CONSTRUCTOR</button>
            </form>
        </div>

        <div id="progress"><div id="bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" onsubmit="load()">
                <input type="hidden" name="view_state" value="scout">
                <button type="submit" name="action" value="run_global" class="btn" style="width:100%; color:var(--green);">INICIAR RASTREO REAL 2026</button>
            </form>
            {% for r in session['history'] %}
            <div class="ficha">
                <div style="display:flex; justify-content:space-between;">
                    <h3>{{ r.nombre }}</h3><span class="{{ r.riesgo }}">{{ r.riesgo }}</span>
                </div>
                <div class="grid">
                    <div><small>ID</small><br>{{ r.id }}</div>
                    <div><small>CEO</small><br>{{ r.ceo }}</div>
                    <div><small>MOVIL</small><br>{{ r.movil }}</div>
                </div>
                <p>{{ r.resumen }}</p>
                <div style="display:flex; justify-content:space-between;">
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">FUENTE</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save_memoria" class="btn">MEMORIA</button></form>
                </div>
            </div>
            {% endfor %}

        {% elif view == 'builder' %}
            <div class="ficha">
                <h2 style="color:var(--pink);">CONSTRUCTOR FINANCIERO</h2>
                <form method="POST">
                    <div class="grid">
                        <input type="text" name="capex" placeholder="CAPEX (COP)">
                        <input type="number" name="capacidad" placeholder="MW">
                        <input type="number" name="ppa" placeholder="PPA (COP)">
                    </div>
                    <button type="submit" name="action" value="hacer_modelo" class="btn" style="width:100%; background:var(--green); color:#000;">HACER EL MODELO</button>
                </form>
            </div>
            {% if session.get('calc') %}
                <div class="grid">
                    <div class="ficha">VPN: {{ session['calc'].vpn }}</div>
                    <div class="ficha">TIR: {{ session['calc'].tir }}</div>
                    <div class="ficha">MONTECARLO: {{ session['calc'].montecarlo_avg }}</div>
                </div>
                <div class="ficha"><canvas id="c"></canvas></div>
                <script>
                    new Chart(document.getElementById('c'), { type:'line', data:{ labels:[1,2,3,4,5], datasets:[{label:'Flujo', data:{{ session['calc'].chart_data }}, borderColor:'#0f0'}] } });
                </script>
            {% endif %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-head" onclick="document.getElementById('cb').style.display = 'block'">MAIA INTELLIGENCE</div>
            <div id="cb" class="chat-body" style="display:block; height:150px; padding:10px; font-size:12px; color:var(--green);">
                > Sistema V.14 Online.<br>> Montecarlo Activado.<br>> Scout Real Conectado.
            </div>
        </div>

        <script>
            function load(){ document.getElementById('progress').style.display='block'; var b=document.getElementById('bar'); var w=0; setInterval(function(){ w+=5; b.style.width=w+'%'; }, 100); }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view)