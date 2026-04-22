# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Clave robusta para persistencia de sesión

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicialización de persistencia
    if 'history' not in session: session['history'] = []
    if 'saved' not in session: session['saved'] = []
    if 'attempt' not in session: session['attempt'] = False
    
    view = request.form.get('view_state', 'scout')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'run_scout':
            # Ejecutar motor de infiltración profunda
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MAIA - NIVEL 130 (BLACK BOX INTELLIGENCE)</title>
        <style>
            :root { --neon: #0ff; --gold: #ffd700; --pure-white: #ffffff; --alert: #ff0055; --bg-ficha: #0a0a0a; }
            body { background:#000; color:var(--pure-white); font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin:0; padding:20px; }
            
            .nav { display:flex; gap:12px; border-bottom:1px solid #222; padding-bottom:20px; align-items: center; }
            .btn { background:none; border:1px solid #444; color:#aaa; padding:12px 24px; cursor:pointer; font-weight:bold; text-transform:uppercase; transition:0.2s; font-size:11px; letter-spacing: 1px; }
            .btn:hover { border-color:var(--neon); color:var(--neon); }
            .active { background:var(--neon); color:#000; border-color:var(--neon); box-shadow: 0 0 15px rgba(0,255,255,0.4); }
            
            #st-cont { width:100%; height:4px; background:#111; margin:20px 0; display:none; border-radius: 2px; overflow: hidden; }
            #st-bar { height:100%; background:var(--neon); width:0%; transition:0.01s; }

            /* TITULO DE ACTIVO RESALTADO */
            .asset-title { color: var(--neon); text-transform: uppercase; letter-spacing: 2px; font-size: 22px; border-left: 5px solid var(--neon); padding-left: 15px; margin: 0 0 25px 0; font-weight: 800; text-shadow: 0 0 10px rgba(0,255,255,0.3); }
            
            .ficha { background:var(--bg-ficha); border:1px solid #1a1a1a; padding:40px; margin-top:30px; border-radius: 8px; position: relative; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:25px; margin:25px 0; border-top: 1px solid #222; padding-top: 25px; }
            .label { color:var(--neon); font-size:10px; display:block; opacity:0.7; margin-bottom:6px; font-weight: bold; text-transform: uppercase; }
            .val { font-size: 14px; color: #fff; font-family: 'Courier New', monospace; }

            /* CAJA DE RESUMEN TÉCNICO */
            .resumen-box { background:#000; border:1px solid #333; padding:30px; color:#ccc; font-size:15px; line-height:1.8; position:relative; margin-top: 25px; border-radius: 4px; }
            .resumen-box::before { content: "INFORME TÉCNICO DE CAMPO"; position: absolute; top: -11px; left: 20px; background: #000; padding: 0 12px; font-size: 10px; color: var(--gold); font-weight: bold; letter-spacing: 1px; }
            
            /* CHAT TERMINAL */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:450px; border:1px solid #222; background:#000; z-index:10000; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
            .chat-h { background:#111; color:var(--neon); padding:15px; font-weight:bold; cursor:pointer; font-size:11px; display:flex; justify-content:space-between; border-bottom: 1px solid #222; }
            #chat-b { display:block; height:280px; padding:20px; overflow-y:auto; font-size:13px; color:#777; border-bottom: 1px solid #111; font-family: 'Courier New', monospace; }
            #cInput { width:100%; background:#000; border:none; color:var(--neon); padding:18px; box-sizing: border-box; outline:none; font-family: monospace; }

            .btn-save { border-color: var(--gold); color: var(--gold); margin-top: 15px; }
            .btn-save:hover { background: var(--gold); color: #000; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">SCANNER DE ACTIVOS</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">PORTAFOLIO ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto; border-color:var(--alert); color:var(--alert);">WIPE SYSTEM</button>
            </form>
        </div>

        <div id="st-cont"><div id="st-bar"></div></div>

        {% if view == 'scout' %}
            <form method="POST" id="scoutF">
                <input type="hidden" name="action" value="run_scout">
                <button type="button" onclick="start()" class="btn" style="width:100%; margin-top:20px; height:80px; border-color:var(--neon); color:var(--neon); font-size:16px;">EJECUTAR INFILTRACIÓN PROFUNDA (NODOS DE CAPITAL Y REGISTRO RED)</button>
            </form>

            {% if session['attempt'] and not session['history'] %}
                <div style="text-align:center; padding:100px; color:#444; text-transform:uppercase; letter-spacing:2px;">
                    [ 0 COINCIDENCIAS - CORTAFUEGOS ACTIVO ]
                </div>
            {% endif %}

            {% for r in session['history'] %}
            <div class="ficha">
                <h1 class="asset-title">{{ r.nombre }}</h1>
                
                <div class="grid">
                    <div><span class="label">ID INFILTRACIÓN</span><span class="val">{{ r.id }}</span></div>
                    <div><span class="label">ENTIDAD DETECTADA</span><span class="val">{{ r.ceo }}</span></div>
                    <div><span class="label">RIESGO ACTIVO</span><span class="val">{{ r.riesgo }}</span></div>
                    <div><span class="label">TIPO DOCUMENTO</span><span class="val">{{ r.movil }}</span></div>
                    <div><span class="label">VIGENCIA</span><span class="val">{{ r.fecha }}</span></div>
                    <div><span class="label">ESTADO RED</span><span class="val">Detectado</span></div>
                </div>

                <div class="resumen-box">
                    {{ r.resumen }}
                    <br><br>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--gold); text-decoration:none; font-weight:bold; font-size:13px; border: 1px solid var(--gold); padding: 5px 10px;">[ ABRIR REGISTRO DE AUTORIDAD ]</a>
                </div>

                <form method="POST">
                    <input type="hidden" name="p_id" value="{{ r.id }}">
                    <button type="submit" name="action" value="save" class="btn btn-save">GUARDAR EN PORTAFOLIO ESTRATÉGICO</button>
                </form>
            </div>
            {% endfor %}
        {% endif %}

        {% if view == 'memoria' %}
            <h2 style="color:var(--gold); margin-top:30px;">ACTIVOS EN PORTAFOLIO</h2>
            {% for r in session['saved'] %}
                <div class="ficha" style="border-left: 4px solid var(--gold);">
                    <h1 class="asset-title" style="color:var(--gold); border-color:var(--gold);">{{ r.nombre }}</h1>
                    <div class="resumen-box">{{ r.resumen }}</div>
                    <a href="{{ r.fuente }}" target="_blank" style="color:var(--gold); display:block; margin-top:15px;">Acceder al archivo</a>
                </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA DEEP TERMINAL V.130</span><span id="ico">[-]</span></div>
            <div id="chat-b">
                <div style="color:var(--gold); margin-bottom:10px;">> Terminal iniciada.</div>
                <div style="color:#555;">> Escaneo de activos reales en curso...</div>
            </div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()">
        </div>

        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { 
                    box.innerHTML += "<div style='margin-bottom:10px; color:var(--neon);'> > "+inp.value+"</div>"; 
                    inp.value=""; box.scrollTop=box.scrollHeight; 
                }
            }
            function start() {
                document.getElementById('st-cont').style.display='block';
                var b=document.getElementById('st-bar'); var w=0;
                var itv=setInterval(function(){ 
                    w+=2; b.style.width=w+'%'; 
                    if(w>=100){ clearInterval(itv); document.getElementById('scoutF').submit(); }
                }, 30);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
