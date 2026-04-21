# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_v3_production_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicialización de Memoria
    if 'history' not in session:
        session['history'] = []
    
    results = []
    summary_data = {}

    if request.method == 'POST':
        # Capturamos la acción del botón pulsado
        action = request.form.get('action')
        
        if action == 'run_specialized':
            # Obtener datos de los Dropdowns
            pais_seleccionado = request.form.get('country')
            tech_seleccionada = request.form.get('tech')
            
            # Solo buscar si no es la opción de borrar
            if pais_seleccionado == "BORRAR" or tech_seleccionada == "BORRAR":
                session['history'] = []
            else:
                results = scout_engine.execute_brutal_search(pais_seleccionado, tech_seleccionada, is_global=False)
                session['history'] = results
            
            session.modified = True
            
        elif action == 'run_global_scout':
            # Botón SCOUT: Rastreo total en todos los países/tecnologías
            results = scout_engine.execute_brutal_search("", "", is_global=True)
            session['history'] = results
            session.modified = True
            
        elif action == 'clear':
            # Botón Limpiar Memoria
            session['history'] = []
            session.modified = True
            results = []

    # Recuperación de datos para renderizar la vista
    display_results = results if results else session.get('history', [])
    if display_results:
        summary_data = scout_engine.generate_summary_table(display_results)

    # HTML con CSS integrado para asegurar que no dependa de archivos externos
    html = """
    <html><head>
        <title>MAIA II - SCOUT PRO</title>
        <style>
            body { background:#000; color:#0ff; font-family:'Courier New', monospace; padding:30px; line-height:1.4; }
            .header { border-bottom:3px solid #f0f; padding-bottom:20px; margin-bottom:30px; display:flex; justify-content:space-between; align-items:center; }
            
            .search-box { background:#111; border:2px solid #0ff; padding:30px; margin-bottom:40px; box-shadow: 0 0 15px rgba(0,255,255,0.2); }
            
            select, .btn { padding:15px; font-weight:bold; border:none; text-transform:uppercase; font-family:monospace; font-size:14px; }
            select { background:#000; border:1px solid #0ff; color:#fff; width:22%; margin-right:15px; cursor:pointer; }
            
            .btn-special { background:#0f0; color:#000; cursor:pointer; margin-right:10px; border:1px solid #0f0; }
            .btn-special:hover { background:#000; color:#0f0; }
            
            .btn-global { background:#f0f; color:#000; cursor:pointer; margin-right:10px; border:1px solid #f0f; }
            .btn-global:hover { background:#000; color:#f0f; }
            
            .btn-clear { background:#444; color:#fff; cursor:pointer; border:1px solid #fff; }
            
            .card { border:1px solid #0f0; padding:25px; margin-bottom:25px; background:rgba(0,40,0,0.1); position:relative; }
            .risk-tag { position:absolute; top:20px; right:20px; padding:8px 15px; font-weight:bold; border:2px solid; font-size:14px; }
            .risk-ALTO { border-color:#f00; color:#f00; background:rgba(255,0,0,0.1); }
            .risk-MODERADO { border-color:#ff0; color:#ff0; background:rgba(255,255,0,0.1); }
            .risk-BAJO { border-color:#0f0; color:#0f0; background:rgba(0,255,0,0.1); }

            .summary-table { width:100%; border:3px solid #f0f; margin-top:40px; border-collapse:collapse; background:rgba(255,0,255,0.05); }
            .summary-table th { background:#f0f; color:#000; padding:15px; text-align:left; font-size:16px; }
            .summary-table td { border:1px solid #f0f; padding:15px; font-size:15px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:2px solid #f0f; background:#000; z-index:1000; box-shadow: -5px -5px 20px rgba(240,0,240,0.3); }
            .chat-header { background:#f0f; color:#000; padding:15px; cursor:pointer; font-weight:bold; display:flex; justify-content:space-between; }
            .chat-body { height:350px; padding:20px; display:block; }
            .minimized { height:50px !important; overflow:hidden; border-color:#0ff !important; }
            .minimized .chat-header { background:#0ff; }
        </style>
        <script>
            function toggleChat() { document.getElementById('maia-chat').classList.toggle('minimized'); }
            setInterval(() => { 
                const now = new Date();
                document.getElementById('clock').innerText = now.toLocaleString(); 
            }, 1000);
        </script>
    </head><body>
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:32px; letter-spacing:3px;">MAIA II <span style="color:#f0f;">SCOUT COMMAND</span></h1>
                <p style="color:#0f0; margin:5px 0 0 0;">ESTADO: LISTO PARA RASTREO MULTI-ZONA</p>
            </div>
            <div style="text-align:right;">
                <div id="clock" style="font-size:20px; color:#f0f; font-weight:bold;"></div>
                <small>PROYECTOS EN CACHÉ: {{ session['history']|length }}</small>
            </div>
        </div>

        <div class="search-box">
            <form method="post">
                <select name="country" required>
                    <option value="" disabled selected>ZONA GEOGRÁFICA</option>
                    <option value="BORRAR">-- BORRAR SELECCIÓN --</option>
                    {% for p in scout_engine.Paises %}
                    <option value="{{ p }}">{{ p }}</option>
                    {% endfor %}
                </select>

                <select name="tech" required>
                    <option value="" disabled selected>TECNOLOGÍA</option>
                    <option value="BORRAR">-- BORRAR SELECCIÓN --</option>
                    {% for t in scout_engine.Tecnologias %}
                    <option value="{{ t }}">{{ t }}</option>
                    {% endfor %}
                </select>

                <button type="submit" name="action" value="run_specialized" class="btn btn-special">INICIAR RASTREO ESPECIAL</button>
                <button type="submit" name="action" value="run_global_scout" class="btn btn-global">SCOUT (GLOBAL)</button>
                <button type="submit" name="action" value="clear" class="btn btn-clear">LIMPIAR</button>
            </form>
        </div>

        <div id="results">
            {% for r in display_results %}
            <div class="card">
                <div class="risk-tag risk-{{ r.Riesgo }}">RIESGO: {{ r.Riesgo }}</div>
                <h3 style="margin:0 0 15px 0; color:#0ff; font-size:20px;">{{ r.Nombre }}</h3>
                <p style="color:#888; font-size:12px; border-bottom:1px solid #333; padding-bottom:10px;">
                    FECHA: {{ r.Fecha_Rastreo }} | ZONA: {{ r.Ubicación }} | TEC: {{ r.Tecnología }}
                </p>
                <p style="font-size:15px; color:#e0e0e0;">{{ r.Resumen }}</p>
                <div style="background:rgba(0,255,255,0.05); padding:15px; margin-top:20px; border-left:5px solid #0ff;">
                    <b>DATOS DE CONTACTO:</b> <a href="{{ r.Contacto }}" target="_blank" style="color:#f0f; text-decoration:none;">ACCEDER A LA FUENTE REAL</a>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if summary_data %}
        <table class="summary-table">
            <thead>
                <tr>
                    <th>TECNOLOGÍA O TIPO</th>
                    <th>PROYECTOS ENCONTRADOS</th>
                    <th>VERIFICACIÓN</th>
                </tr>
            </thead>
            <tbody>
                {% for tech, count in summary_data.items() %}
                <tr>
                    <td>{{ tech }}</td>
                    <td>{{ count }} Proyectos detectados</td>
                    <td style="color:#0f0;">DATOS 100% EXTERNOS</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        <div id="maia-chat" class="minimized">
            <div class="chat-header" onclick="toggleChat()">MAIA ECONOMIST AGENT <span>[MAXIMIZAR]</span></div>
            <div class="chat-body">
                <div style="height:270px; overflow-y:auto; font-size:14px; border-bottom:1px solid #333; color:#fff;">
                    <p style="color:#0f0;">> PROTOCOLO DE BLINDAJE ACTIVADO.</p>
                    <p>> Sistema de búsqueda real listo.</p>
                    {% if display_results %}
                    <p>> Análisis de {{ display_results|length }} hilos completado.</p>
                    {% endif %}
                </div>
                <input type="text" placeholder="Escribe aquí para consultar a Maia..." style="width:100%; margin-top:15px; background:#000; border:1px solid #0ff; color:#fff; padding:12px;">
            </div>
        </div>
    </body></html>
    """
    # Pasamos el motor al template para que pueda leer las listas Paises y Tecnologias
    return render_template_string(html, display_results=display_results, summary_data=summary_data, scout_engine=scout_engine)

if __name__ == '__main__':
    # Puerto dinámico para despliegue en la nube
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))