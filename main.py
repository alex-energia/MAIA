# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_scout_v24_strict"

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
        elif action == 'limpiar':
            session.clear()
            return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA - SCOUT</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; padding:20px; }
            .nav { display:flex; gap:15px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            #st-cont { width:100%; height:8px; background:#111; margin:15px 0; display:none; border:1px solid #333; }
            #st-bar { height:100%; background:var(--green); width:0%; transition:0.3s; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--neon); }
            .grid-ficha { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin-bottom:15px; }
            .label { color:var(--pink); font-size:10px; display:block; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">SCOUT ENERGÍA</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">LIMPIAR</button>
            </form>
        </div>
        <div id="st-cont"><div id="st-bar"></div></div>
        {% if view == 'scout' %}
            <form method="POST" onsubmit="start()"><button type="submit" name="action" value="run_scout" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green);">EJECUTAR SCOUT 2026</button></form>
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid-ficha">
                    <div><span class="label">ID</span>{{ r.id }}</div>
                    <div><span class="label">CEO</span>{{ r.ceo }}</div>
                    <div><span class="label">RIESGO</span>{{ r.riesgo }}</div>
                    <div><span class="label">MÓVIL</span>{{ r.movil }}</div>
                    <div><span class="label">EMAIL</span>{{ r.email }}</div>
                    <div><span class="label">DETECCIÓN</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:15px; border:1px solid #222;">
                    <span class="label">RESUMEN EJECUTIVO</span>
                    <p style="color:#ccc; font-size:13px;">{{ r.resumen_ejecutivo }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[FUENTE REAL]</a>
                </div>
                <form method="POST" style="margin-top:15px;"><input type="hidden" name="p_id" value="{{ r.id }}"><button type="submit" name="action" value="save" class="btn">GUARDAR EN MEMORIA</button></form>
            </div>
            {% endfor %}
        {% elif view == 'memoria' %}
            {% for m in session['saved'] %}<div class="ficha"><h3>{{ m.nombre }}</h3><p>{{ m.resumen_ejecutivo }}</p></div>{% endfor %}
        {% endif %}
        <script>
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var i=setInterval(function(){ w+=5; if(w<=100) b.style.width=w+'%'; else clearInterval(i); }, 100);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)