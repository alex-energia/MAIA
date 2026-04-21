# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine

app = Flask(__name__)
app.secret_key = "maia_ultimate_v17"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    view = request.form.get('view_state', 'scout')
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.execute_global_scout()
            session.modified = True
            view = 'scout'
        elif action == 'run_builder':
            session['calc'] = builder_engine.calcular_modelo_completo(request.form)
            session.modified = True
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html><head>
        <title>MAIA II - V17 GOLD</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; }
            .nav { border-bottom:2px solid var(--pink); padding:10px; display:flex; gap:20px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            .panel { background:#0a0a0a; border:1px solid #333; padding:20px; margin-top:20px; border-left:4px solid var(--pink); }
            .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:20px; }
            #chat { position:fixed; bottom:0; right:20px; width:300px; border:2px solid var(--pink); background:#000; z-index:999; }
            .chat-h { background:var(--pink); color:#000; padding:10px; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { height:180px; padding:10px; overflow-y:auto; font-size:11px; color:var(--green); }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">1. SCOUT REAL-TIME</button>
                <button type="submit" name="view_state" value="builder" class="btn {{ 'active' if view == 'builder' }}">2. MODELO FINANCIERO PRO</button>
            </form>
        </div>

        {% if view == 'scout' %}
            <form method="POST"><button type="submit" name="action" value="run_scout" class="btn" style="width:100%; margin-top:20px; color:var(--green);">INICIAR RASTREO PROFUNDO 2026</button></form>
            {% for r in session['history'] %}
            <div class="panel">
                <h3>{{ r.title }}</h3>
                <p style="color:#ccc;">{{ r.body }}</p>
                <a href="{{ r.link }}" target="_blank" style="color:var(--pink);">IR A FUENTE OFICIAL</a>
            </div>
            {% endfor %}

        {% elif view == 'builder' %}
            <div class="panel">
                <form method="POST">
                    <div class="grid">
                        <div><label style="font-size:10px;">CAPEX TOTAL (COP)</label><input type="text" name="capex" value="90389977843" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:8px;"></div>
                        <div><label style="font-size:10px;">CAPACIDAD (MW)</label><input type="number" step="0.01" name="capacidad" value="23.42" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:8px;"></div>
                        <div><label style="font-size:10px;">PPA (COP/kWh)</label><input type="number" name="ppa" value="323" style="width:100%; background:#111; color:#fff; border:1px solid var(--neon); padding:8px;"></div>
                    </div>
                    <button type="submit" name="action" value="run_builder" class="btn" style="width:100%; margin-top:20px; background:var(--green); color:#000;">GENERAR MODELO DE INVERSIÓN</button>
                </form>
            </div>

            {% if session.get('calc') %}
            <div class="grid">
                <div class="panel">
                    <h4 style="color:var(--pink); margin-top:0;">INDICADORES CLAVE</h4>
                    VPN: $ {{ session['calc'].vpn }}<br>
                    TIR: {{ session['calc'].tir }}<br>
                    EBITDA ANUAL: $ {{ session['calc'].ebitda }}<br>
                    IMPUESTOS (TAX): $ {{ session['calc'].impuestos }}<br>
                    <strong style="color:var(--green);">MONTECARLO (Prob. Éxito): {{ session['calc'].exito }}</strong>
                </div>
                <div class="panel">
                    <h4 style="color:var(--pink); margin-top:0;">DESGLOSE OPEX</h4>
                    {% for k, v in session['calc'].opex_list.items() %}
                        <small>{{ k }}: ${{ v }}</small><br>
                    {% endfor %}
                </div>
                <div class="panel"><canvas id="finChart"></canvas></div>
            </div>
            <script>
                new Chart(document.getElementById('finChart'), { type:'line', data:{ labels:[1,2,3,4,5,6,7,8,9,10], datasets:[{label:'Flujo Neto', data: {{ session['calc'].chart }}, borderColor:'#0f0'}] } });
            </script>
            {% endif %}
        {% endif %}

        <div id="chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA INTELLIGENCE CORE</span><span id="t-ico">[-]</span></div>
            <div id="chat-b">
                > V.17 Gold Status.<br>> Error 500 Eliminado.<br>> Modelo de Impuestos/Depreciación Activo.<br>> Búsqueda Real 2026 Conectada.
            </div>
        </div>
        <script>
            function toggle() {
                var b = document.getElementById('chat-b');
                var i = document.getElementById('t-ico');
                if(b.style.display == 'none'){ b.style.display = 'block'; i.innerText = '[-]'; }
                else { b.style.display = 'none'; i.innerText = '[+]'; }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
