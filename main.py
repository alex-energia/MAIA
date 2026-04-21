# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)
app.secret_key = "maia_v13_vibrant"

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
            if item and item not in session['saved']: session['saved'].append(item)
        elif action == 'clear_all':
            session['history'] = []; session['saved'] = []
        elif action == 'hacer_modelo':
            session['calc'] = builder_engine.calculate_indicators(request.form)
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html><head>
        <title>MAIA II - V.13</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; --red: #ff3131; --yellow: #ffff31; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:20px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; margin-bottom:20px; }
            .btn { padding:10px; border:1px solid var(--neon); background:none; color:var(--neon); cursor:pointer; font-weight:bold; }
            .btn-active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            /* Colores de Riesgo Vivos */
            .ALTO { background:var(--red); color:#000; padding:5px 10px; }
            .MODERADO { background:var(--yellow); color:#000; padding:5px 10px; }
            .BAJO { background:var(--green); color:#000; padding:5px 10px; }
            
            .ficha { background:#0a0a0a; border:1px solid #333; padding:20px; margin-bottom:20px; border-left:5px solid var(--neon); }
            .grid { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin:15px 0; }
            .label { color:var(--pink); font-size:10px; display:block; }
            .value { color:#fff; font-size:13px; }
            
            input, select { width:100%; padding:10px; background:#111; border:1px solid var(--neon); color:#fff; }
            .card-fin { background:#111; padding:15px; border:1px solid var(--green); text-align:center; }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <input type="hidden" name="view_state" value="scout">
                <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'scout' }}">SCOUT GLOBAL</button>
                <input type="hidden" name="view_state" value="memoria">
                <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <input type="hidden" name="view_state" value="builder">
                <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'builder' }}">CONSTRUCTOR FINANCIERO</button>
                <button type="submit" name="action" value="clear_all" class="btn" style="border-color:red; color:red;">LIMPIAR TODO</button>
            </form>
        </div>

        {% if view == 'scout' %}
        <form method="POST"><button type="submit" name="action" value="run_global" class="btn" style="width:100%; border-color:var(--green);">INICIAR RASTREO 2026</button></form>
        {% for r in session['history'] %}
            <div class="ficha">
                <div style="display:flex; justify-content:space-between;">
                    <strong>{{ r.nombre }}</strong>
                    <span class="{{ r.riesgo }}">RIESGO {{ r.riesgo }}</span>
                </div>
                <div class="grid">
                    <div><span class="label">UBICACIÓN</span><span class="value">{{ r.ubicacion }}</span></div>
                    <div><span class="label">CAPACIDAD</span><span class="value">{{ r.capacidad }}</span></div>
                    <div><span class="label">ID</span><span class="value">{{ r.id }}</span></div>
                </div>
                <p style="color:#ccc; font-size:12px; border-top:1px solid #222; padding-top:10px;">{{ r.resumen }}</p>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[VER FUENTE]</a>
                    <form method="POST"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save_memoria" class="btn" style="font-size:10px;">+ MEMORIA</button></form>
                </div>
            </div>
        {% endfor %}

        {% elif view == 'memoria' %}
        <h2 style="color:var(--pink);">FICHAS GUARDADAS EN MEMORIA</h2>
        {% for r in session['saved'] %}<div class="ficha"><strong>{{ r.nombre }}</strong> ({{ r.id }})</div>{% endfor %}

        {% elif view == 'builder' %}
        <div class="ficha">
            <h2 style="color:var(--pink);">CREAR NUEVO PROYECTO</h2>
            <form method="POST">
                <div class="grid">
                    <div><label class="label">CAPEX (COP)</label><input type="text" name="capex" placeholder="Ej: 90000000000"></div>
                    <div><label class="label">CAPACIDAD (MW)</label><input type="number" step="0.01" name="capacidad"></div>
                    <div><label class="label">PPA (COP/kWh)</label><input type="number" name="ppa"></div>
                </div>
                <button type="submit" name="action" value="hacer_modelo" class="btn" style="width:100%; background:var(--green); color:#000;">HACER EL MODELO</button>
            </form>
        </div>
        
        {% if session.get('calc') %}
        <div class="grid">
            <div class="card-fin"><span class="label">VPN</span><div style="font-size:18px;">{{ session['calc'].vpn }}</div></div>
            <div class="card-fin"><span class="label">TIR</span><div style="font-size:18px;">{{ session['calc'].tir }}</div></div>
            <div class="card-fin"><span class="label">PAYBACK</span><div style="font-size:18px;">{{ session['calc'].payback }}</div></div>
        </div>
        <canvas id="myChart" style="background:#111; margin-top:20px;"></canvas>
        <script>
            new Chart(document.getElementById('myChart'), {
                type: 'line',
                data: { labels: ['Añ1', 'Añ2', 'Añ3', 'Añ4'], datasets: [{ label: 'Ingresos Proyectados', data: {{ session['calc'].data_grafica }}, borderColor: '#0f0' }] }
            });
        </script>
        {% endif %}
        {% endif %}
    </body></html>
    """
    return render_template_string(html, view=view)
