from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_market_intelligence import buscar_oportunidades, detectar_activos_tempranos
from maia_global_scanner import escanear_mercado_global
import os

# =========================
# CREAR APP
# =========================

app = Flask(__name__)

# =========================
# INICIALIZAR BASE DE DATOS
# =========================

init_db()

# =========================
# REGISTRAR BLUEPRINT
# =========================

app.register_blueprint(proyectos_bp)

# =========================
# PAGINA PRINCIPAL
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# ALERTAS MAIA
# =========================

@app.route("/maia_alertas")
def maia_alertas():

    from proyectos import get_db

    conn = get_db()

    alertas = conn.execute(
        "SELECT * FROM maia_alertas ORDER BY id DESC LIMIT 10"
    ).fetchall()

    conn.close()

    return jsonify([dict(a) for a in alertas])

# =========================
# CHAT MAIA
# =========================

@app.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()
    pregunta = data.get("message", "").lower()

    respuesta = "MAIA no tiene suficiente información para responder."

    # =========================
    # ANALISIS FINANCIERO
    # =========================

    if "van" in pregunta:
        respuesta = "El VAN (Valor Actual Neto) mide la rentabilidad del proyecto descontando los flujos futuros."

    elif "tir" in pregunta:
        respuesta = "La TIR es la tasa de retorno que iguala el VAN a cero. Si es mayor al costo de capital, el proyecto es rentable."

    elif "riesgo" in pregunta:
        respuesta = "El riesgo del proyecto depende de la volatilidad de ingresos, el CAPEX y la estabilidad del flujo de caja."

    elif "invertir" in pregunta:
        respuesta = "MAIA recomienda evaluar VAN positivo, TIR mayor al WACC y probabilidad alta en la simulación Monte Carlo."

    elif "capex" in pregunta:
        respuesta = "El CAPEX corresponde a la inversión inicial necesaria para ejecutar el proyecto."

    elif "payback" in pregunta:
        respuesta = "El payback indica el tiempo necesario para recuperar la inversión inicial."

    elif "montecarlo" in pregunta:
        respuesta = "La simulación Monte Carlo evalúa miles de escenarios posibles para estimar la probabilidad de rentabilidad."

    # =========================
    # INFORMACION SOBRE MAIA
    # =========================

    elif "maia" in pregunta:
        respuesta = "MAIA es un motor de inteligencia energética que analiza proyectos, detecta oportunidades de inversión y realiza barridos globales del mercado energético."

    # =========================
    # SCANNER GLOBAL
    # =========================

    elif "barrido" in pregunta or "scan" in pregunta or "buscar proyectos" in pregunta:

        resultados = escanear_mercado_global()

        respuesta = f"MAIA realizó un barrido global y encontró {len(resultados)} oportunidades energéticas."

    elif "smr" in pregunta or "nuclear" in pregunta:

        resultados = escanear_mercado_global()

        filtrados = [r for r in resultados if r.get("tipo_activo") == "nuclear_smr"]

        respuesta = f"MAIA detectó {len(filtrados)} oportunidades relacionadas con reactores nucleares SMR."

    elif "hidro" in pregunta or "hidroelectrica" in pregunta:

        resultados = escanear_mercado_global()

        filtrados = [r for r in resultados if r.get("tipo_activo") == "hidroelectrica"]

        respuesta = f"MAIA detectó {len(filtrados)} oportunidades hidroeléctricas en el mercado global."

    return jsonify({"reply": respuesta})

# =========================
# MAIA OPORTUNIDADES ENERGETICAS
# =========================

@app.route("/maia_oportunidades")
def maia_oportunidades():

    try:

        data = buscar_oportunidades()

        return jsonify({
            "total_oportunidades": len(data),
            "oportunidades": data
        })

    except Exception as e:

        return jsonify({
            "error": "Error buscando oportunidades",
            "detalle": str(e)
        })

# =========================
# MAIA DEAL FINDER
# =========================

@app.route("/maia_deal_finder")
def maia_deal_finder():

    try:

        data = detectar_activos_tempranos()

        return jsonify({
            "deals_detectados": len(data),
            "deals": data
        })

    except Exception as e:

        return jsonify({
            "error": "Error detectando activos",
            "detalle": str(e)
        })

# =========================
# MAIA GLOBAL SCANNER
# =========================

@app.route("/maia_global_scan")
def maia_global_scan():

    try:

        data = escanear_mercado_global()

        return jsonify({
            "total_oportunidades": len(data),
            "resultados": data
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# HEALTH CHECK (IMPORTANTE PARA RENDER)
# =========================

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# =========================
# EJECUTAR APP
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )