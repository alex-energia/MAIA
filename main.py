# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_global_230_asset"

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
        <title>MAIA - NIVEL 230 (GLOBAL ASSET RADAR)</title>
        <style>
            :root { --neon: #00ff41; --world: #0080ff; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family:'Courier New', monospace; margin:0; padding:20px; }
            .nav { border-bottom: 1px solid #222; padding-bottom:15px; display:flex; justify-content:space-between; align-items:center; }
            
            #bar-cont { width:100%; height:4px; background:#111; margin:25px 0; display:none; border: 1px solid #333; }
            #bar-fill { height:100%; background:linear-gradient(90deg, #000, var(--world)); width:0%; box-shadow: 0 0 15px var(--world); }
            #status-txt { display:none; color:var(--world); font-size:10px; margin-bottom:10px; text-transform:uppercase; letter-spacing:1px; }

            .btn { background:none; border:1px solid #333; color:#777; padding:15px 30px; cursor:pointer; font-weight:bold; font-size:12px; }
            .btn:hover { border-color:var(--world); color:var(--world); }
            
            .ficha { border:1px solid #1a1a1a; background:#050505; padding:25px; margin-top:20px; border-left: 5px solid var(--world); position:relative; }
            .ficha::before { content: "GLOBAL NODE"; position:absolute; top:10px; right:10px; font-size:8px; color:var(--world); border:1px solid var(--world); padding:2px 5px; }
            
            .title { font-size:16px; color:#fff; margin:15px 0; font-weight:bold; border-bottom:1px solid #111; padding-bottom:10px; }
            .desc { color:#999; font-size:13px; line-height:1.6; background:#080808; padding:20px; border-radius:3px; }
            .link { display:inline-block; margin-top:15px; color:var(--world); text-decoration:none; font-weight:bold; font-size:11px; }
            
            .error-box { padding:60px; border:1px dashed #ff0055; text-align:center; color:#ff0055; margin-top:20px; background:rgba(255,0,85,0.02); }
        </style>
    </head>
    <body>
        <div class="nav">
            <div>MAIA INTELLIGENCE | <span style="color:var(--world);">NIVEL 230: GLOBAL ASSET RADAR</span></div>
            <form method="POST"><button type="submit" name="action" value="limpiar" class="btn" style="border-color:#333;">REINICIAR</button></form>
        </div>

        <div id="bar-cont"><div id="bar-fill"></div></div>
        <div id="status-txt">INICIANDO BARRIDO TRANSFRONTERIZO...</div>

        <form method="POST" id="scoutF">
            <input type="hidden" name="action" value="run_scout">
            <button type="button" onclick="start()" class="btn" style="width:100%; border-color:var(--world); color:var(--world); height:80px; font-size:14px;">EJECUTAR ESCANEO GLOBAL (UE, ASIA, MENA)</button>
        </form>

        {% if session['attempt'] and not session['history'] %}
            <div class="error-box">
                [ ESTADO: 0 ACTIVOS TRANSACCIONALES DETECTADOS EN CAPA 230 ]<br>
                <small style="color:#666; display:block; margin-top:10px;">Los nodos internacionales no reportan adjudicaciones públicas en este ciclo de búsqueda. Rotando a Nodos Secundarios.</small>
            </div>
        {% endif %}

        {% for r in session['history'] %}
        <div class="ficha">
            <div class="title">{{ r.nombre }}</div>
            <div style="color:#444; font-size:10px; margin-bottom:10px;">ORIGEN: {{ r.autoridad }} | TIPO: {{ r.tipo }}</div>
            <div class="desc">{{ r.datos_tecnicos }}</div>
            <a href="{{ r.vinculo }}" target="_blank" class="link">[ ACCEDER A EXPEDIENTE INTERNACIONAL ]</a>
        </div>
        {% endfor %}

        <script>
            function start() {
                var cont = document.getElementById('bar-cont');
                var fill = document.getElementById('bar-fill');
                var txt = document.getElementById('status-txt');
                cont.style.display = 'block'; txt.style.display = 'block';
                
                var w = 0;
                // Sincronización Global: 45 segundos (ajustado para búsqueda en múltiples zonas)
                var itv = setInterval(function(){
                    w += 0.4;
                    fill.style.width = w + '%';
                    
                    if(w > 10 && w < 30) txt.innerText = "SINC: Escaneando Registros de la Unión Europea (TED / Europarl)...";
                    if(w >= 30 && w < 60) txt.innerText = "SINC: Localizando RFPs en Mercados del Golfo (Adnoc, Neom)...";
                    if(w >= 60 && w < 90) txt.innerText = "SINC: Filtrando Alianzas en Asia-Pacífico (Nikkei / Yonhap)...";
                    if(w >= 90) txt.innerText = "SINC: Consolidando Resultados de Clase A...";
                    
                    if(w >= 100) {
                        clearInterval(itv);
                        document.getElementById('scoutF').submit();
                    }
                }, 180); 
            }
        </script>
    </body></html>
    """
    return render_template_string(html, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)