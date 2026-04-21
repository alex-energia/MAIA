# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_full_cycle_scout_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    if 'attempt' not in session: session['attempt'] = False
    
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            session['history'] = scout_engine.execute_global_scout()
            session['attempt'] = True
            session.modified = True
            view = 'scout'
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item: 
                session['saved'].append(item)
                session.modified = True
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>MAIA - BUSINESS SCOUT</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; padding-bottom:120px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            #st-cont { width:100%; height:8px; background:#111; margin:15px 0; display:none; border:1px solid #333; }
            #st-bar { height:100%; background:var(--green); width:0%; transition:0.3s; }
            .alert { border: 1px solid red; color: red; padding: 20px; text-align: center; margin-top: 20px; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--neon); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; margin:15px 0; border-top:1px solid #222; padding-top:10px; }
            .label { color:var(--pink); font-size:9px; display:block; }
            #maia-chat { position:fixed; bottom:0; right:20px; width:300px; border:2px solid var(--pink); background:#000; z-index:9999; }
            .chat-h { background:var(--pink); color:#000; padding:8px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { height:150px; padding:10px; overflow-y:auto; font-size:11px; color:var(--green); border-top:1px solid var(--pink); }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">MAIA SCOUT</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">LIMPIAR</button>
            </form>
        </div>
        <div id="st-cont"><div id="st-bar"></div></div>
        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="go()" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green);">SINCRONIZAR NEGOCIOS: DISEÑO | EJECUCIÓN | ACCIONES</button>
            </form>
            {% if session['attempt'] and not session['history'] %}
                <div class="alert">NO SE DETECTARON NEGOCIOS VIGENTES EN EL CICLO DE 30 DÍAS.</div>
            {% endif %}
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID NEGOCIO</span>{{ r.id }}</div>
                    <div><span class="label">PUNTO DE CONTACTO</span>{{ r.ceo }}</div>
                    <div><span class="label">STATUS BANCARIO</span>{{ r.riesgo }}</div>
                    <div><span class="label">MÓVIL</span>{{ r.movil }}</div>
                    <div><span class="label">E-MAIL</span>{{ r.email }}</div>
                    <div><span class="label">FECHA DETECCIÓN</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:15px; border:1px solid #222;">
                    <span class="label">OPORTUNIDAD DETECTADA</span>
                    <p style="color:#ccc; font-size:12px;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink);">[VER DOCUMENTACIÓN REAL]</a>
                </div>
                <form method="POST" style="margin-top:10px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:10px;">GUARDAR EN MEMORIA</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}
        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA CORE</span><span id="ico">[-]</span></div>
            <div id="chat-b">
                > Sincronización: 360° (Diseño a Venta).<br>
                > Ramas: Hidro, Solar, Viento, SMR, Geotermia, H2.<br>
                > Vigencia: Últimos 30 días.<br>
                > Filtro: Licitaciones Públicas y Privadas.
            </div>
        </div>
        <script>
            function toggle() {
                var b = document.getElementById('chat-b');
                var i = document.getElementById('ico');
                if(b.style.display=='none') { b.style.display='block'; i.innerText='[-]'; }
                else { b.style.display='none'; i.innerText='[+]'; }
            }
            function go() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var i=setInterval(function(){ w+=10; b.style.width=w+'%'; if(w>=100){ clearInterval(i); document.getElementById('scoutF').submit(); }}, 100);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
