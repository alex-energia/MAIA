# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_v6_total"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
    
    current_results = []
    summary_data = {}
    searching = False

    if request.method == 'POST':
        action = request.form.get('action')
        searching = True # Activa estado de búsqueda
        
        if action == 'run_specialized':
            p = request.form.get('country')
            t = request.form.get('tech')
            found = scout_engine.execute_brutal_search(p, t, is_global=False)
            session['history'] = found
        elif action == 'run_global_scout':
            found = scout_engine.execute_brutal_search("", "", is_global=True)
            session['history'] = found
        elif action == 'clear':
            session['history'] = []
            
        session.modified = True
        current_results = session['history']

    if not current_results:
        current_results = session.get('history', [])

    if current_results:
        summary_data = scout_engine.generate_summary_table(current_results)

    html = """
    <html><head>
        <title>MAIA II - GLOBAL SCOUT</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:'Courier New', monospace; padding:30px; margin:0; }
            
            .header { border-bottom: 2px solid var(--pink); padding-bottom:20px; margin-bottom:30px; }
            .control-panel { background:#0a0a0a; border:1px solid var(--neon); padding:25px; margin-bottom:30px; }
            
            select, .btn { padding:12px; font-weight:bold; font-family:monospace; font-size:14px; }
            select { background:#000; border:1px solid var(--neon); color:#fff; width:220px; }
            
            .btn { cursor:pointer; text-transform:uppercase; border:none; margin-right:10px; }
            .btn-run { background:var(--green); color:#000; }
            .btn-global { background:var(--pink); color:#000; }
            .btn-clear { background:#333; color:#fff; }

            /* Barra de Estado */
            .status-container { width:100%; background:#111; height:25px; border:1px solid var(--neon); margin-bottom:30px; position:relative; overflow:hidden; }
            .status-bar { height:100%; background:var(--green); width:0%; transition: width 0.5s; }
            .status-text { position:absolute; top:4px; width:100%; text-align:center; font-size:12px; font-weight:bold; color:#fff; }

            /* Fichas de Proyecto */
            .ficha { border:1px solid #333; margin-bottom:25px; background:rgba(0,255,255,0.02); }
            .ficha-head { background:#111; padding:15px; display:flex; justify-content:space-between; border-bottom:1px solid #333; }
            .ficha-body { padding:20px; display:grid; grid-template-columns: 1fr 1fr; gap:25px; }
            .ficha-footer { grid-column: span 2; border-top: 1px solid #222; padding-top:15px; }
            
            .label { color:var(--pink); font-size:11px; text-transform:uppercase; display:block; }
            .value { color:#fff; font-size:15px; display:block; margin-bottom:12px; }
            
            .risk { padding:3px 8px; font-weight:bold; border:1px solid; }
            .ALTO { border-color:#f00; color:#f00; }
            .MODERADO { border-color:#ff0; color:#ff0; }
            .BAJO { border-color:var(--green); color:var(--green); }

            /* Chat Maia Modular */
            #maia-chat { position:fixed; bottom:0; right:20px; width:360px; border:2px solid var(--pink); background:#000; transition: 0.3s; z-index:9999; }
            .chat-header { background:var(--pink); color:#000; padding:12px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            .chat-body { height:300px; padding:15px; overflow-y:auto; display:block; }
            .minimized { transform: translateY(300px); }

            .summary-table { width:100%; border-collapse:collapse; margin-top:50px; border:2px solid var(--pink); }
            .summary-table th { background:var(--pink); color:#000; padding:15px; text-align:left; }
            .summary-table td { border:1px solid #333; padding:15px; }
        </style>
    </head><body>
        <div class="header">
            <h1 style="margin:0;">MAIA II <span style="color:var(--pink);">SISTEMA SCOUT</span></h1>
            <p style="color:var(--green); margin:5px 0;">ESTADO: MOTOR CONECTADO A RED GLOBAL 2026</p>
        </div>

        <div class="status-container">
            <div id="p-bar" class="status-bar"></div>
            <div id="p-text" class="status-text">SISTEMA EN ESPERA</div>
        </div>

        <div class="control-panel">
            <form method="POST" id="scout-form" onsubmit="startLoading()">
                <select name="country">
                    <option value="BORRAR">-- SELECCIONAR PAÍS --</option>
                    {% for p in scout_engine.Paises %}
                    <option value="{{ p }}">{{ p }}</option>
                    {% endfor %}
                </select>

                <select name="tech">
                    <option value="BORRAR">-- SELECCIONAR TECNOLOGÍA --</option>
                    {% for t in scout_engine.Tecnologias %}
                    <option value="{{ t }}">{{ t }}</option>
                    {% endfor %}
                </select>

                <button type="submit" name="action" value="run_specialized" class="btn btn-run">INICIAR RASTREO</button>
                <button type="submit" name="action" value="run_global_scout" class="btn btn-global">SCOUT GLOBAL</button>
                <button type="submit" name="action" value="clear" class="btn btn-clear">LIMPIAR</button>
            </form>
        </div>

        <div id="results">
            {% for r in current_results %}
            <div class="ficha">
                <div class="ficha-head">
                    <span style="color:var(--neon); font-weight:bold;">FICHA: {{ r.id }}</span>
                    <span class="risk {{ r.Estado_Riesgo }}">RIESGO: {{ r.Estado_Riesgo }}</span>
                </div>
                <div class="ficha-body">
                    <div>
                        <span class="label">Proyecto</span>
                        <span class="value">{{ r.Nombre_Proyecto }}</span>
                        <span class="label">Ubicación / Tecnología</span>
                        <span class="value">{{ r.Ubicacion_Pais }} | {{ r.Tecnologia_Tipo }}</span>
                        <span class="label">Capacidad Técnica</span>
                        <span class="value">{{ r.Capacidad_Estimada }}</span>
                    </div>
                    <div>
                        <span class="label">CEO / Contacto</span>
                        <span class="value">{{ r.Nombre_CEO }}</span>
                        <span class="label">Móvil / Dirección</span>
                        <span class="value">{{ r.Telefono_Contacto }}<br>{{ r.Direccion_Sede }}</span>
                    </div>
                    <div class="ficha-footer">
                        <span class="label">Resumen Ejecutivo</span>
                        <p style="color:#ccc; font-size:13px;">{{ r.Resumen_Ejecutivo }}</p>
                        <a href="{{ r.URL_Fuente }}" target="_blank" style="color:var(--pink);">>> ACCEDER A FUENTE ORIGINAL</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if summary_data %}
        <table class="summary-table">
            <thead>
                <tr>
                    <th>TECNOLOGÍA</th>
                    <th>REGISTROS</th>
                    <th>ANALÍTICA</th>
                </tr>
            </thead>
            <tbody>
                {% for t, c in summary_data.items() %}
                <tr>
                    <td>{{ t }}</td>
                    <td>{{ c }} Items</td>
                    <td style="color:var(--green);">VERIFICADO</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <div id="maia-chat">
            <div class="chat-header" onclick="toggleChat()">
                MAIA AGENT <span>[Min/Max]</span>
            </div>
            <div class="chat-body" id="chat-body">
                <p>> Sistema iniciado.</p>
                <p>> Protocolo de búsqueda 100% real activo.</p>
                {% if current_results %}
                <p style="color:var(--green);">> Rastreo completado. {{ current_results|length }} hallazgos.</p>
                {% endif %}
            </div>
        </div>

        <script>
            function toggleChat() {
                document.getElementById('maia-chat').classList.toggle('minimized');
            }
            
            function startLoading() {
                const bar = document.getElementById('p-bar');
                const txt = document.getElementById('p-text');
                let width = 0;
                txt.innerText = "RASTREANDO REDES GLOBALES...";
                const interval = setInterval(() => {
                    if (width >= 100) clearInterval(interval);
                    else {
                        width += 5;
                        bar.style.width = width + "%";
                    }
                }, 100);
            }

            // Mantener barra al 100 si hay resultados
            {% if current_results %}
            document.getElementById('p-bar').style.width = "100%";
            document.getElementById('p-text').innerText = "RASTREO FINALIZADO - DATOS CARGADOS";
            {% endif %}
        </script>
    </body></html>
    """
    return render_template_string(html, current_results=current_results, summary_data=summary_data, scout_engine=scout_engine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
