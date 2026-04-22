# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_octa_pillar_250"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session: session['history'] = []
    if 'attempt' not in session: session['attempt'] = False

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
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
        <title>MAIA - NIVEL 250: OCTA-ASSET RADAR</title>
        <style>
            :root { 
                --electric-blue: #00E5FF; 
                --cyber-gold: #FFD600; 
                --deep-bg: #050505;
                --status-green: #39FF14;
            }
            body { background:var(--deep-bg); color:#fff; font-family:'Consolas', monospace; margin:0; padding:20px; }
            
            .nav { border-bottom: 2px solid #1a1a1a; padding-bottom:15px; display:flex; justify-content:space-between; align-items:center; }
            .status-indicator { color: var(--status-green); font-size: 10px; letter-spacing: 1px; }

            /* BARRA DE PROGRESO DE ALTA PRECISIÓN */
            #bar-cont { width:100%; height:10px; background:#111; margin:30px 0; display:none; border: 1px solid #333; box-shadow: inset 0 0 10px #000; }
            #bar-fill { height:100%; background: linear-gradient(90deg, var(--electric-blue), var(--cyber-gold)); width:0%; box-shadow: 0 0 20px rgba(0,229,255,0.4); }
            #status-txt { display:none; color:var(--electric-blue); font-size:11px; margin-bottom:10px; font-weight: bold; }

            .btn-scan { 
                background: #000; border: 2px solid var(--cyber-gold); color: var(--cyber-gold); 
                padding: 25px; width: 100%; cursor: pointer; font-weight: bold; font-size: 16px;
                transition: 0.3s; text-transform: uppercase;
            }
            .btn-scan:hover { background: var(--cyber-gold); color: #000; box-shadow: 0 0 40px var(--cyber-gold); }
            
            .ficha { 
                background: #0d0d0d; border: 1px solid #222; border-top: 4px solid var(--electric-blue); 
                padding: 30px; margin-top: 25px; transition: 0.3s;
            }
            .ficha:hover { border-color: var(--cyber-gold); transform: translateY(-2px); }
            
            .title { font-size: 18px; color: var(--electric-blue); margin-bottom: 15px; font-weight: bold; }
            .desc { color: #888; font-size: 14px; line-height: 1.6; background: #000; padding: 20px; border-radius: 2px; }
            
            .link-btn { 
                display: inline-block; margin-top: 20px; color: var(--cyber-gold); 
                text-decoration: none; border: 1px solid var(--cyber-gold); padding: 10px 20px; font-size: 11px;
            }

            /* CHAT SIEMPRE PRESENTE */
            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid #333; background:#000; box-shadow: 0 0 30px rgba(0,0,0,0.9); }
            .chat-h { background:#111; color:var(--electric-blue); padding:15px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; }
            #chat-b { height:200px; padding:20px; overflow-y:auto; font-size:12px; color:#555; border-bottom: 1px solid #111; }
            #cInput { width:100%; background:#050505; border:none; color:var(--status-green); padding:15px; box-sizing:border-box; outline:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <div style="font-weight:bold; color:var(--cyber-gold);">MAIA OCTA-PILLAR v2.50</div>
            <div class="status-indicator">MODO: INFILTRACIÓN ESTRICTA EN 8 EJES</div>
        </div>

        <div id="bar-cont"><div id="bar-fill"></div></div>
        <div id="status-txt">SISTEMA EN ESPERA...</div>

        <form method="POST" id="scoutF">
            <input type="hidden" name="action" value="run_scout">
            <button type="button" onclick="start()" class="btn-scan">EJECUTAR BARRIDO DE LOS 8 PILARES ESTRATÉGICOS</button>
        </form>

        {% if session['attempt'] and not session['history'] %}
            <div style="padding:100px; text-align:center; color:#ff0055; border: 1px dashed #ff0055; margin-top:20px;">
                [ ERROR: CERO RESULTADOS EN LOS 8 PILARES ]<br>
                <small style="color:#444;">Los nodos globales están rechazando la firma. Intentando rotación de sub-nodos...</small>
            </div>
        {% endif %}

        {% for r in session['history'] %}
        <div class="ficha">
            <div class="title">{{ r.nombre }}</div>
            <div style="font-size:10px; color:#444; margin-bottom:10px;">ID: {{ r.id }} | TIPO: {{ r.categoria }}</div>
            <div class="desc">{{ r.datos }}</div>
            <a href="{{ r.vinculo }}" target="_blank" class="link-btn">[ ANALIZAR OPORTUNIDAD ]</a>
        </div>
        {% endfor %}

        <div id="maia-chat">
            <div class="chat-h"><span>MAIA COMMAND CENTER</span><span>[LIVE]</span></div>
            <div id="chat-b">
                <div style="color:var(--electric-blue)">> Filtro: Hidro, Solar, SMR, Térmica, Geo, Neutrino, H2, Startups.</div>
                <div style="color:#333;">> Nivel 250 sincronizado.</div>
            </div>
            <input type="text" id="cInput" placeholder="Enviar instrucción..." onkeydown="if(event.key==='Enter') push()">
        </div>

        <script>
            function start() {
                var cont = document.getElementById('bar-cont');
                var fill = document.getElementById('bar-fill');
                var txt = document.getElementById('status-txt');
                cont.style.display = 'block'; txt.style.display = 'block';
                
                var w = 0;
                // Sincronización real de 8 pilares: 80 segundos (10s por pilar para evitar bloqueos)
                var itv = setInterval(function(){
                    w += 0.25; 
                    fill.style.width = w + '%';
                    
                    if(w < 12.5) txt.innerText = "PILAR 1/8: ESCANEANDO ADJUDICACIONES HIDROELÉCTRICAS...";
                    if(w >= 12.5 && w < 25) txt.innerText = "PILAR 2/8: LOCALIZANDO MEGA-PLANTAS SOLARES (UTILITY SCALE)...";
                    if(w >= 25 && w < 37.5) txt.innerText = "PILAR 3/8: RASTREANDO EMPLAZAMIENTOS SMR NUCLEAR...";
                    if(w >= 37.5 && w < 50) txt.innerText = "PILAR 4/8: ANALIZANDO CONTRATOS DE PLANTAS TÉRMICAS...";
                    if(w >= 50 && w < 62.5) txt.innerText = "PILAR 5/8: DETECTANDO PERFORACIONES GEOTÉRMICAS...";
                    if(w >= 62.5 && w < 75) txt.innerText = "PILAR 6/8: BUSCANDO NODOS DE ENERGÍA NEUTRINO...";
                    if(w >= 75 && w < 87.5) txt.innerText = "PILAR 7/8: FILTRANDO PROYECTOS FID DE HIDRÓGENO...";
                    if(w >= 87.5) txt.innerText = "PILAR 8/8: IDENTIFICANDO STARTUPS DE TECNOLOGÍA ENERGÉTICA...";
                    
                    if(w >= 100) {
                        clearInterval(itv);
                        document.getElementById('scoutF').submit();
                    }
                }, 200); 
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { 
                    box.innerHTML += "<div style='color:var(--status-green); margin-top:5px;'> > "+inp.value+"</div>"; 
                    inp.value=""; box.scrollTop=box.scrollHeight; 
                }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)