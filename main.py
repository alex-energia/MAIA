# main.py - CONSOLA MAIA II (BLINDAJE NIVEL 7)
from flask import Flask, render_template_string, request
from scout_engine import scout_core
from builder_engine import builder_core

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def maia_console():
    scout_results = []
    financial_results = None
    
    # Manejo de acciones sin alterar el estado del otro motor
    if request.form.get('action') == 'exec_scout':
        scout_results = scout_core.execute_brutal_search(request.form.get('c'), request.form.get('t'))
    
    if request.form.get('action') == 'exec_builder':
        financial_results = builder_core.run_montecarlo(
            float(request.form.get('capex', 0)), 
            float(request.form.get('opex', 0)), 
            float(request.form.get('ppa', 0))
        )

    return render_template_string(f"""
    <html><head>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; margin:0; display:flex; }}
        .sidebar {{ width:300px; border-right:2px solid #f0f; padding:20px; height:100vh; }}
        .main-content {{ flex-grow:1; padding:30px; overflow-y:auto; }}
        .card {{ border:1px solid #0f0; background:rgba(0,50,0,0.1); padding:15px; margin-bottom:15px; }}
        .tab-btn {{ background:none; border:1px solid #f0f; color:#f0f; padding:10px; cursor:pointer; width:100%; margin-bottom:10px; }}
        .chat-float {{ position:fixed; bottom:20px; right:20px; width:350px; border:2px solid #0ff; background:#111; }}
        input {{ background:#000; border:1px solid #0ff; color:#fff; width:100%; padding:8px; margin:5px 0; }}
        .metric {{ color:#f0f; font-size:20px; font-weight:bold; }}
    </style>
    </head><body>
        <div class="sidebar">
            <h2 style="color:#f0f;">MAIA II CONTROL</h2>
            <button class="tab-btn" onclick="document.getElementById('scout-ui').style.display='block';">MOTOR SCOUT</button>
            <button class="tab-btn" onclick="document.getElementById('builder-ui').style.display='block';">BUILDER FINANCIERO</button>
            <hr style="border-color:#333;">
            <div style="font-size:10px; color:#555;">SISTEMA DE BLINDAJE NIVEL 7 ACTIVO</div>
        </div>

        <div class="main-content">
            <div id="scout-ui">
                <h1 style="color:#0f0;">SCOUT ENGINE [OPERATIVO]</h1>
                <form method="post">
                    <input name="c" placeholder="PAÍS / REGIÓN">
                    <input name="t" placeholder="TECNOLOGÍA (SMR, H2, SOLAR...)">
                    <button type="submit" name="action" value="exec_scout" style="background:#0f0; color:#000; width:100%; border:none; padding:10px; font-weight:bold; cursor:pointer;">EJECUTAR BÚSQUEDA BRUTAL</button>
                </form>
                {"".join([f'<div class="card"><b>{r["Nombre"]}</b><br>{r["Resumen"]}<br><small>{r.get("Contacto","")}</small></div>' for r in scout_results])}
            </div>

            <div id="builder-ui" style="margin-top:50px; border-top:2px solid #f0f; padding-top:20px;">
                <h1 style="color:#f0f;">PROJECT BUILDER [MORROSQUILLO MODEL]</h1>
                <form method="post">
                    <h3>CAPEX & OPEX</h3>
                    <input name="capex" placeholder="Inversión Inicial (CAPEX)">
                    <input name="opex" placeholder="Costo Operativo (OPEX)">
                    <h3>MERCADO</h3>
                    <input name="ppa" placeholder="Precio PPA (kWh)">
                    <button type="submit" name="action" value="exec_builder" style="background:#f0f; color:#000; width:100%; border:none; padding:10px; font-weight:bold; cursor:pointer;">CALCULAR VIABILIDAD & MONTECARLO</button>
                </form>

                {f'''
                <div class="card" style="border-color:#f0f;">
                    <h3 style="color:#f0f;">ANÁLISIS DE SENSIBILIDAD MONTECARLO</h3>
                    <div class="metric">ÉXITO: {financial_results['success_rate']}%</div>
                    <p>VPN MÁX: ${financial_results['max_vpn']:,.2f} | VPN MÍN: ${financial_results['min_vpn']:,.2f}</p>
                    <button class="tab-btn" style="width:auto; padding:5px 20px;">GUARDAR EN MEMORIA</button>
                </div>
                ''' if financial_results else ''}
            </div>
        </div>

        <div class="chat-float">
            <div style="background:#0ff; color:#000; padding:10px; font-weight:bold;">MAIA ECONOMIST AGENT</div>
            <div style="padding:15px; font-size:12px;">Analizando modelo Granja Solar vs Mercado SMR...</div>
            <input placeholder="Consulta económica avanzada...">
        </div>
    </body></html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
