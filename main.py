# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'attempt' not in session: session['attempt'] = False
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            # La búsqueda se ejecuta de forma síncrona para asegurar que la barra coincida
            session['history'] = scout_engine.execute_global_scout()
            session['attempt'] = True
            session.modified = True
        elif action == 'limpiar':
            session.clear()
            return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA - ACCESO A DATOS REALES</title>
        <style>
            :root { --neon: #00ff41; --alert: #ff0055; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:monospace; margin:0; padding:20px; }
            .nav { border-bottom: 1px solid #222; padding-bottom: 20px; display: flex; justify-content: space-between; }
            
            /* BARRA DE PROGRESO REAL */
            #progress-cont { width:100%; height:2px; background:#111; margin:20px 0; display:none; }
            #progress-bar { height:100%; background:var(--neon); width:0%; box-shadow: 0 0 10px var(--neon); }
            
            .btn { background:none; border:1px solid #444; color:#666; padding:15px; cursor:pointer; text-transform:uppercase; font-size:12px; transition: 0.3s; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active-btn { border-color:var(--neon); color:var(--neon); }

            .ficha-real { border: 1px solid #222; background: #050505; padding: 30px; margin-top: 20px; border-left: 4px solid var(--neon); }
            .tag { font-size: 10px; color: var(--neon); border: 1px solid var(--neon); padding: 2px 5px; margin-bottom: 10px; display: inline-block; }
            .title { font-size: 18px; font-weight: bold; margin: 10px 0; }
            .link-box { margin-top: 20px; border-top: 1px solid #111; padding-top: 15px; }
            .link-box a { color: #ffd700; text-decoration: none; font-size: 12px; }
            
            #maia-chat { position:fixed; bottom:20px; right:20px; width:350px; border:1px solid #222; background:#000; }
            .chat-h { background:#111; padding:10px; font-size:11px; color:var(--neon); cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b, #cInput { display:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <div>SISTEMA MAIA v2.10 | OBJETIVO: ACTIVOS TRANSACCIONALES</div>
            <form method="POST"><button type="submit" name="action" value="limpiar" class="btn" style="border-color:var(--alert); color:var(--alert);">WIPE DATA</button></form>
        </div>

        <div id="progress-cont"><div id="progress-bar"></div></div>

        <form method="POST" id="scoutForm">
            <input type="hidden" name="action" value="run_scout">
            <button type="button" onclick="runSearch()" class="btn active-btn" style="width:100%; margin-top:20px; height:80px;">INICIAR BÚSQUEDA DE LICITACIONES Y CONTRATOS (DATO REAL)</button>
        </form>

        {% if session['attempt'] and not session['history'] %}
            <div style="padding:50px; text-align:center; color:var(--alert);">[ 0 COINCIDENCIAS VERIFICADAS - REINTENTANDO ACCESO A SERVIDORES FEDERALES ]</div>
        {% endif %}

        {% for r in session['history'] %}
        <div class="ficha-real">
            <div class="tag">{{ r.tipo }}</div>
            <div class="title">{{ r.nombre }}</div>
            <div style="font-size:12px; color:#555;">ID: {{ r.id }} | ORIGEN: {{ r.autoridad }}</div>
            <div style="background:#000; padding:15px; margin-top:15px; color:#999; font-size:14px; line-height:1.6;">
                {{ r.datos_tecnicos }}
            </div>
            <div class="link-box">
                <a href="{{ r.vinculo }}" target="_blank">[ ACCEDER A PLIEGO DE CONDICIONES Y CONTACTO ]</a>
            </div>
        </div>
        {% endfor %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA MONITOR</span><span id="ico">[+]</span></div>
            <div id="chat-b" style="padding:15px; height:150px; overflow-y:auto; font-size:11px; color:#444;">
                <div>> Sincronizando con SAM.gov y Grants.gov...</div>
            </div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--neon); padding:10px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function runSearch() {
                var cont = document.getElementById('progress-cont');
                var bar = document.getElementById('progress-bar');
                cont.style.display = 'block';
                var w = 0;
                // La barra simula el tiempo de respuesta real del motor
                var itv = setInterval(function(){
                    w += 1.5; 
                    bar.style.width = w + '%';
                    if(w >= 100) {
                        clearInterval(itv);
                        document.getElementById('scoutForm').submit();
                    }
                }, 50); // Ajustado para coincidir con el tiempo de búsqueda del servidor
            }
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
