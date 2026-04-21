# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_v12_full"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
        elif action == 'calc_model':
            # Procesa el formulario
            session['calc_res'] = builder_engine.process_financials(request.form)
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html><head>
        <title>MAIA II - V.12 CONTROL TOTAL</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:20px; }
            .nav { border-bottom: 2px solid var(--pink); padding-bottom:15px; margin-bottom:25px; display:flex; gap:10px; }
            .btn { padding:10px 20px; background:none; border:1px solid var(--neon); color:var(--neon); cursor:pointer; font-weight:bold; }
            .btn-active { background:var(--pink); color:#000; border-color:var(--pink); }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:20px; margin-bottom:20px; }
            .label { color:var(--pink); font-size:10px; text-transform:uppercase; }
            .value { color:#fff; display:block; margin-bottom:10px; }
            .risk-badge { padding:3px 8px; font-weight:bold; border:1px solid; }
            .ALTO { border-color:red; color:red; } .MODERADO { border-color:yellow; color:yellow; } .BAJO { border-color:green; color:green; }
            
            /* Formulario Vacío */
            .field-group { margin-bottom:15px; }
            input, select { width:100%; padding:10px; background:#111; border:1px solid var(--neon); color:#fff; }
            
            #loader { width:100%; height:6px; background:#111; display:none; margin-bottom:20px; }
            #bar { height:100%; background:var(--green); width:0%; transition:0.4s; }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <input type="hidden" name="view_state" value="scout">
                <button type="submit" name="action" value="go" class="btn {{ 'btn-active' if view == 'scout' }}">SCOUT GLOBAL</button>
                <input type="hidden" name="view_state" value="builder">
                <button type="submit" name="action" value="go" class="btn {{ 'btn-active' if view == 'builder' }}">CONSTRUCTOR</button>
            </form>
        </div>

        <div id="loader"><div id="bar"></div></div>

        {% if view == 'scout' %}
        <form method="POST" onsubmit="start()">
            <input type="hidden" name="view_state" value="scout">
            <button type="submit" name="action" value="run_global" class="btn" style="width:100%; border-color:var(--green); color:var(--green);">EJECUTAR BÚSQUEDA PROFUNDA 2026</button>
        </form>
        <div style="margin-top:30px;">
            {% for r in session['history'] %}
            <div class="ficha">
                <div style="display:flex; justify-content:space-between;">
                    <span class="label">ID: {{ r.id }}</span>
                    <span class="risk-badge {{ r.Riesgo }}">RIESGO: {{ r.Riesgo }}</span>
                </div>
                <h3 style="color:#fff;">{{ r.Nombre }}</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                    <div>
                        <span class="label">Ubicación del Proyecto</span><span class="value">{{ r.Ubicacion }}</span>
                        <span class="label">Capacidad Estimada</span><span class="value">{{ r.Capacidad }}</span>
                    </div>
                    <div>
                        <span class="label">CEO / Líder</span><span class="value">{{ r.CEO }}</span>
                        <span class="label">Contacto Directo</span><span class="value">{{ r.Contacto }}</span>
                    </div>
                </div>
                <div style="border-top:1px solid #222; padding-top:15px; margin-top:15px;">
                    <span class="label">Resumen Ejecutivo</span>
                    <p style="color:#ccc; font-size:13px;">{{ r.Resumen }}</p>
                    <span class="label">Fuente de Información</span><br>
                    <a href="{{ r.Fuente }}" target="_blank" style="color:var(--pink); font-size:11px;">{{ r.Fuente }}</a>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="ficha">
            <h2 style="color:var(--pink);">NUEVO MODELO FINANCIERO (DILIGENCIAR DATOS)</h2>
            <form method="POST">
                <div class="field-group">
                    <label>Tecnología</label>
                    <select name="tech">
                        <option value="solar">Solar Fotovoltaica</option>
                        <option value="wind">Eólica</option>
                        <option value="hydrogen">Hidrógeno Verde</option>
                    </select>
                </div>
                <div class="field-group"><label>Nombre del Proyecto</label><input type="text" name="p_name" placeholder="..."></div>
                <div class="field-group"><label>Capacidad (MW)</label><input type="number" step="0.01" name="capacidad"></div>
                <div class="field-group"><label>CAPEX Total (COP)</label><input type="text" name="capex"></div>
                <div class="field-group"><label>Valor PPA (COP/kWh)</label><input type="number" name="ppa"></div>
                <button type="submit" name="action" value="calc_model" class="btn" style="width:100%; background:var(--green); color:#000;">HACER EL MODELO</button>
            </form>
        </div>
        {% endif %}

        <script>
            function start() {
                document.getElementById('loader').style.display = 'block';
                var b = document.getElementById('bar'); var w = 0;
                var i = setInterval(function(){ w+=10; b.style.width=w+'%'; if(w>=100) clearInterval(i); }, 200);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
