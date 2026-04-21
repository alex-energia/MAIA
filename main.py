# -*- coding: utf-8 -*-
# MAIA II - DASHBOARD V.11
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_v11_independent"

# Datos del modelo Morrosquillo I para el Constructor
MORROSQUILLO_DATA = {
    "capacidad": 23.42,
    "capex": 90389977843,
    "ppa": 323,
    "kd": 0.1164,
    "periodos": 25
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    
    # Manejo de vistas independiente
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
            view = 'scout'
        elif action == 'go_builder':
            view = 'builder'
        elif action == 'go_scout':
            view = 'scout'

    summary = scout_engine.generate_summary(session['history']) if session['history'] else None

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA II - V.11 INDEPENDIENTE</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:30px; }
            .nav { display:flex; gap:15px; border-bottom:2px solid var(--pink); padding-bottom:15px; margin-bottom:25px; }
            .btn-nav { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .btn-nav.active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            .btn-action { background:var(--green); color:#000; border:none; padding:15px; width:100%; cursor:pointer; font-weight:bold; text-transform:uppercase; }
            
            /* Barra de Progreso */
            #p-container { width:100%; height:10px; background:#111; border:1px solid var(--neon); margin-bottom:20px; display:none; }
            #p-bar { height:100%; background:var(--green); width:0%; transition: 0.4s; }

            .ficha { background:#0a0a0a; border:1px solid #333; padding:20px; margin-bottom:20px; }
            .grid { display:grid; grid-template-columns: 1fr 1fr; gap:20px; }
            .label { color:var(--pink); font-size:11px; display:block; }
            .value { color:#fff; display:block; margin-bottom:10px; font-size:14px; }

            /* Constructor Form */
            .form-group { margin-bottom:15px; }
            input, select { width:100%; padding:10px; background:#111; border:1px solid var(--neon); color:#fff; font-family:monospace; }

            .summary-table { width:100%; border:2px solid var(--pink); border-collapse:collapse; margin-top:30px; background:rgba(255,0,255,0.05); }
            .summary-table td { border:1px solid #333; padding:15px; }

            #maia-chat { position:fixed; bottom:0; right:20px; width:320px; border:2px solid var(--pink); background:#000; }
            .chat-head { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; }
            .chat-body { height:200px; padding:10px; display:none; overflow-y:auto; border-top:1px solid var(--pink); font-size:12px; }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <input type="hidden" name="view_state" value="scout">
                <button type="submit" name="action" value="go_scout" class="btn-nav {{ 'active' if view == 'scout' }}">SCOUT GLOBAL</button>
                <input type="hidden" name="view_state" value="builder">
                <button type="submit" name="action" value="go_builder" class="btn-nav {{ 'active' if view == 'builder' }}">CONSTRUCTOR</button>
            </form>
        </div>

        <div id="p-container"><div id="p-bar"></div></div>

        {% if view == 'scout' %}
        <div id="scout-section">
            <form method="POST" onsubmit="startAnim()">
                <input type="hidden" name="view_state" value="scout">
                <button type="submit" name="action" value="run_global" class="btn-action">EJECUTAR RASTREO GLOBAL 2026</button>
            </form>

            <div style="margin-top:30px;">
                {% for r in session['history'] %}
                <div class="ficha">
                    <div class="grid">
                        <div>
                            <span class="label">ID PROYECTO</span><span class="value">{{ r.id }}</span>
                            <span class="label">NOMBRE</span><span class="value">{{ r.Nombre }}</span>
                            <span class="label">CAPACIDAD</span><span class="value">{{ r.Capacidad }}</span>
                        </div>
                        <div>
                            <span class="label">CEO / DIRECTOR</span><span class="value">{{ r.CEO }}</span>
                            <span class="label">CONTACTO / MÓVIL</span><span class="value">{{ r.Contacto }}</span>
                            <span class="label">DIRECCIÓN CORPORATIVA</span><span class="value">{{ r.Direccion }}</span>
                        </div>
                    </div>
                    <div style="border-top:1px solid #222; margin-top:15px; padding-top:15px;">
                        <span class="label">RESUMEN TÉCNICO Y EJECUTIVO</span>
                        <p style="color:#ccc; font-size:13px; line-height:1.6;">{{ r.Resumen }}</p>
                        <a href="{{ r.URL }}" target="_blank" style="color:var(--neon);">[VER FUENTE ORIGINAL]</a>
                        <p style="text-align:right; font-size:10px; color:#444;">RASTREO: {{ r.Fecha }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>

            {% if summary %}
            <table class="summary-table">
                <tr><td colspan="2" style="background:var(--pink); color:#000; font-weight:bold;">RESUMEN FINAL DE BÚSQUEDA</td></tr>
                {% for k, v in summary.items() %}
                <tr><td>{{ k }}</td><td style="color:var(--green);">{{ v }}</td></tr>
                {% endfor %}
            </table>
            {% endif %}
        </div>
        {% else %}
        <div id="builder-section" style="background:#0a0a0a; padding:30px; border:1px solid var(--neon);">
            <h2 style="color:var(--pink);">MODELADOR FINANCIERO DINÁMICO</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Tipo de Tecnología</label>
                    <select name="tech" id="tech-select" onchange="adjustForm(this.value)">
                        <option value="solar">Solar (Basado en Morrosquillo I)</option>
                        <option value="wind">Eólica</option>
                        <option value="hydrogen">Hidrógeno Verde</option>
                        <option value="smr">SMR Nuclear / Neutrino</option>
                        <option value="biomass">Biomasa</option>
                    </select>
                </div>
                <div id="dynamic-fields" class="grid">
                    <div class="form-group"><label>Capacidad Instalada (MWp)</label><input type="number" step="0.01" value="23.42"></div>
                    <div class="form-group"><label>CAPEX Total (COP)</label><input type="text" value="90.389.977.843"></div>
                    <div class="form-group"><label>Precio PPA (kWh Año 1)</label><input type="number" value="323"></div>
                    <div class="form-group"><label>Tasa Kd (Crédito)</label><input type="text" value="0.1164"></div>
                    <div class="form-group"><label>Horizonte (Años)</label><input type="number" value="25"></div>
                </div>
                <button type="button" class="btn-action" style="margin-top:20px;" onclick="alert('Generando Modelo Financiero...')">HACER EL MODELO</button>
            </form>
        </div>
        {% endif %}

        <div id="maia-chat">
            <div class="chat-head" onclick="toggleChat()">MAIA AGENT</div>
            <div class="chat-body" id="c-body">
                <p>> Frentes Independientes Activos.</p>
                <p>> Scout Global: Protocolo de datos de contacto ON.</p>
                <p>> Constructor: Cargado modelo Morrosquillo I.</p>
            </div>
        </div>

        <script>
            function toggleChat() {
                var b = document.getElementById('c-body');
                b.style.display = (b.style.display == 'block') ? 'none' : 'block';
            }
            function startAnim() {
                document.getElementById('p-container').style.display = 'block';
                var bar = document.getElementById('p-bar');
                var w = 0;
                var i = setInterval(function(){
                    w += 10; bar.style.width = w + '%';
                    if(w>=100) clearInterval(i);
                }, 200);
            }
            function adjustForm(val) {
                const fields = document.getElementById('dynamic-fields');
                if(val === 'hydrogen') {
                    fields.innerHTML = '<div class="form-group"><label>Kg H2/Día</label><input type="number"></div><div class="form-group"><label>Costo Electrolizador</label><input type="text"></div>';
                } else if(val === 'solar') {
                    fields.innerHTML = '<div class="form-group"><label>MWp</label><input type="number" value="23.42"></div><div class="form-group"><label>CAPEX (COP)</label><input type="text" value="90.389.977.843"></div>';
                }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
