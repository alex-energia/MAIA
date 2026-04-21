# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_dual_constructor_v7"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'projects' not in session: session['projects'] = [] # Memoria para el Constructor
    
    current_results = []
    view_mode = "scout" # Modo por defecto

    if request.method == 'POST':
        action = request.form.get('action')
        
        # Lógica del SCOUT
        if action == 'run_specialized':
            p, t = request.form.get('country'), request.form.get('tech')
            session['history'] = scout_engine.execute_brutal_search(p, t)
        elif action == 'run_global_scout':
            session['history'] = scout_engine.execute_brutal_search("", "", True)
        
        # Lógica del CONSTRUCTOR (NUEVO)
        elif action == 'open_builder':
            view_mode = "builder"
        
        elif action == 'create_project':
            new_p = {"name": request.form.get('p_name'), "status": "Draft"}
            session['projects'].append(new_p)
            view_mode = "builder"

        elif action == 'clear':
            session['history'] = []

        session.modified = True
        current_results = session['history']

    html = """
    <html><head>
        <title>MAIA II - DUAL CORE</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:20px; }
            .nav-top { display:flex; gap:20px; border-bottom:2px solid var(--pink); padding-bottom:10px; margin-bottom:20px; }
            .nav-btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; }
            .nav-btn.active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            .panel { background:#0a0a0a; border:1px solid var(--neon); padding:20px; margin-bottom:20px; }
            .btn { padding:10px; cursor:pointer; font-weight:bold; border:none; text-transform:uppercase; }
            .btn-scout { background:var(--green); color:#000; }
            .btn-builder { background:var(--pink); color:#000; }
            
            .ficha { border:1px solid #333; padding:15px; margin-bottom:15px; display:grid; grid-template-columns: 1fr 1fr; }
            
            /* CHAT FIX: Estado inicial cerrado */
            #maia-chat { position:fixed; bottom:0; right:20px; width:320px; border:2px solid var(--pink); background:#000; z-index:1000; transition:0.3s; }
            .chat-header { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; }
            .chat-content { height:250px; padding:15px; overflow-y:auto; display: block; }
            .is-minimized { transform: translateY(250px); }
        </style>
    </head><body>
        <div class="nav-top">
            <form method="POST" style="margin:0; display:flex; gap:10px;">
                <button type="submit" name="action" value="go_scout" class="nav-btn {{ 'active' if view_mode == 'scout' }}">SCOUT AGENT</button>
                <button type="submit" name="action" value="open_builder" class="nav-btn {{ 'active' if view_mode == 'builder' }}">BUILDER AGENT</button>
            </form>
        </div>

        {% if view_mode == 'scout' %}
        <div class="panel">
            <form method="POST">
                <select name="country" style="padding:10px; background:#000; color:#fff; border:1px solid var(--neon);">
                    {% for p in scout_engine.Paises %}<option value="{{ p }}">{{ p }}</option>{% endfor %}
                </select>
                <select name="tech" style="padding:10px; background:#000; color:#fff; border:1px solid var(--neon);">
                    {% for t in scout_engine.Tecnologias %}<option value="{{ t }}">{{ t }}</option>{% endfor %}
                </select>
                <button type="submit" name="action" value="run_specialized" class="btn btn-scout">RASTREAR</button>
                <button type="submit" name="action" value="run_global_scout" class="btn btn-builder">SCOUT GLOBAL</button>
            </form>
        </div>
        <div id="results">
            {% for r in session['history'] %}
            <div class="ficha">
                <div><strong>{{ r.Nombre_Proyecto }}</strong><br><small>{{ r.Ubicacion_Pais }}</small></div>
                <div>CEO: {{ r.Nombre_CEO }}<br>TEL: {{ r.Telefono_Contacto }}</div>
                <div style="grid-column: span 2; margin-top:10px; color:#ccc; border-top:1px solid #222;">{{ r.Resumen_Ejecutivo }}</div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="panel">
            <h2 style="color:var(--pink);">CONSTRUCTOR DE PROYECTOS</h2>
            <form method="POST">
                <input type="text" name="p_name" placeholder="Nombre del nuevo proyecto..." style="padding:10px; width:300px;">
                <button type="submit" name="action" value="create_project" class="btn btn-builder">CREAR PROYECTO</button>
            </form>
            <div style="margin-top:20px;">
                <h3>PROYECTOS EN DESARROLLO:</h3>
                {% for p in session['projects'] %}
                <div style="border:1px solid var(--pink); padding:10px; margin-bottom:5px;">{{ p.name }} - [{{ p.status }}]</div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <div id="maia-chat" class="is-minimized">
            <div class="chat-header" onclick="toggleChat()">MAIA AGENT [+/-]</div>
            <div class="chat-content">
                <p>> Modo Actual: {{ view_mode.upper() }}</p>
                <p>> Botones sincronizados con el backend.</p>
                <p>> Chat bloqueado para evitar saltos automáticos.</p>
            </div>
        </div>

        <script>
            function toggleChat() {
                const chat = document.getElementById('maia-chat');
                chat.classList.toggle('is-minimized');
            }
        </script>
    </body></html>
    """
    return render_template_string(html, scout_engine=scout_engine, view_mode=view_mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
