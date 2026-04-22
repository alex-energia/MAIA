# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_bruteforce_120"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    if 'attempt' not in session: session['attempt'] = False
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            # EJECUCIÓN DE FUERZA BRUTA 120
            session['history'] = scout_engine.execute_global_scout()
            session['attempt'] = True
            session.modified = True
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
        <meta charset="UTF-8">
        <title>MAIA - NIVEL 120 (BRUTEFORCE)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --pure-white: #ffffff; --alert: #ff0055; }
            body { background:#000; color:var(--pure-white); font-family:'Courier New', monospace; margin:0; padding:20px; }
            .nav { display:flex; gap:10px; border-bottom:1px solid #222; padding-bottom:15px; }
            .btn { background:none; border:1px solid #333; color:#888; padding:10px 20px; cursor:pointer; font-weight:bold; text-transform:uppercase; transition:0.2s; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active { background:var(--neon); color:#000; border-color:var(--neon); box-shadow: 0 0 15px var(--neon); }
            
            #st-cont { width:100%; height:4px; background:#111; margin:20px 0; display:none; border: 1px solid #222; }
            #st-bar { height:100%; background:var(--neon); width:0%; transition:0.01s; }

            .ficha { background:#0a0a0a; border:1px solid #222; padding:30px; margin-top:20px; border-top: 3px solid var(--neon); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin:20px 0; }
            .label { color:var(--neon); font-size:10px; display:block; opacity:0.6; margin-bottom:5px; }
            
            .status-box { padding: 40px; text-align: center; border: 1px solid var(--alert); color: var(--alert); margin-top: 20px; font-size: 14px; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">SCANNER BRUTEFORCE 120</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">PORTAFOLIO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto; border-color:var(--alert); color:var(--alert);">WIPE DATA</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; height:70px; border-color:var(--gold); color:var(--gold); font-size:16px;">FORZAR INFILTRACIÓN EN DOMINIOS DE AUTORIDAD (.GOV / .ORG / .PDF)</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="status-box">
                    [ ALERTA: CORTAFUEGOS DE RED DETECTADO ]<br>
                    <small style="color:#666">Los servidores de búsqueda están bloqueando el acceso profundo. Intenta de nuevo en 30 segundos o cambia de Nodo.</small>
                </div>
            {% endif %}
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; font-size:18px;">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID ORIGEN</span>{{ r.id }}</div>
                    <div><span class="label">ENTIDAD DETECTADA</span>{{ r.ceo }}</div>
                    <div><span class="label">RIESGO ACTIVO</span>{{ r.riesgo }}</div>
                    <div><span class="label">TIPO DOC</span>{{ r.movil }}</div>
                    <div><span class="label">INTEL E-MAIL</span>{{ r.email }}</div>
                    <div><span class="label">VIGENCIA</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#000; padding:15px; border:1px solid #111; color:#999; font-size:12px; line-height:1.6;">
                    {{ r.resumen }}
                    <br><br>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--neon); text-decoration:none;">[ ABRIR REGISTRO DE AUTORIDAD ]</a>
                </div>
                <form method="POST" style="margin-top:15px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:10px; border-color:var(--gold); color:var(--gold);">GURDAR ACTIVO</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <script>
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ 
                    w+=1; b.style.width=w+'%'; 
                    if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }
                }, 25);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
