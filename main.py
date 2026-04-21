# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
from builder_engine import builder_engine

app = Flask(__name__)
app.secret_key = "maia_final_fixed_v18"

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
            session['calc'] = builder_engine.calcular_modelo_pro(request.form)
            session.modified = True
            view = 'builder'

    html = """
    <!DOCTYPE html>
    <html><head>
        <title>MAIA II - V18 PRO</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; }
            .nav { border-bottom:2px solid var(--pink); padding:10px; display:flex; gap:20px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            /* BARRA DE PROGRESO */
            #progress-cont { width:100%; height:10px; background:#111; margin:10px 0; display:none; }
            #progress-bar { width:0%; height:100%; background:var(--green); transition:0.3s; }

            .panel { background:#0a0a0a; border:1px solid #333; padding:20px; margin-top:20px; border-left:5px solid var(--neon); }
            .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:20px; }
            
            #maia-chat { position:fixed; bottom:0; right:20px; width:320px; border:2px solid var(--pink); background:#000; z-index:1000; }
            .chat-h { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; display:flex; justify-content:space-between; }
            #chat-b { height:200px; padding:15px; overflow-y:auto; font-size:12px; color:var(--green); }
            
            input { width:100%; background:#111; border:1px solid var(--neon); color:#fff; padding:10px; box-sizing:border-box; }
        </style>
    </head><body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">1. SCOUT DE NEGOCIOS</button>
                <button type="submit" name="view_state" value="builder" class="btn {{ 'active' if view == 'builder' }}">2. CONSTRUCTOR EXPERTO</button>
            </form>
        </div>

        <div id="progress-cont"><div id="progress-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" onsubmit="startLoad()">
                <button type="submit" name="action" value="run_scout" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green);">EJECUTAR BÚSQUEDA DE PROYECTOS REALES</button>
            </form>
            {% for r in session['history'] %}
            <div class="panel">
                <div style="display:flex; justify-content:space-between;">
                    <h3 style="margin:0;">{{ r.nombre }}</h3>
                    <span style="border:1px solid; padding:5px; font-size:11px; color:{{ 'red' if r.riesgo == 'ALTO' else 'var(--green)' }}">RIESGO: {{ r.riesgo }}</span>
                </div>
                <p style="color:#ccc; font-size:13px;">{{ r.resumen }}</p>
                <div style="display:flex; justify-content:space-between; font-size:11px;">
                    <span>UBICACIÓN: {{ r.ubicacion }}</span>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[VER FUENTE Y PLIEGOS]</a>
                </div>
            </div>
            {% endfor %}

        {% elif view == 'builder' %}
            <div class="panel">
                <h2 style="color:var(--pink); margin-top:0;">MODELO DE INVERSIÓN AVANZADO</h2>
                <form method="POST" onsubmit="startLoad()">
                    <div class="grid">
                        <div><label>CAPEX (COP)</label><input type="text" name="capex" value="90389977843"></div>
                        <div><label>CAPACIDAD (MW)</label><input type="number" step="0.01" name="capacidad" value="23.42"></div>
                        <div><label>PPA (COP/kWh)</label><input type="number" name="ppa" value="323"></div>
                    </div>
                    <button type="submit" name="action" value="run_builder" class="btn" style="width:100%; margin-top:20px; background:var(--green); color:#000;">CALCULAR PROYECCIÓN FINANCIERA</button>
                </form>
            </div>

            {% if session.get('calc') %}
            <div class="grid">
                <div class="panel">
                    <h4 style="color:var(--pink);">RESULTADOS INDICADORES</h4>
                    VPN: $ {{ session['calc'].vpn }}<br>
                    TIR: {{ session['calc'].tir }}<br>
                    EBITDA: $ {{ session['calc'].ebitda }}<br>
                    FCL: $ {{ session['calc'].fcl }}<br>
                    <strong style="color:var(--green);">MONTECARLO (Prob. Éxito): {{ session['calc'].probabilidad }}</strong>
                </div>
                <div class="panel">
                    <h4 style="color:var(--pink);">OPEX ANUALIZADO</h4>
                    {% for k, v in session['calc'].opex_list.items() %}
                        <small>{{ k }}: ${{ v }}</small><br>
                    {% endfor %}
                </div>
                <div class="panel"><canvas id="proChart"></canvas></div>
            </div>
            <script>
                new Chart(document.getElementById('proChart'), { type:'line', data:{ labels:[1,2,3,4,5,6,7,8,9,10], datasets:[{label:'Flujo Caja Libre', data: {{ session['calc'].chart }}, borderColor:'#0f0', fill:true, backgroundColor:'rgba(0,255,0,0.1)'}] } });
            </script>
            {% endif %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA INTELLIGENCE CORE</span><span id="t-ico">[-]</span></div>
            <div id="chat-b">
                > Sistema V.18 Estabilizado.<br>> Búsqueda enfocada en RFPs/Licitaciones.<br>> Modelo Financiero con Tax/Depreciación.<br>> Montecarlo nativo 1000 iteraciones.
            </div>
        </div>
        <script>
            function toggle(){ var b=document.getElementById('chat-b'); var i=document.getElementById('t-ico'); if(b.style.display=='none'){ b.style.display='block'; i.innerText='[-]'; } else { b.style.display='none'; i.innerText='[+]'; } }
            function startLoad(){ document.getElementById('progress-cont').style.display='block'; var bar=document.getElementById('progress-bar'); var w=0; setInterval(function(){ w+=5; if(w<=100) bar.style.width=w+'%'; }, 100); }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
