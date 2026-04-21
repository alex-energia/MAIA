# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine

app = Flask(__name__)
app.secret_key = "maia_expert_level_v28"

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
        <title>MAIA CORE - NIVEL EXPERTO</title>
        <style>
            :root { --neon: #0ff; --pink: #f0f; --green: #0f0; }
            body { background:#000; color:var(--neon); font-family:monospace; margin:0; padding:20px; padding-bottom:180px; }
            .nav { display:flex; gap:10px; border-bottom:2px solid var(--pink); padding-bottom:15px; }
            .btn { background:none; border:1px solid var(--neon); color:var(--neon); padding:10px 20px; cursor:pointer; font-weight:bold; }
            .active { background:var(--pink); color:#000; border-color:var(--pink); }
            
            #st-cont { width:100%; height:10px; background:#111; margin:15px 0; display:none; border:1px solid #333; }
            #st-bar { height:100%; background:var(--green); width:0%; transition:0.3s; }

            .alert-null { border: 2px solid red; background: rgba(255,0,0,0.1); color: red; padding: 30px; text-align: center; margin-top: 20px; font-weight: bold; }
            .ficha { background:#0a0a0a; border:1px solid #333; padding:25px; margin-top:20px; border-left:5px solid var(--neon); box-shadow: 0 0 10px rgba(0,255,255,0.1); }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin:15px 0; border-top:1px solid #222; padding-top:15px; }
            .label { color:var(--pink); font-size:10px; display:block; letter-spacing:1px; }
            
            /* CHAT FLOTANTE RECONSTRUIDO - SIN TEXTO PREVIO */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:350px; border:2px solid var(--pink); background:#000; z-index:10000; }
            .chat-h { background:var(--pink); color:#000; padding:10px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { display:block; height:250px; padding:10px; overflow-y:auto; font-size:12px; color:var(--green); }
            .chat-input { width:100%; background:#111; border:none; border-top:2px solid var(--pink); color:var(--green); padding:15px; box-sizing: border-box; font-family:monospace; font-size:14px; outline:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">BÚSQUEDA EXHAUSTIVA</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">MEMORIA ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="border-color:red; color:red; margin-left:auto;">REINICIAR SISTEMA</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutForm">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="goScout()" class="btn" style="width:100%; margin-top:20px; border-color:var(--green); color:var(--green); height:60px; font-size:16px;">SINCRONIZAR RADAR GLOBAL (AMÉRICA-EUROPA-ASIA-GOLFO)</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div class="alert-null">MAIA INFORMA: NO SE HAN ENCONTRADO OPORTUNIDADES VIGENTES QUE CUMPLAN LOS REQUISITOS EN LOS ÚLTIMOS 30 DÍAS.</div>
            {% endif %}
            
            {% for r in session['history'] %}
            <div class="ficha">
                <h2 style="margin:0; color:#fff; letter-spacing:1px;">{{ r.nombre }}</h2>
                <div class="grid">
                    <div><span class="label">ID PROYECTO</span>{{ r.id }}</div>
                    <div><span class="label">RESPONSABLE</span>{{ r.ceo }}</div>
                    <div><span class="label">EVALUACIÓN COMERCIAL</span>{{ r.riesgo }}</div>
                    <div><span class="label">MÓVIL</span>{{ r.movil }}</div>
                    <div><span class="label">EMAIL</span>{{ r.email }}</div>
                    <div><span class="label">DETECCIÓN</span>{{ r.fecha }}</div>
                </div>
                <div style="background:#111; padding:20px; border:1px solid #222;">
                    <span class="label">ANÁLISIS TÉCNICO-FINANCIERO</span>
                    <p style="color:#ccc; font-size:13px; line-height:1.6;">{{ r.resumen }}</p>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--pink); font-weight:bold; text-decoration:none;">[ACCEDER A FUENTE ORIGINAL]</a>
                </div>
                <form method="POST" style="margin-top:15px;">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn" style="font-size:11px; padding:5px 15px;">GUARDAR EN MEMORIA</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggleChat()"><span>MAIA CORE V28</span><span id="c-ico">[-]</span></div>
            <div id="chat-b"></div>
            <input type="text" class="chat-input" id="cInput" placeholder="Esperando comando..." onkeydown="if(event.key==='Enter') executeCmd()">
        </div>

        <script>
            function toggleChat() {
                var b = document.getElementById('chat-b');
                var i = document.getElementById('cInput');
                var ico = document.getElementById('c-ico');
                if(b.style.display=='none') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function executeCmd() {
                var input = document.getElementById('cInput');
                var box = document.getElementById('chat-b');
                if(input.value.trim() !== "") {
                    box.innerHTML += "<div style='margin-bottom:10px; color:var(--pink);'>> " + input.value + "</div>";
                    input.value = "";
                    box.scrollTop = box.scrollHeight;
                }
            }
            function goScout() {
                document.getElementById('st-cont').style.display='block';
                var bar = document.getElementById('st-bar'); var w = 0;
                var int = setInterval(function(){ w += 5; bar.style.width = w + '%'; if(w>=100){ clearInterval(int); document.getElementById('scoutForm').submit(); }}, 150);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
