# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_final_shield_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    # Asegurar que la memoria exista
    if 'history' not in session:
        session['history'] = []
    
    # Variables de control
    display_results = session.get('history', [])
    summary_data = {}

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_specialized':
            pais = request.form.get('country')
            tech = request.form.get('tech')
            # Ejecutar búsqueda con filtros
            new_results = scout_engine.execute_brutal_search(pais, tech, is_global=False)
            session['history'] = new_results
            session.modified = True
            display_results = new_results
            
        elif action == 'run_global_scout':
            # Ejecutar búsqueda global sin filtros
            new_results = scout_engine.execute_brutal_search("", "", is_global=True)
            session['history'] = new_results
            session.modified = True
            display_results = new_results
            
        elif action == 'clear':
            session['history'] = []
            session.modified = True
            display_results = []

    # Generar tabla si hay resultados
    if display_results:
        summary_data = scout_engine.generate_summary_table(display_results)

    html = """
    <html><head>
        <title>MAIA II - SCOUT COMMAND</title>
        <style>
            body { background:#000; color:#0ff; font-family:monospace; padding:25px; }
            .header { border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; display:flex; justify-content:space-between; align-items:center; }
            .search-box { background:#111; border:1px solid #0ff; padding:25px; margin-bottom:30px; }
            
            select, .btn { padding:12px; font-weight:bold; font-family:monospace; font-size:13px; }
            select { background:#000; border:1px solid #0ff; color:#fff; width:22%; margin-right:10px; }
            
            .btn { cursor:pointer; text-transform:uppercase; border:1px solid transparent; }
            .btn-special { background:#0f0; color:#000; }
            .btn-global { background:#f0f; color:#000; }
            .btn-clear { background:#444; color:#fff; }
            
            .card { border:1px solid #0f0; padding:20px; margin-bottom:20px; background:rgba(0,40,0,0.1); position:relative; }
            .risk-tag { position:absolute; top:15px; right:15px; padding:5px 10px; font-weight:bold; border:1px solid; }
            .risk-ALTO { border-color:#f00; color:#f00; }
            .risk-MODERADO { border-color:#ff0; color:#ff0; }
            .risk-BAJO { border-color:#0f0; color:#0f0; }

            .summary-table { width:100%; border:2px solid #f0f; margin-top:30px; border-collapse:collapse; }
            .summary-table th { background:#f0f; color:#000; padding:12px; text-align:left; }
            .summary-table td { border:1px solid #f0f; padding:12px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:380px; border:2px solid #f0f; background:#000; z-index:1000; }
            .chat-header { background:#f0f; color:#000; padding:10px; cursor:pointer; font-weight:bold; display:flex; justify-content:space-between; }
            .chat-body { height:300px; padding:15px; }
            .minimized { height:45px !important; overflow:hidden; }
        </style>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0;">MAIA II <span style="color:#f0f;">SCOUT</span></h1>
                <small style="color:#0f0;">SISTEMA DE BÚSQUEDA REAL ACTIVO</small>
            </div>
            <div style="text-align:right;">
                <div id="clock"></div>
                <small>MEMORIA: {{ display_results|length }} ITEMS</small>
            </div>
        </div>

        <div class="search-box">
            <form method="POST" action="/">
                <select name="country">
                    <option value="BORRAR">-- ZONA / PAÍS --</option>
                    {% for p in scout_engine.Paises %}
                    <option value="{{ p }}">{{ p }}</option>
                    {% endfor %}
                </select>

                <select name="tech">
                    <option value="BORRAR">-- TECNOLOGÍA --</option>
                    {% for t in scout_engine.Tecnologias %}
                    <option value="{{ t }}">{{ t }}</option>
                    {% endfor %}
                </select>

                <button type="submit" name="action" value="run_specialized" class="btn btn-special">INICIAR RASTREO</button>
                <button type="submit" name="action" value="run_global_scout" class="btn btn-global">SCOUT GLOBAL</button>
                <button type="submit" name="action" value="clear" class="btn btn-clear">LIMPIAR</button>
            </form>
        </div>

        <div id="results">
            {% for r in display_results %}
            <div class="card">
                <div class="risk-tag risk-{{ r.Riesgo }}">RIESGO: {{ r.Riesgo }}</div>
                <h3 style="margin:0; color:#0ff;">{{ r.Nombre }}</h3>
                <p style="color:#888; font-size:11px; margin:5px 0;">ZONA: {{ r.Ubicación }} | TEC: {{ r.Tecnología }} | {{ r.Fecha_Rastreo }}</p>
                <p>{{ r.Resumen }}</p>
                <div style="margin-top:15px; padding-top:10px; border-top:1px solid #333;">
                    <a href="{{ r.Contacto }}" target="_blank" style="color:#f0f;">VER FUENTE ORIGINAL</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if summary_data %}
        <table class="summary-table">
            <thead>
                <tr>
                    <th>TECNOLOGÍA</th>
                    <th>PROYECTOS</th>
                    <th>ESTADO</th>
                </tr>
            </thead>
            <tbody>
                {% for tech, count in summary_data.items() %}
                <tr>
                    <td>{{ tech }}</td>
                    <td>{{ count }}</td>
                    <td style="color:#0f0;">PROCESADO</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <div id="maia-chat" class="minimized" onclick="this.classList.toggle('minimized')">
            <div class="chat-header">MAIA AGENT <span>[+/-]</span></div>
            <div class="chat-body">
                <p>> Esperando búsqueda...</p>
                {% if display_results %}
                <p>> {{ display_results|length }} resultados cargados en memoria.</p>
                {% endif %}
            </div>
        </div>

        <script>
            setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleString(); }, 1000);
        </script>
    </body></html>
    """
    return render_template_string(html, display_results=display_results, summary_data=summary_data, scout_engine=scout_engine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
