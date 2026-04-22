# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, session
from scout_engine import scout_engine
import os

app = Flask(__name__)
app.secret_key = "maia_biz_200"

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
        elif action == 'save':
            p_id = request.form.get('p_id')
            item = next((x for x in session['history'] if x['id'] == p_id), None)
            if item and item not in session['saved']:
                session['saved'].append(item); session.modified = True
        elif action == 'limpiar':
            session.clear(); return "<script>window.location='/';</script>"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>MAIA - NIVEL 200 (BUSINESS INTELLIGENCE)</title>
        <style>
            :root { --money: #00ff41; --gold: #ffd700; --bg: #000; }
            body { background:var(--bg); color:#fff; font-family: 'Segoe UI', sans-serif; margin:0; padding:20px; }
            .nav { display:flex; gap:15px; border-bottom:1px solid #222; padding-bottom:15px; }
            .btn { background:none; border:1px solid #444; color:#aaa; padding:10px 20px; cursor:pointer; font-size:11px; font-weight:bold; }
            .btn:hover { border-color:var(--money); color:var(--money); }
            .active { background:var(--money); color:#000; border-color:var(--money); box-shadow: 0 0 15px rgba(0,255,65,0.4); }
            
            .header { background:#0a0a0a; border:1px solid #1a1a1a; padding:20px; margin:20px 0; border-left: 5px solid var(--money); }
            
            .ficha { background:#0a0a0a; border:1px solid #1a1a1a; padding:30px; margin-top:25px; transition: 0.3s; }
            .ficha:hover { border-color: var(--money); }
            
            .biz-title { color: var(--money); font-size: 18px; margin-bottom: 15px; font-weight: 800; border-bottom: 1px solid #222; padding-bottom: 10px; }
            .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; font-size: 12px; }
            .label { color:#555; font-weight:bold; font-size: 10px; }
            .val { color:#ddd; }
            
            .resumen-box { background:#000; border:1px solid #222; padding:20px; color:#888; font-size:14px; margin-top: 15px; border-radius: 4px; }
            .action-row { margin-top: 20px; display: flex; gap: 15px; }

            #maia-chat { position:fixed; bottom:20px; right:20px; width:400px; border:1px solid #222; background:#000; z-index:1000; }
            .chat-h { background:#111; color:var(--money); padding:10px; font-weight:bold; cursor:pointer; display:flex; justify-content:space-between; font-size:11px; }
            #chat-b, #cInput { display:none; }
        </style>
    </head>
    <body>
        <div class="nav">
            <form method="POST" style="display:contents;">
                <button type="submit" name="view_state" value="scout" class="btn {{ 'active' if view == 'scout' }}">OPORTUNIDADES DE NEGOCIO 200</button>
                <button type="submit" name="view_state" value="memoria" class="btn {{ 'active' if view == 'memoria' }}">PIPELINE COMERCIAL ({{ session['saved']|length }})</button>
                <button type="submit" name="action" value="limpiar" class="btn" style="margin-left:auto; border-color:#ff0055; color:#ff0055;">WIPE</button>
            </form>
        </div>

        <div class="header">
            <strong>ESTADO:</strong> Búsqueda orientada a flujo de capital, licitaciones y contratos de suministro 2026.
        </div>

        {% if view == 'scout' %}
            <form method="POST">
                <input type="hidden" name="action" value="run_scout">
                <button type="submit" class="btn" style="width:100%; height:60px; border-color:var(--money); color:var(--money);">ESCANEAR CAPA COMERCIAL (RFPs Y CONTRATOS)</button>
            </form>

            {% for r in session['history'] %}
            <div class="ficha">
                <div class="biz-title">{{ r.nombre }}</div>
                <div class="grid">
                    <div><span class="label">PUNTO DE ACCESO</span><br><span class="val">{{ r.ceo }}</span></div>
                    <div><span class="label">ESTADO DEL NEGOCIO</span><br><span class="val">{{ r.riesgo }}</span></div>
                    <div><span class="label">VIGENCIA</span><br><span class="val">{{ r.fecha }}</span></div>
                </div>
                <div class="resumen-box">{{ r.resumen }}</div>
                <div class="action-row">
                    <a href="{{ r.fuente }}" target="_blank" class="btn" style="border-color:var(--gold); color:var(--gold);">[ VER PLIEGOS DE LICITACIÓN ]</a>
                    <form method="POST">
                        <input type="hidden" name="p_id" value="{{ r.id }}">
                        <button type="submit" name="action" value="save" class="btn" style="border-color:var(--money); color:var(--money);">AÑADIR A PIPELINE</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        {% endif %}

        <div id="maia-chat">
            <div class="chat-h" onclick="toggle()"><span>MAIA BUSINESS TERMINAL</span><span id="ico">[+]</span></div>
            <div id="chat-b" style="padding:15px; height:200px; overflow-y:auto; color:#444; font-size:12px;">
                <div>> Filtrando por "Request for Proposal" y "Subcontracting".</div>
            </div>
            <input type="text" id="cInput" placeholder="Comando..." onkeydown="if(event.key==='Enter') push()" style="width:100%; background:#000; border:none; color:var(--money); padding:12px; box-sizing:border-box; outline:none;">
        </div>

        <script>
            function toggle() {
                var b=document.getElementById('chat-b'); var i=document.getElementById('cInput'); var ico=document.getElementById('ico');
                if(b.style.display==='none' || b.style.display==='') { b.style.display='block'; i.style.display='block'; ico.innerText='[-]'; }
                else { b.style.display='none'; i.style.display='none'; ico.innerText='[+]'; }
            }
            function push() {
                var inp=document.getElementById('cInput'); var box=document.getElementById('chat-b');
                if(inp.value.trim()!="") { box.innerHTML += "<div> > "+inp.value+"</div>"; inp.value=""; box.scrollTop=box.scrollHeight; }
            }
        </script>
    </body></html>
    """
    return render_template_string(html, view=view, session=session)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)