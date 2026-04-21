# main.py - CONSOLA MAIA II V.6
from flask import Flask, render_template_string, request
from scout_engine import scout_engine
from builder_engine import builder_engine

app = Flask(__name__)

@app.route('/builder', methods=['GET', 'POST'])
def builder():
    # Variables automáticas detectadas por MAIA
    market = builder_engine.get_market_variables("Solar", "Colombia")
    
    h = f"""
    <html><head>
    <style>
        body {{ background:#000; color:#0ff; font-family:monospace; padding:20px; }}
        .form-sec {{ border:1px solid #0f0; padding:20px; margin-bottom:20px; background:rgba(0,20,0,0.3); }}
        .indicator {{ color:#f0f; font-weight:bold; font-size:1.2em; }}
        input {{ background:#111; border:1px solid #0ff; color:#fff; padding:8px; width:100%; }}
        .chat-float {{ position:fixed; bottom:20px; right:20px; width:380px; border:2px solid #f0f; background:#000; z-index:1000; }}
        .minimized {{ height:45px; overflow:hidden; }}
    </style>
    <script>function toggleChat() {{ document.getElementById('chat').classList.toggle('minimized'); }}</script>
    </head><body>
        <h1 style="color:#f0f;">MAIA PROJECT BUILDER - MODELO MULTI-TECNOLOGÍA</h1>
        
        <form method="post" action="/run_model">
            <div class="form-sec">
                <h3>1. VARIABLES DE ENTRADA (MAIA AUTO-DETECT)</h3>
                TRM Sugerida: <input name="trm" value="{market['trm']}">
                IPC Proyectado: <input name="ipc" value="{market['ipc']}">
            </div>

            <div class="form-sec">
                <h3>2. DETALLE CAPEX / OPEX</h3>
                CAPEX Total (USD): <input name="capex" placeholder="Ej: 90000000">
                OPEX Anual (USD): <input name="opex" placeholder="Ej: 1000000">
                Potencia Instalada (MW/GW): <input name="power">
            </div>

            <div class="form-sec">
                <h3>3. ESTRUCTURA FINANCIERA</h3>
                % Deuda: <input name="debt_pct" value="0.7">
                Tasa de Interés: <input name="rate" value="0.11">
            </div>

            <button type="submit" style="background:#f0f; color:#000; padding:20px; width:100%; font-weight:bold; cursor:pointer;">
                EJECUTAR MODELO FINANCIERO & MONTECARLO
            </button>
        </form>

        <div id="chat" class="chat-float minimized">
            <div style="background:#f0f; color:#000; padding:10px; cursor:pointer;" onclick="toggleChat()">
                MAIA ECONOMIST AGENT [+/-]
            </div>
            <div style="padding:15px;">
                <p style="font-size:10px; color:#0f0;">Especialista en: TIR, VAN, LCOE, Montecarlo y Ley 1715.</p>
                <div id="chat-content" style="height:200px; overflow-y:auto; border-bottom:1px solid #333;">
                    MAIA: Esperando ejecución del modelo para análisis de sensibilidad...
                </div>
                <input placeholder="Pregunta sobre el modelo..." style="margin-top:10px;">
            </div>
        </div>
    </body></html>
    """
    return render_template_string(h)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
