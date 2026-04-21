# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_scout_pro_v25"

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
        <title>MAIA - SCOUT ENERGÍA</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            #st-cont { width:100%; height:8px; background:#111; margin:15px 0; display:none; border:1px solid #333; }
            #st-bar { height:100%; background:var(--green); width:0%; }

            .resumen-global { background: rgba(0,255,255,0.05); border: 1px dashed var(--neon); padding: 20px; margin: 20px 0; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--neon); }
            .grid-ficha { display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:20px; margin:20px 0; border-top:1px solid #222; padding-top:15px; }
            .label { color:var(--pink); font-size:10px; display:block; margin-bottom:5px; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">SCOUT</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">LIMPIAR</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutForm">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="executeScout()" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green);">EJECUTAR RASTREO REAL 2026</button>
            </form>

            {% if session['history'] %}
            <div class="resumen-global">
                <h3 style="margin:0; color:var(--pink);">RESUMEN DE INTELIGENCIA MAIA</h3>
                <p style="font-size:13px; color:#fff;">
                    Se han detectado {{ session['history']|length }} oportunidades críticas en los sectores de energía avanzada (SMR, H2 Verde y Neutrino) con proyecciones de cierre para el ciclo 2026. Los datos provienen de fuentes de mercado activas.
                </p>
            </div>
            {% endif %}
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff;">{{ r.nombre }}</h2>
                <div class="grid-ficha">
                    <div><span class="label">ID PROYECTO</span>{{ r.id }}</div>
                    <div><span class="label">CEO / RESPONSABLE</span>{{ r.ceo }}</div>
                    <div><span class="label">RIESGO</span>{{ r.riesgo }}</div>
                    <div><span class="label">MÓVIL</span>{{ r.movil }}</div>
                    <div><span class="label">EMAIL</span>{{ r.email }}</div>
                    <div><span class="label">FECHA DETECCIÓN</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:20px; border:1px solid #222;">
                    <span class="label">ANÁLISIS DE LA OPORTUNIDAD</span>
                    <p style="color:#ccc; font-size:13px; line-height:1.6; margin:10px 0;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink); font-size:11px;">[VER FUENTE ORIGINAL]</a>
                </div>
                <form method="POST" style="margin-top:20px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:11px;">GUARDAR EN MEMORIA</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <script>
            function executeScout() {
                document.getElementById('st-cont').style.display = 'block';
                var bar = document.getElementById('st-bar');
                var w = 0;
                var int = setInterval(function(){ 
                    w += 10; 
                    bar.style.width = w + '%';
                    if(w >= 100) {
                        clearInterval(int);
                        document.getElementById('scoutForm').submit();
                    }
                }, 80);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
