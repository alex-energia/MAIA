# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    scout_res = []
    fin_res = None
    active_tab = 'scout'

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'run_scout':
            scout_res = scout_engine.execute_brutal_search(request.form.get('c'), request.form.get('t'))
            active_tab = 'scout'
        elif action == 'run_finance':
            fin_res = builder_engine.process_model(request.form)
            active_tab = 'builder'

    return render_template_string(f"""
    <html><head>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .header {{ border-bottom:2px solid #f0f; padding-bottom:10px; margin-bottom:20px; }}
        .tab-content {{ display: {'block' if active_tab == 'scout' else 'none'}; }}
        .builder-content {{ display: {'block' if active_tab == 'builder' else 'none'}; }}
        .card {{ border:1px solid #0f0; padding:15px; margin:10px 0; background:rgba(0,40,0,0.1); }}
        input, select {{ background:#111; border:1px solid #0ff; color:#fff; padding:10px; width:100%; margin:5px 0; }}
        .btn {{ background:#f0f; color:#000; padding:12px; border:none; font-weight:bold; cursor:pointer; width:100%; }}
        
        /* CHAT MAXIMIZABLE/MINIMIZABLE */
        #maia-chat {{ position:fixed; bottom:20px; right:20px; width:350px; border:2px solid #0ff; background:#000; transition: 0.3s; }}
        .chat-header {{ background:#0ff; color:#000; padding:10px; cursor:pointer; font-weight:bold; }}
        .chat-body {{ height: 300px; padding:15px; display:block; }}
        .minimized {{ height: 40px !important; overflow:hidden; }}
    </style>
    <script>
        function toggleChat() {{ document.getElementById('maia-chat').classList.toggle('minimized'); }}
        function showTab(tab) {{ 
            document.getElementById('scout-ui').style.display = tab === 'scout' ? 'block' : 'none';
            document.getElementById('builder-ui').style.display = tab === 'builder' ? 'block' : 'none';
        }}
    </script>
    </head><body>
        <div class="header">
            <h1>MAIA II - COMMAND CENTER</h1>
            <button onclick="showTab('scout')" style="background:none; border:1px solid #0ff; color:#0ff; padding:5px 15px; cursor:pointer;">MOTOR SCOUT</button>
            <button onclick="showTab('builder')" style="background:none; border:1px solid #f0f; color:#f0f; padding:5px 15px; cursor:pointer;">+ CREAR PROYECTO NUEVO</button>
        </div>

        <div id="scout-ui" class="tab-content" style="display: {'block' if active_tab == 'scout' else 'none'};">
            <form method="post">
                <input name="c" placeholder="PAÍS (EJ: COLOMBIA)">
                <input name="t" placeholder="TECNOLOGÍA (EJ: HIDRÓGENO VERDE)">
                <button type="submit" name="action" value="run_scout" class="btn" style="background:#0f0;">EJECUTAR BÚSQUEDA BRUTAL</button>
            </form>
            {"".join([f'<div class="card"><b>{r["Nombre"]}</b><br>{r["Resumen"]}<br><small>CONTACTO: {r["Contacto"]}</small></div>' for r in scout_res])}
        </div>

        <div id="builder-ui" class="builder-content" style="display: {'block' if active_tab == 'builder' else 'none'};">
            <h2 style="color:#f0f;">FORMULARIO DE MODELO FINANCIERO</h2>
            <form method="post">
                <h3>Pestaña 1: CAPEX/OPEX</h3>
                <input name="capex" placeholder="CAPEX Total (USD)">
                <input name="opex" placeholder="OPEX Anual (USD)">
                <h3>Pestaña 2: Mercado e Ingresos</h3>
                <input name="ingresos" placeholder="Ingresos Anuales Estimados">
                <input name="trm" value="3900" placeholder="TRM Proyectada">
                
                <button type="submit" name="action" value="run_finance" class="btn">GENERAR MODELO FINANCIERO & MONTECARLO</button>
            </form>

            {f'''
            <div class="card" style="border-color:#f0f;">
                <h3>RESULTADOS DEL ANÁLISIS</h3>
                <p>VPN ESTIMADO: ${fin_res['vpn_base']:,.2f}</p>
                <p>PROBABILIDAD ÉXITO (MONTECARLO): {fin_res['montecarlo_exito']}%</p>
                <button class="btn" style="width:auto; background:#0ff;">GUARDAR EN MEMORIA</button>
            </div>
            ''' if fin_res else ''}
        </div>

        <div id="maia-chat" class="minimized">
            <div class="chat-header" onclick="toggleChat()">MAIA II AGENT [+/-]</div>
            <div class="chat-body">
                <p style="font-size:11px; color:#0f0;">Especialista en Energía y Finanzas activo.</p>
                <div style="height:180px; border-bottom:1px solid #333; margin-bottom:10px;">
                    MAIA: Lista para analizar el modelo Morrosquillo o buscar nuevos activos.
                </div>
                <input placeholder="Pregunta sobre TIR, VAN o SMR...">
            </div>
        </div>
    </body></html>
    """)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
