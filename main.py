# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_scout_final_v23"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.execute_global_scout()
            session.modified = True
            view = 'scout'
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item)
                session.modified = True
            view = 'scout'
        elif action == 'limpiar':
            session.clear()
            return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA II - SCOUT ENERGÍA</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; }
            .nav { display:flex; gap:15px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            #st-cont { width:100%; height:6px; background:#111; margin-top:15px; display:none; border:1px solid #333; }
            #st-bar { height:100%; background:var(--green); width:0%; transition:0.3s; }

            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--neon); }
            .grid-ficha { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin:20px 0; border-top:1px solid #222; padding-top:15px; }
            .label { color:var(--pink); font-size:10px; display:block; margin-bottom:5px; }
            
            #maia-chat { position:fixed; bottom:0; right:20px; width:320px; border:2px solid var(--pink); background:#000; }
            .chat-h { background:var(--pink); color:#000; padding:10px; font-weight:bold; cursor:pointer; }
            #chat-b { height:180px; padding:15px; overflow-y:auto; font-size:11px; color:var(--green); }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">1. SCOUT ENERGÍA</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">2. MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">LIMPIAR</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" onsubmit="start()">
                <button type="submit" name="action" value="run_scout" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green);">EJECUTAR RASTREO ENERGÍAS AVANZADAS 2026</button>
            </form>
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid-ficha">
                    <div><span class="label">ID NEGOCIO</span>{{ r.id }}</div>
                    <div><span class="label">CEO / RESPONSABLE</span>{{ r.ceo }}</div>
                    <div><span class="label">RIESGO PROYECTO</span>{{ r.riesgo }}</div>
                    <div><span class="label">MÓVIL</span>{{ r.movil }}</div>
                    <div><span class="label">EMAIL</span>{{ r.email }}</div>
                    <div><span class="label">DETECCION</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:20px; border:1px solid #222;">
                    <span class="label">RESUMEN DE NEGOCIO</span>
                    <p style="color:#ccc; font-size:13px; line-height:1.6; margin:10px 0;">{{ r.resumen_ejecutivo }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink); font-size:11px;">[ACCEDER A LA FUENTE REAL]</a>
                </div>
                <form method="POST" style="margin-top:20px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:11px;">GUARDAR EN MEMORIA</button>
                </form>
            </div>
            {% endfor %}

        {% elif view == 'memoria' %}
            <h2 style="color:var(--pink);">MEMORIA DE NEGOCIOS</h2>
            {% for m in session['saved'] %}
                <div class="ficha"><h3>{{ m.nombre }}</h3><p>{{ m.resumen_ejecutivo }}</p></div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()">MAIA II CORE [-]</div>
            <div id="chat-b">
                > Filtro de Energía Avanzada Activo.<br>
                > Barra de estado reestablecida.<br>
                > Botones Memoria/Limpiar funcionales.<br>
                > Sin placeholders. Información real.
            </div>
        </div>

        <script>
            function toggle() { document.getElementById('chat-b').style.display = (document.getElementById('chat-b').style.display == 'none') ? 'block' : 'none'; }
            function start() {
                document.getElementById('st-cont').style.display = 'block';
                var bar = document.getElementById('st-bar');
                var w = 0;
                var int = setInterval(function(){ w += 5; if(w <= 100) bar.style.width = w + '%'; else clearInterval(int); }, 100);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
