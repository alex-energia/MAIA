from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_market_intelligence import buscar_oportunidades, detectar_activos_tempranos
import os

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
# CHAT MAIA
# =========================
@app.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()
    pregunta = data.get("message","").lower()

    respuesta = "MAIA no tiene suficiente información para responder."

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

    elif "maia" in pregunta:
        respuesta = "MAIA es un motor de análisis financiero que evalúa proyectos usando indicadores, simulaciones y modelos de riesgo."

    return jsonify({"reply": respuesta})


# =========================
# MAIA OPORTUNIDADES ENERGÉTICAS
# =========================
@app.route("/maia_oportunidades")
def maia_oportunidades():

    data = buscar_oportunidades()

    return jsonify({
        "total_oportunidades": len(data),
        "oportunidades": data
    })


# =========================
# MAIA DEAL FINDER
# Detecta activos antes de salir al mercado
# =========================
@app.route("/maia_deal_finder")
def maia_deal_finder():

    data = detectar_activos_tempranos()

    return jsonify({
        "deals_detectados": len(data),
        "deals": data
    })


# =========================
# EJECUTAR APLICACION
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)