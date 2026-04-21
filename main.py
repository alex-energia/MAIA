# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)
app.secret_key = "maia_ultimate_v14_fixed"

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicialización de sesiones
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
            session.modified = True
        
        elif action == 'save_memoria':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item)
                session.modified = True
        
        elif action == 'clear_all':
            session['history'] = []
            session['saved'] = []
            session['calc'] = None
            session.modified = True
            
        elif action == 'hacer_modelo':
            session['calc'] = builder_engine.calculate_full_model(request.form)
            session.modified = True
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA II - SISTEMA INTEGRAL V.14</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; --red: #ff003c; --yellow: #ffea00; }
            body { background:#000; color:var(--neon); font-family:'Courier New', monospace; margin:0; padding:20px; padding-bottom:100px; }
            
            /* Navegación Fija */
            .nav-top { position:sticky; top:0; background:#000; z-index:100; display:flex; gap:10px; border-bottom:2px solid var(--pink); padding:10px 0; margin-bottom:20px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:12px; cursor:pointer; font-weight:bold; font-size:12px; }
            .btn-active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            /* Barra de Progreso */
            #progress-box { width:100%; height:8px; background:#111; border:1px solid var(--neon); margin-bottom:20px; display:none; }
            #progress-bar { height:100%; background:var(--green); width:0%; transition:0.3s; }

            /* Fichas Scout */
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-bottom:20px; position:relative; }
            .ALTO { color:var(--red); font-weight:bold; border:2px solid var(--red); padding:5px; }
            .MODERADO { color:var(--yellow); font-weight:bold; border:2px solid var(--yellow); padding:5px; }
            .BAJO { color:var(--green); font-weight:bold; border:2px solid var(--green); padding:5px; }
            
            .grid-3 { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:20px; margin:20px 0; }
            .label { color:var(--pink); font-size:10px; display:block; text-transform:uppercase; }
            .value { color:#fff; font-size:14px; }

            /* Chat Flotante */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:300px; border:2px solid var(--pink); background:#000; z-index:2000; box-shadow: 0 0 15px var(--pink); }
            .chat-head { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; display:flex; justify-content:space-between; }
            .chat-body { height:200px; padding:15px; display:block; overflow-y:auto; font-size:12px; color:var(--green); }

            /* Indicadores Financieros */
            .ind-card { border:1px solid var(--green); padding:15px; text-align:center; background:#050505; }
        </style>
    </head>
    <body>

    <div class="nav-top">
        <form method="POST" style="display:contents;">
            <input type="hidden" name="view_state" value="scout">
            <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'scout' }}">SCOUT GLOBAL</button>
            <input type="hidden" name="view_state" value="memoria">
            <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
            <input type="hidden" name="view_state" value="builder">
            <button type="submit" name="action" value="v" class="btn {{ 'btn-active' if view == 'builder' }}">CONSTRUCTOR</button>
            <button type="submit" name="action" value="clear_all" class="btn" style="border-color:red; color:red;">LIMPIAR TODO</button>
        </form>
    </div>

    <div id="progress-box"><div id="progress-bar"></div></div>

    {% if view == 'scout' %}
        <form method="POST" onsubmit="startLoader()">
            <input type="hidden" name="view_state" value="scout">
            <button type="submit" name="action" value="run_global" class="btn" style="width:100%; background:var(--green); color:#000;">INICIAR RASTREO PROFUNDO 2026</button>
        </form>
        
        <div style="margin-top:20px;">
            {% for r in session['history'] %}
            <div class="ficha">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                    <span class="{{ r.riesgo }}">RIESGO {{ r.riesgo }}</span>
                </div>
                <div class="grid-3">
                    <div><span class="label">Ubicación</span><span class="value">{{ r.ubicacion }}</span></div>
                    <div><span class="label">Capacidad</span><span class="value">{{ r.capacidad }}</span></div>
                    <div><span class="label">ID Sistema</span><span class="value">{{ r.id }}</span></div>
                    <div><span class="label">CEO / Líder</span><span class="value">{{ r.ceo }}</span></div>
                    <div><span class="label">Móvil Contacto</span><span class="value">{{ r.movil }}</span></div>
                    <div><span class="label">Email</span><span class="value">{{ r.email }}</span></div>
                </div>
                <div style="border-top:1px solid #222; padding-top:15px;">
                    <span class="label">Resumen Ejecutivo Elaborado</span>
                    <p style="color:#ccc; font-size:13px; line-height:1.6;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[VER FUENTE ORIGINAL]</a>
                </div>
                <form method="POST" style="position:absolute; top:20px; right:200px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save_memoria" class="btn" style="font-size:10px;">GUARDAR EN MEMORIA</button>
                </form>
            </div>
            {% endfor %}
        </div>

    {% elif view == 'memoria' %}
        <h2 style="color:var(--pink);">PROYECTOS EN MEMORIA</h2>
        {% for r in session['saved'] %}
        <div class="ficha"><strong>{{ r.nombre }}</strong> - {{ r.id }}</div>
        {% endfor %}

    {% elif view == 'builder' %}
        <div class="ficha">
            <h2 style="color:var(--pink);">NUEVO PROYECTO: CONFIGURACIÓN CAPEX/OPEX</h2>
            <form method="POST">
                <div class="grid-3">
                    <div><label class="label">CAPEX (COP)</label><input type="text" name="capex" placeholder="90000000000"></div>
                    <div><label class="label">CAPACIDAD (MW)</label><input type="number" step="0.1" name="capacidad"></div>
                    <div><label class="label">PPA (COP/kWh)</label><input type="number" name="ppa"></div>
                </div>
                <button type="submit" name="action" value="hacer_modelo" class="btn" style="width:100%; background:var(--green); color:#000;">EJECUTAR MODELO FINANCIERO</button>
            </form>
        </div>

        {% if session.get('calc') %}
        <div class="grid-3">
            <div class="ind-card"><span class="label">VPN</span><div style="font-size:20px; color:#fff;">{{ session['calc'].vpn }}</div></div>
            <div class="ind-card"><span class="label">TIR</span><div style="font-size:20px; color:#fff;">{{ session['calc'].tir }}</div></div>
            <div class="ind-card"><span class="label">PAYBACK</span><div style="font-size:20px; color:#fff;">{{ session['calc'].payback }}</div></div>
        </div>
        <div class="grid-3">
            <div class="ind-card"><span class="label">OPEX ANUAL</span><div style="color:var(--pink);">{{ session['calc'].opex_anual }}</div></div>
            <div class="ind-card"><span class="label">CAPEX / MW</span><div style="color:var(--pink);">{{ session['calc'].capex_mw }}</div></div>
        </div>
        <div class="ficha">
            <canvas id="mainChart" style="max-height:300px;"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('mainChart'), {
                type: 'line',
                data: {
                    labels: ['Año 1', 'Año 2', 'Año 3', 'Año 4'],
                    datasets: [{
                        label: 'Flujo de Ingresos Estimado',
                        data: {{ session['calc'].chart_data }},
                        borderColor: '#0f0',
                        backgroundColor: 'rgba(0,255,0,0.1)',
                        fill: true
                    }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        </script>
        {% endif %}
    {% endif %}

    <div id="maia-chat">
        <div class="chat-head" onclick="toggleChat()">
            <span>MAIA INTELLIGENCE</span>
            <span>[-]</span>
        </div>
        <div class="chat-body" id="chat-body">
            <p>> Sistema V.14 Listo.</p>
            <p>> Memoria Activa: {{ session['saved']|length }} ítems.</p>
            <p>> Motor de Modelado conectado.</p>
            {% if session.get('calc') %}
            <p>> Indicadores generados exitosamente.</p>
            {% endif %}
        </div>
    </div>

    <script>
        function toggleChat() {
            var b = document.getElementById('chat-body');
            b.style.display = (b.style.display == 'none') ? 'block' : 'none';
        }
        function startLoader() {
            document.getElementById('progress-box').style.display = 'block';
            var bar = document.getElementById('progress-bar');
            var w = 0;
            var i = setInterval(function(){
                w += 5; bar.style.width = w + '%';
                if(w >= 100) clearInterval(i);
            }, 100);
        }
    </script>
    </body>
    </html>
    """
    return render_template_string(html, view=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)