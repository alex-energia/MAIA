# main.py - CONSOLA MAIA II V.7
from flask import Flask, render_template_string, request
from scout_engine import scout_engine
from builder_engine import builder_engine
import os

app = Flask(__name__)

@app.route('/')
def index():
    # El código del buscador (Scout) se mantiene idéntico aquí
    return render_template_string("<h1>CONSOLA PRINCIPAL MAIA - SCOUT ACTIVO</h1><a href='/builder'>IR AL CONSTRUCTOR</a>")

@app.route('/builder', methods=['GET', 'POST'])
def builder_view():
    resultado = None
    if request.method == 'POST':
        resultado = builder_engine.run_full_model(request.form)

    h = f"""
    <html><head>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .tab-container {{ border:2px solid #f0f; padding:20px; }}
        .metric-card {{ display:inline-block; border:1px solid #0f0; padding:15px; margin:10px; min-width:200px; }}
        input {{ background:#111; border:1px solid #0ff; color:#fff; padding:10px; width:100%; margin-bottom:10px; }}
        .maia-chat {{ position:fixed; bottom:20px; right:20px; width:350px; border:2px solid #f0f; background:#111; }}
    </style>
    </head><body>
        <h1 style="color:#f0f;">MAIA BUILDER - FORMULARIO FINANCIERO DETALLADO</h1>
        <form method="post">
            <div class="tab-container">
                <h3>Pestaña 1: CAPEX & Ingeniería</h3>
                <input name="capex" placeholder="Inversión Total (CAPEX USD)">
                <input name="power" placeholder="Potencia (MW)">
                
                <h3>Pestaña 2: Ingresos y Mercado</h3>
                <input name="ingresos_est" placeholder="Ingreso Anual Estimado (PPA)">
                <input name="trm_manual" placeholder="TRM (Auto: 3900)">
                
                <button type="submit" style="background:#0f0; color:#000; padding:15px; width:100%; cursor:pointer; font-weight:bold;">
                    GENERAR MODELO FINANCIERO & MONTECARLO
                </button>
            </div>
        </form>

        {f'''
        <div class="tab-container" style="margin-top:20px; border-color:#0f0;">
            <h2 style="color:#0f0;">RESULTADOS DEL MODELO</h2>
            <div class="metric-card">VPN: <br><span style="font-size:20px;">${resultado['VPN']:,.2f}</span></div>
            <div class="metric-card">TIR: <br><span style="font-size:20px;">{resultado['TIR']:.2f}%</span></div>
            <div class="metric-card">MONTECARLO (Éxito): <br><span style="font-size:20px;">{resultado['Montecarlo_Exito']}%</span></div>
            <br>
            <button class="btn" style="border:1px solid #f0f; color:#f0f; background:none; padding:10px;">GUARDAR EN MEMORIA</button>
        </div>
        ''' if resultado else ''}

        <div class="maia-chat">
            <div style="background:#f0f; color:#000; padding:10px;">MAIA ECONOMIST AGENT</div>
            <div style="padding:15px; font-size:12px;">
                Especialista en análisis de sensibilidad y riesgos financieros. 
                <input placeholder="Pregunta sobre la TIR o Ley 1715..." style="margin-top:10px;">
            </div>
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)