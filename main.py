# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_scout_ultra_v5"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
    
    current_results = []
    summary_data = {}

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_specialized':
            pais = request.form.get('country')
            tech = request.form.get('tech')
            found = scout_engine.execute_brutal_search(pais, tech, is_global=False)
            session['history'] = found
            session.modified = True
            current_results = found
            
        elif action == 'run_global_scout':
            found = scout_engine.execute_brutal_search("", "", is_global=True)
            session['history'] = found
            session.modified = True
            current_results = found
            
        elif action == 'clear':
            session['history'] = []
            session.modified = True
            current_results = []

    if not current_results:
        current_results = session.get('history', [])

    if current_results:
        summary_data = scout_engine.generate_summary_table(current_results)

    html = """
    <html><head>
        <title>MAIA II - SCOUT CONTROL PANEL</title>
        <style>
            body { background:#050505; color:#0ff; font-family:'Segoe UI', monospace; padding:40px; }
            .header-main { border-left: 10px solid #f0f; padding-left:20px; margin-bottom:40px; }
            
            .control-panel { background:#111; border:1px solid #0ff; padding:30px; margin-bottom:40px; display:flex; gap:15px; align-items:center; }
            select { background:#000; border:1px solid #0ff; color:#fff; padding:12px; width:250px; font-family:monospace; }
            
            .btn { padding:12px 25px; font-weight:bold; cursor:pointer; text-transform:uppercase; border:none; font-family:monospace; }
            .btn-run { background:#0f0; color:#000; }
            .btn-scout { background:#f0f; color:#000; }
            .btn-clear { background:#333; color:#eee; }

            .ficha-proyecto { background:#0a0a0a; border:1px solid #333; margin-bottom:30px; padding:0; border-radius:4px; overflow:hidden; }
            .ficha-header { background:#1a1a1a; padding:15px 25px; display:flex; justify-content:space-between; border-bottom:1px solid #333; }
            .ficha-body { padding:25px; display:grid; grid-template-columns: 1fr 1fr; gap:20px; }
            .ficha-full { grid-column: span 2; border-top: 1px solid #222; padding-top:15px; }
            
            .label { color:#f0f; font-size:11px; text-transform:uppercase; display:block; margin-bottom:4px; }
            .value { color:#fff; font-size:15px; margin-bottom:15px; display:block; }
            
            .tag-riesgo { padding:4px 12px; font-weight:bold; border:1px solid; }
            .ALTO { border-color:#f00; color:#f00; background:rgba(255,0,0,0.1); }
            .MODERADO { border-color:#ff0; color:#ff0; background:rgba(255,255,0,0.1); }
            .BAJO { border-color:#0f0; color:#0f0; background:rgba(0,255,0,0.1); }

            .resumen-final { width:100%; border-collapse:collapse; margin-top:50px; background:#111; border:1px solid #f0f; }
            .resumen-final th { background:#f0f; color:#000; padding:15px; text-align:left; }
            .resumen-final td { border:1px solid #333; padding:15px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:350px; background:#000; border:1px solid #f0f; z-index:999; }
            .chat-head { background:#f0f; color:#000; padding:10px; font-weight:bold; cursor:pointer; }
            .chat-content { height:250px; padding:15px; font-size:13px; }
        </style>
    </head><body>
        <div class="header-main">
            <h1 style="margin:0; font-size:35px; letter-spacing:2px;">MAIA II <span style="color:#f0f;">SCOUT ENGINE</span></h1>
            <p style="color:#0f0; margin:5px 0;">SISTEMA DE RASTREO DE OPORTUNIDADES AMÉRICA - EUROPA - ASIA - ARABIA</p>
        </div>

        <div class="control-panel">
            <form method="POST" style="display:flex; gap:15px; width:100%;">
                <select name="country">
                    <option value="BORRAR">-- FILTRAR PAÍS/ZONA --</option>
                    {% for p in scout_engine.Paises %}
                    <option value="{{ p }}">{{ p }}</option>
                    {% endfor %}
                </select>

                <select name="tech">
                    <option value="BORRAR">-- FILTRAR TECNOLOGÍA --</option>
                    {% for t in scout_engine.Tecnologias %}
                    <option value="{{ t }}">{{ t }}</option>
                    {% endfor %}
                </select>

                <button type="submit" name="action" value="run_specialized" class="btn btn-run">INICIAR RASTREO</button>
                <button type="submit" name="action" value="run_global_scout" class="btn btn-scout">SCOUT GLOBAL</button>
                <button type="submit" name="action" value="clear" class="btn btn-clear">LIMPIAR</button>
            </form>
        </div>

        <div id="fichas-container">
            {% for r in current_results %}
            <div class="ficha-proyecto">
                <div class="ficha-header">
                    <span style="color:#0ff; font-weight:bold;">ID: {{ r.id }}</span>
                    <span class="tag-riesgo {{ r.Estado_Riesgo }}">RIESGO: {{ r.Estado_Riesgo }}</span>
                </div>
                <div class="ficha-body">
                    <div>
                        <span class="label">Nombre del Proyecto</span>
                        <span class="value">{{ r.Nombre_Proyecto }}</span>
                        
                        <span class="label">Ubicación</span>
                        <span class="value">{{ r.Ubicacion_Pais }}</span>
                        
                        <span class="label">Tecnología</span>
                        <span class="value">{{ r.Tecnologia_Tipo }}</span>
                    </div>
                    <div>
                        <span class="label">CEO / Líder de Proyecto</span>
                        <span class="value">{{ r.Nombre_CEO }}</span>
                        
                        <span class="label">Contacto Directo</span>
                        <span class="value">{{ r.Telefono_Contacto }}</span>
                        
                        <span class="label">Dirección Primaria</span>
                        <span class="value">{{ r.Direccion_Sede }}</span>
                    </div>
                    <div class="ficha-full">
                        <span class="label">Resumen Ejecutivo y Descripción Técnica</span>
                        <p style="color:#ccc; font-size:14px; line-height:1.6;">{{ r.Resumen_Ejecutivo }}</p>
                        
                        <span class="label">Fuente Original</span>
                        <a href="{{ r.URL_Fuente }}" target="_blank" style="color:#f0f; font-size:13px;">{{ r.URL_Fuente }}</a>
                        
                        <p style="text-align:right; font-size:10px; color:#555; margin-top:15px;">RASTREADO: {{ r.Fecha_Rastreo }}</p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        {% if summary_data %}
        <div style="margin-top:60px;">
            <h2 style="color:#f0f; border-bottom:1px solid #f0f; padding-bottom:10px;">RESUMEN DE INTELIGENCIA DE MERCADO</h2>
            <table class="resumen-final">
                <thead>
                    <tr>
                        <th>TECNOLOGÍA IDENTIFICADA</th>
                        <th>CANTIDAD DE PROYECTOS</th>
                        <th>ESTADO DE BASE DE DATOS</th>
                    </tr>
                </thead>
                <tbody>
                    {% for tech, count in summary_data.items() %}
                    <tr>
                        <td>{{ tech }}</td>
                        <td>{{ count }} PROYECTOS ENCONTRADOS</td>
                        <td style="color:#0f0;">ACTUALIZADO 2026</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}

        <div id="maia-chat">
            <div class="chat-head">MAIA II AGENT</div>
            <div class="chat-content">
                <p style="color:#0f0;">> Módulos de países actualizados.</p>
                <p style="color:#0f0;">> Motor de búsqueda sincronizado con DuckDuckGo API.</p>
                {% if current_results %}
                <p style="color:#f0f;">> Hallazgos: {{ current_results|length }} proyectos listos para análisis financiero.</p>
                {% endif %}
            </div>
        </div>
    </body></html>
    """
    return render_template_string(html, current_results=current_results, summary_data=summary_data, scout_engine=scout_engine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
