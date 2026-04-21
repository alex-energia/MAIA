# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_shield_v8_final"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'builder_list' not in session: session['builder_list'] = []
    
    view = session.get('view', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_global':
            session['history'] = scout_engine.execute_global_scout()
            session['view'] = 'scout'
        elif action == 'switch_builder':
            session['view'] = 'builder'
        elif action == 'switch_scout':
            session['view'] = 'scout'
        elif action == 'add_to_builder':
            new_prj = {"id": request.form.get('id'), "name": request.form.get('name')}
            session['builder_list'].append(new_prj)
        elif action == 'clear':
            session['history'] = []
            session['builder_list'] = []

        session.modified = True
        return render_template_string(HTML_TEMPLATE, view=session['view'])

    return render_template_string(HTML_TEMPLATE, view=view)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html><head>
    <title>MAIA II - GLOBAL CORE</title>
    <style>
        :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
        body { background:#000; color:var(--neon); font-family:monospace; padding:30px; margin:0; }
        .top-nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; margin-bottom:25px; }
        
        .btn { padding:12px 20px; cursor:pointer; font-weight:bold; border:none; text-transform:uppercase; font-family:monospace; }
        .btn-main { background:var(--pink); color:#000; }
        .btn-nav { background:transparent; border:1px solid var(--neon); color:var(--neon); }
        .btn-nav.active { background:var(--neon); color:#000; }
        
        /* Barra de Estado */
        .loading-bar-container { width:100%; height:10px; background:#111; border:1px solid var(--neon); margin-bottom:20px; display:none; }
        .loading-bar { height:100%; background:var(--green); width:0%; }

        .ficha { background:#0a0a0a; border:1px solid #333; margin-bottom:20px; padding:20px; display:grid; grid-template-columns: 1fr 1fr; gap:20px; }
        .full-width { grid-column: span 2; border-top: 1px solid #222; padding-top:15px; }
        .label { color:var(--pink); font-size:10px; display:block; }
        .value { color:#fff; display:block; margin-bottom:10px; }

        /* Chat Maia: Blindado */
        #maia-chat { position:fixed; bottom:0; right:20px; width:300px; border:2px solid var(--pink); background:#000; z-index:9999; }
        .chat-head { background:var(--pink); color:#000; padding:10px; cursor:pointer; font-weight:bold; text-align:center; }
        .chat-body { height:200px; padding:15px; display:none; overflow-y:auto; border-top:1px solid var(--pink); }
    </style>
</head><body>
    <div class="top-nav">
        <form method="POST">
            <button type="submit" name="action" value="switch_scout" class="btn btn-nav {{ 'active' if view == 'scout' }}">SCOUT GLOBAL</button>
            <button type="submit" name="action" value="switch_builder" class="btn btn-nav {{ 'active' if view == 'builder' }}">CONSTRUCTOR</button>
        </form>
    </div>

    <div class="loading-bar-container" id="l-container"><div class="loading-bar" id="l-bar"></div></div>

    {% if view == 'scout' %}
    <form method="POST" onsubmit="showLoading()">
        <button type="submit" name="action" value="run_global" class="btn btn-main" style="width:100%; margin-bottom:30px;">EJECUTAR RASTREO GLOBAL 2026</button>
    </form>
    
    <div id="scout-results">
        {% for r in session['history'] %}
        <div class="ficha">
            <div>
                <span class="label">ID PROYECTO</span><span class="value">{{ r.id }}</span>
                <span class="label">NOMBRE</span><span class="value">{{ r.Nombre_Proyecto }}</span>
                <span class="label">TECNOLOGÍA</span><span class="value">{{ r.Tecnologia }}</span>
            </div>
            <div>
                <span class="label">CEO / CONTACTO</span><span class="value">{{ r.CEO_Director }}</span>
                <span class="label">TELÉFONO / DIRECCIÓN</span><span class="value">{{ r.Contacto_Directo }}<br>{{ r.Direccion_Sede }}</span>
            </div>
            <div class="full-width">
                <span class="label">EXTRACTO TÉCNICO COMPLETO</span>
                <p style="color:#ccc; font-size:12px;">{{ r.Resumen_Completo }}</p>
                <a href="{{ r.Enlace }}" target="_blank" style="color:var(--neon);">[IR A FUENTE]</a>
                <form method="POST" style="margin-top:10px;">
                    <input type="hidden" name="id" value="{{ r.id }}">
                    <input type="hidden" name="name" value="{{ r.Nombre_Proyecto }}">
                    <button type="submit" name="action" value="add_to_builder" class="btn" style="background:var(--green); font-size:10px; color:#000;">+ ENVIAR A CONSTRUCTOR</button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>

    {% else %}
    <div style="background:#0a0a0a; padding:30px; border:1px solid var(--pink);">
        <h2 style="color:var(--pink);">MÓDULO CONSTRUCTOR (PROYECTOS SELECCIONADOS)</h2>
        {% if not session['builder_list'] %}
            <p>No hay proyectos en la mesa de construcción. Usa el Scout para añadir proyectos.</p>
        {% else %}
            {% for p in session['builder_list'] %}
            <div style="border:1px solid var(--green); padding:10px; margin-bottom:10px;">
                <strong>{{ p.name }}</strong> (ID: {{ p.id }}) - <span style="color:var(--green);">[LISTO PARA DESARROLLO]</span>
            </div>
            {% endfor %}
        {% endif %}
    </div>
    {% endif %}

    <div id="maia-chat">
        <div class="chat-head" onclick="toggleChat()">MAIA AGENT [VER LOG]</div>
        <div class="chat-body" id="c-body">
            <p>> Sistema estable.</p>
            <p>> Modo: {{ view|upper }}</p>
            <p>> Scout Global cargado al 100%.</p>
        </div>
    </div>

    <script>
        function toggleChat() {
            var body = document.getElementById('c-body');
            body.style.display = (body.style.display === 'block') ? 'none' : 'block';
        }
        function showLoading() {
            document.getElementById('l-container').style.display = 'block';
            var bar = document.getElementById('l-bar');
            var w = 0;
            var interval = setInterval(function() {
                if (w >= 100) clearInterval(interval);
                else { w += 10; bar.style.width = w + '%'; }
            }, 200);
        }
    </script>
</body></html>
"""