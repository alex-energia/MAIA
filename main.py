# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine

app = Flask(__name__)
app.secret_key = "maia_shield_v16_no_error"

@app.context_processor
def utility_processor():
    return dict(int=int)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
            session.modified = True
            view = 'scout'
        elif action == 'hacer_modelo':
            session['calc'] = builder_engine.calculate_model_completo(request.form)
            session.modified = True
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html><head>
        <title>MAIA II - V.16</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:20px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px; cursor:pointer; }
            .btn-active { background:var(--pink); color:#000; }
            .panel { background:#0a0a0a; border:1px solid #333; padding:20px; margin-top:20px; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; }
            
            /* Chat */
            #maia-chat { position:fixed; bottom:0; right:20px; width:300px; border:2px solid var(--pink); background:#000; }
            .chat-h { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; }
            #chat-b { height:200px; padding:10px; display:block; overflow-y:auto; font-size:12px; }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'btn-active' if view == 'scout' }}">SCOUT REAL</button>
                <button type="submit" name="view_state" value="builder" class="btn {{ 'btn-active' if view == 'builder' }}">CONSTRUCTOR</button>
            </form>
        </div>

        {% if view == 'scout' %}
            <form method="POST"><button type="submit" name="action" value="run_global" class="btn" style="width:100%; margin-top:20px; color:var(--green);">INICIAR RASTREO REAL</button></form>
            {% for r in session['history'] %}
                <div class="panel">
                    <h3>{{ r.nombre }}</h3>
                    <p>{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">VER FUENTE REAL</a>
                </div>
            {% endfor %}
        {% elif view == 'builder' %}
            <div class="panel">
                <form method="POST">
                    <div class="grid">
                        <input type="text" name="capex" placeholder="CAPEX (COP)" value="90389977843">
                        <input type="number" step="0.01" name="capacidad" placeholder="MW" value="23.42">
                        <input type="number" name="ppa" placeholder="PPA" value="323">
                    </div>
                    <button type="submit" name="action" value="hacer_modelo" class="btn" style="width:100%; margin-top:20px; background:var(--green); color:#000;">CALCULAR MODELO</button>
                </form>
            </div>
            {% if session.get('calc') %}
                <div class="grid">
                    <div class="panel">VPN: {{ session['calc'].indicadores.vpn }}</div>
                    <div class="panel">ÉXITO MONTECARLO: {{ session['calc'].indicadores.probabilidad_exito }}</div>
                </div>
                <div class="grid">
                    <div class="panel">
                        <strong>CAPEX DETALLADO</strong><br>
                        {% for k,v in session['calc'].capex_detallado.items() %}
                            <small>{{k}}: ${{int(v):,}}</small><br>
                        {% endfor %}
                    </div>
                    <div class="panel">
                        <strong>OPEX ANUAL</strong><br>
                        {% for k,v in session['calc'].opex_detallado.items() %}
                            <small>{{k}}: ${{int(v):,}}</small><br>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()">MAIA INTELLIGENCE CORE [-]</div>
            <div id="chat-b">
                > V.16 Online.<br>> Error 500 Solucionado.<br>> Montecarlo nativo activo.
            </div>
        </div>

        <script>
            function toggle() {
                var b = document.getElementById('chat-b');
                b.style.display = (b.style.display == 'none') ? 'block' : 'none';
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view)
