# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_v15_final"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
            session.modified = True
            view = 'scout'
        
        elif action == 'hacer_modelo':
            session['calc'] = builder_engine.calcular_modelo_completo(request.form)
            session.modified = True
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA II - V.15 PRO</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; --bg: #000; }
            body { background: var(--bg); color: var(--neon); font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
            
            /* Nav Blindada */
            .nav-bar { display: flex; gap: 10px; border-bottom: 2px solid var(--pink); padding-bottom: 15px; margin-bottom: 20px; }
            .btn-nav { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 10px 20px; cursor: pointer; font-weight: bold; }
            .btn-nav.active { background: var(--pink); color: #000; border-color: var(--pink); }

            /* Fichas y Contenedores */
            .panel { background: #0a0a0a; border: 1px solid #333; padding: 20px; margin-bottom: 20px; }
            .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
            .label { color: var(--pink); font-size: 10px; text-transform: uppercase; }
            
            /* Chat Colapsable */
            #maia-chat { position: fixed; bottom: 0; right: 20px; width: 320px; border: 2px solid var(--pink); background: #000; z-index: 9999; }
            .chat-header { background: var(--pink); color: #000; padding: 10px; font-weight: bold; cursor: pointer; display: flex; justify-content: space-between; }
            #chat-content { height: 250px; padding: 15px; overflow-y: auto; display: block; font-size: 12px; color: var(--green); border-top: 1px solid var(--pink); }

            /* Progress Bar */
            #loader { width: 100%; height: 6px; background: #111; margin-bottom: 20px; display: none; }
            #bar { height: 100%; background: var(--green); width: 0%; transition: 0.3s; }
            
            input { width: 100%; padding: 10px; background: #111; border: 1px solid var(--neon); color: #fff; box-sizing: border-box; }
        </style>
    </head>
    <body>

    <div class="nav-bar">
        <form method="POST" style="display:contents;">
            <input type="hidden" name="view_state" value="scout">
            <button type="submit" name="action" value="nav" class="btn-nav {{ 'active' if view == 'scout' }}">1. SCOUT REAL</button>
            <input type="hidden" name="view_state" value="builder">
            <button type="submit" name="action" value="nav" class="btn-nav {{ 'active' if view == 'builder' }}">2. CONSTRUCTOR PRO</button>
        </form>
    </div>

    <div id="loader"><div id="bar"></div></div>

    {% if view == 'scout' %}
        <form method="POST" onsubmit="startScan()">
            <input type="hidden" name="view_state" value="scout">
            <button type="submit" name="action" value="run_global" class="btn-nav" style="width:100%; background:var(--green); color:#000;">EJECUTAR BÚSQUEDA 100% REAL 2026</button>
        </form>
        <div style="margin-top:20px;">
            {% for r in session['history'] %}
            <div class="panel">
                <div style="display:flex; justify-content:space-between;">
                    <h3 style="margin:0;">{{ r.nombre }}</h3>
                    <span style="border:1px solid; padding:5px; font-size:10px;">RIESGO: {{ r.riesgo }}</span>
                </div>
                <div class="grid-3" style="margin-top:15px;">
                    <div><span class="label">Contacto CEO</span><br>{{ r.ceo }}</div>
                    <div><span class="label">Móvil</span><br>{{ r.movil }}</div>
                    <div><span class="label">Email</span><br>{{ r.email }}</div>
                </div>
                <p style="font-size:13px; color:#ccc; border-top:1px solid #222; padding-top:10px;">{{ r.resumen }}</p>
                <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[VER FUENTE ORIGINAL]</a>
            </div>
            {% endfor %}
        </div>

    {% elif view == 'builder' %}
        <div class="panel">
            <h2 style="color:var(--pink);">CONFIGURACIÓN DE PROYECTO MAESTRO</h2>
            <form method="POST">
                <div class="grid-3">
                    <div><label class="label">CAPEX INICIAL (COP)</label><input type="text" name="capex" placeholder="90389977843"></div>
                    <div><label class="label">CAPACIDAD (MWp)</label><input type="number" step="0.01" name="capacidad" placeholder="23.42"></div>
                    <div><label class="label">PPA (COP/kWh)</label><input type="number" name="ppa" placeholder="323"></div>
                </div>
                <button type="submit" name="action" value="hacer_modelo" class="btn-nav" style="width:100%; margin-top:20px; background:var(--green); color:#000;">CALCULAR MODELO FINANCIERO COMPLETO</button>
            </form>
        </div>

        {% if session.get('calc') %}
            <div class="grid-3">
                <div class="panel" style="text-align:center;"><span class="label">VPN ESTIMADO</span><div style="font-size:20px;">{{ session['calc'].indicadores.vpn }}</div></div>
                <div class="panel" style="text-align:center;"><span class="label">TIR PROYECTADA</span><div style="font-size:20px;">{{ session['calc'].indicadores.tir }}</div></div>
                <div class="panel" style="text-align:center;"><span class="label">ÉXITO MONTECARLO</span><div style="font-size:20px; color:var(--green);">{{ session['calc'].indicadores.probabilidad_exito }}</div></div>
            </div>

            <div class="grid-3">
                <div class="panel">
                    <span class="label">DESGLOSE CAPEX</span>
                    {% for k, v in session['calc'].capex_detallado.items() %}
                    <div style="font-size:11px; margin-top:5px;">{{ k }}: <span style="color:#fff;">$ {{ int(v):, }}</span></div>
                    {% endfor %}
                </div>
                <div class="panel">
                    <span class="label">DESGLOSE OPEX ANUAL</span>
                    {% for k, v in session['calc'].opex_detallado.items() %}
                    <div style="font-size:11px; margin-top:5px;">{{ k }}: <span style="color:#fff;">$ {{ int(v):, }}</span></div>
                    {% endfor %}
                </div>
                <div class="panel">
                    <canvas id="chart"></canvas>
                </div>
            </div>
            <script>
                new Chart(document.getElementById('chart'), {
                    type: 'line',
                    data: { labels: [1,2,3,4,5,6,7,8,9,10], datasets: [{ label: 'Flujo Caja Anual', data: {{ session['calc'].flujo_grafica }}, borderColor: '#0f0' }] }
                });
            </script>
        {% endif %}
    {% endif %}

    <div id="maia-chat">
        <div class="chat-header" onclick="toggleChat()">
            <span>MAIA INTELLIGENCE CORE</span>
            <span id="chat-toggle-icon">[-]</span>
        </div>
        <div id="chat-content">
            <p>> Sistema V.15 Estabilizado.</p>
            <p>> Desglose de OPEX/CAPEX inyectado.</p>
            <p>> Montecarlo: 1,000 iteraciones listas.</p>
            <p>> Modo: Avance Significativo.</p>
        </div>
    </div>

    <script>
        function toggleChat() {
            var content = document.getElementById('chat-content');
            var icon = document.getElementById('chat-toggle-icon');
            if (content.style.display === "none") {
                content.style.display = "block";
                icon.innerText = "[-]";
            } else {
                content.style.display = "none";
                icon.innerText = "[+]";
            }
        }
        function startScan() {
            document.getElementById('loader').style.display = 'block';
            var b = document.getElementById('bar');
            var w = 0;
            var i = setInterval(function(){
                w += 2; b.style.width = w + '%';
                if(w >= 100) clearInterval(i);
            }, 50);
        }
    </script>
    </body>
    </html>
    """
    return render_template_string(html, view=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)