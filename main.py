# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_ultra_shield_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
    
    results = []
    summary_data = {}

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_scout':
            c = request.form.get('country', '')
            t = request.form.get('tech', '')
            results = scout_engine.execute_brutal_search(c, t)
            session['history'] = results
            session.modified = True
            
        elif action == 'clear':
            session['history'] = []
            session.modified = True
            results = []

    # Recuperar de memoria y generar resumen
    display_results = results if results else session.get('history', [])
    if display_results:
        summary_data = scout_engine.generate_summary_table(display_results)

    html = """
    <html><head>
        <title>MAIA II - CONSOLA DE RASTREO</title>
        <style>
            body { background:#000; color:#0ff; font-family:monospace; padding:20px; }
            .header { border-bottom:2px solid #f0f; padding-bottom:15px; margin-bottom:25px; display:flex; justify-content:space-between; }
            .search-box { background:#111; border:1px solid #0ff; padding:20px; margin-bottom:30px; }
            input { background:#000; border:1px solid #0ff; color:#fff; padding:12px; width:30%; margin-right:10px; }
            .btn { padding:12px 25px; font-weight:bold; cursor:pointer; border:none; text-transform:uppercase; }
            .btn-scout { background:#0f0; color:#000; }
            .btn-clear { background:#555; color:#fff; }
            
            /* CUADRO DE RESUMEN */
            .summary-table { width:100%; border:2px solid #f0f; margin-top:30px; border-collapse:collapse; background:rgba(255,0,255,0.05); }
            .summary-table th { background:#f0f; color:#000; padding:10px; text-align:left; }
            .summary-table td { border:1px solid #f0f; padding:10px; }
            
            .card { border:1px solid #0f0; padding:25px; margin-bottom:20px; background:rgba(0,40,0,0.2); position:relative; }
            .risk-tag { position:absolute; top:15px; right:15px; padding:5px 12px; font-weight:bold; border:1px solid; }
            .risk-ALTO { border-color:#f00; color:#f00; }
            .risk-MODERADO { border-color:#ff0; color:#ff0; }
            .risk-BAJO { border-color:#0f0; color:#0f0; }

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
                <h1 style="margin:0; letter-spacing:2px;">MAIA II <span style="color:#f0f;">SCOUT ENGINE</span></h1>
                <small style="color:#0f0;">MODO: BÚSQUEDA BRUTAL 100% REAL EN VIVO</small>
            </div>
            <div style="text-align:right;">
                <div id="clock"></div>
                <small>MEMORIA: {{ session['history']|length }} ACTIVOS</small>
            </div>
        </div>

        <div class="search-box">
            <form method="post">
                <input type="text" name="country" placeholder="PAÍS (EJ: COLOMBIA)" required>
                <input type="text" name="tech" placeholder="TECNOLOGÍA (EJ: HIDRÓGENO)" required>
                <button type="submit" name="action" value="run_scout" class="btn btn-scout">INICIAR RASTREO</button>
                <button type="submit" name="action" value="clear" class="btn btn-clear">LIMPIAR MEMORIA</button>
            </form>
        </div>

        <div id="results">
            {% for r in results %}
            <div class="card">
                <div class="risk-tag risk-{{ r.Riesgo }}">RIESGO: {{ r.Riesgo }}</div>
                <h3 style="margin:0 0 10px 0; color:#0ff;">{{ r.Nombre }}</h3>
                <p style="color:#888; font-size:11px;">TIMESTAMP: {{ r.Fecha_Rastreo }} | UBICACIÓN: {{ r.Ubicación }}</p>
                <p>{{ r.Resumen }}</p>
                <div style="background:rgba(0,255,255,0.1); padding:12px; margin-top:15px; border-left:4px solid #0ff;">
                    <b>CEO/DUEÑO:</b> {{ r.CEO }}<br>
                    <b>LINK DE CONTACTO:</b> <a href="{{ r.Contacto }}" target="_blank" style="color:#f0f; text-decoration:none;">{{ r.Contacto }}</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if summary_data %}
        <table class="summary-table">
            <thead>
                <tr>
                    <th>TECNOLOGÍA ANALIZADA</th>
                    <th>PROYECTOS ENCONTRADOS (REAL-TIME)</th>
                    <th>ESTADO DEL RASTREO</th>
                </tr>
            </thead>
            <tbody>
                {% for tech, count in summary_data.items() %}
                <tr>
                    <td>{{ tech }}</td>
                    <td>{{ count }} Proyectos detectados</td>
                    <td style="color:#0f0;">✓ VERIFICADO POR MAIA</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <div id="maia-chat" class="minimized">
            <div class="chat-header" onclick="toggleChat()">MAIA ECONOMIST INTERFACE <span>[+/-]</span></div>
            <div class="chat-body">
                <div style="height:250px; overflow-y:auto; font-size:13px; border-bottom:1px solid #333;">
                    <p style="color:#0f0;">[SISTEMA]: Motor Scout listo para ejecución.</p>
                    {% if summary_data %}
                    <p>He resumido {{ session['history']|length }} hallazgos en la tabla de control inferior.</p>
                    {% endif %}
                </div>
                <input type="text" placeholder="Consultar sobre viabilidad..." style="width:100%; margin-top:15px; background:#000; border:1px solid #0ff; color:#fff; padding:8px;">
            </div>
        </div>
    </body></html>
    """
    return render_template_string(html, results=display_results, summary_data=summary_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
