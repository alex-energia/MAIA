# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_ultra_access_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
    
    results = []
    summary_data = {}

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_specialized':
            # Búsqueda con filtros específicos
            c = request.form.get('country')
            t = request.form.get('tech')
            results = scout_engine.execute_brutal_search(c, t, is_global=False)
            session['history'] = results
            session.modified = True
            
        elif action == 'run_global_scout':
            # Búsqueda en todo el mundo y todas las tecnologías
            results = scout_engine.execute_brutal_search("", "", is_global=True)
            session['history'] = results
            session.modified = True
            
        elif action == 'clear':
            session['history'] = []
            session.modified = True
            results = []

    # Recuperar memoria
    display_results = results if results else session.get('history', [])
    if display_results:
        summary_data = scout_engine.generate_summary_table(display_results)

    html = """
    <html><head>
        <title>MAIA II - CONSOLA BLINDADA</title>
        <style>
            body { background:#000; color:#0ff; font-family:monospace; padding:20px; }
            .header { border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; display:flex; justify-content:space-between; }
            .search-box { background:#111; border:1px solid #0ff; padding:25px; margin-bottom:30px; }
            
            select, .btn { padding:12px; font-weight:bold; border:none; text-transform:uppercase; font-family:monospace; }
            select { background:#000; border:1px solid #0ff; color:#fff; width:25%; margin-right:10px; }
            
            .btn-special { background:#0f0; color:#000; cursor:pointer; margin-right:10px; }
            .btn-global { background:#f0f; color:#000; cursor:pointer; margin-right:10px; }
            .btn-clear { background:#444; color:#fff; cursor:pointer; }
            
            .card { border:1px solid #0f0; padding:25px; margin-bottom:20px; background:rgba(0,40,0,0.1); position:relative; }
            .risk-tag { position:absolute; top:15px; right:15px; padding:5px 12px; font-weight:bold; border:1px solid; }
            .risk-ALTO { border-color:#f00; color:#f00; }
            .risk-MODERADO { border-color:#ff0; color:#ff0; }
            .risk-BAJO { border-color:#0f0; color:#0f0; }

            .summary-table { width:100%; border:2px solid #f0f; margin-top:30px; border-collapse:collapse; }
            .summary-table th { background:#f0f; color:#000; padding:12px; text-align:left; }
            .summary-table td { border:1px solid #f0f; padding:12px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:380px; border:2px solid #f0f; background:#000; transition:0.3s; z-index:999; }
            .chat-header { background:#f0f; color:#000; padding:12px; cursor:pointer; font-weight:bold; display:flex; justify-content:space-between; }
            .chat-body { height:320px; padding:15px; display:block; }
            .minimized { height:45px !important; overflow:hidden; border-color:#0ff !important; }
            .minimized .chat-header { background:#0ff; }
        </style>
        <script>
            function toggleChat() { document.getElementById('maia-chat').classList.toggle('minimized'); }
            setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleString(); }, 1000);
        </script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0;">MAIA II <span style="color:#f0f;">CONTROL PANEL</span></h1>
                <small style="color:#0f0;">SISTEMA OPERATIVO DE RASTREO EN TIEMPO REAL</small>
            </div>
            <div style="text-align:right;">
                <div id="clock" style="font-size:18px;"></div>
                <small>CACHE: {{ session['history']|length }} PROYECTOS</small>
            </div>
        </div>

        <div class="search-box">
            <form method="post">
                <select name="country">
                    <option value="" disabled selected>SELECCIONE PAÍS</option>
                    {% for p in scout_engine.Paises %}
                    <option value="{{ p }}">{{ p }}</option>
                    {% endfor %}
                    <option value="TODOS">TODOS</option>
                </select>

                <select name="tech">
                    <option value="" disabled selected>SELECCIONE TECNOLOGÍA</option>
                    {% for t in scout_engine.Tecnologias %}
                    <option value="{{ t }}">{{ t }}</option>
                    {% endfor %}
                    <option value="TODAS">TODAS</option>
                </select>

                <button type="submit" name="action" value="run_specialized" class="btn btn-special">INICIAR RASTREO ESPECIAL</button>
                <button type="submit" name="action" value="run_global_scout" class="btn btn-global">SCOUT GLOBAL</button>
                <button type="submit" name="action" value="clear" class="btn btn-clear">LIMPIAR</button>
            </form>
        </div>

        <div id="results">
            {% for r in display_results %}
            <div class="card">
                <div class="risk-tag risk-{{ r.Riesgo }}">RIESGO: {{ r.Riesgo }}</div>
                <h3 style="margin:0 0- 10px 0; color:#0ff;">{{ r.Nombre }}</h3>
                <p style="color:#888; font-size:11px;">FECHA RASTREO: {{ r.Fecha_Rastreo }} | TECNOLOGÍA: {{ r.Tecnología }}</p>
                <p>{{ r.Resumen }}</p>
                <div style="background:rgba(0,255,255,0.1); padding:12px; margin-top:15px; border-left:4px solid #0ff;">
                    <b>CEO:</b> {{ r.CEO }} | <b>FUENTE:</b> <a href="{{ r.Contacto }}" target="_blank" style="color:#f0f;">ENLACE DIRECTO</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if summary_data %}
        <table class="summary-table">
            <thead>
                <tr>
                    <th>TECNOLOGÍA</th>
                    <th>PROYECTOS DETECTADOS</th>
                    <th>ESTADO MAIA</th>
                </tr>
            </thead>
            <tbody>
                {% for tech, count in summary_data.items() %}
                <tr>
                    <td>{{ tech }}</td>
                    <td>{{ count }} Hallazgos</td>
                    <td style="color:#0f0;">ACTIVO / ANALIZADO</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <div id="maia-chat" class="minimized">
            <div class="chat-header" onclick="toggleChat()">MAIA INTERFACE <span>[+/-]</span></div>
            <div class="chat-body">
                <div style="height:250px; overflow-y:auto; font-size:13px; border-bottom:1px solid #333;">
                    <p style="color:#0f0;">[SECURE SESSION ACTIVE]</p>
                    <p>Esperando comandos de análisis sobre los datos del Scout.</p>
                </div>
                <input type="text" placeholder="Consultar sobre viabilidad..." style="width:100%; margin-top:15px; background:#000; border:1px solid #0ff; color:#fff; padding:10px;">
            </div>
        </div>
    </body></html>
    """
    return render_template_string(html, display_results=display_results, summary_data=summary_data, scout_engine=scout_engine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
