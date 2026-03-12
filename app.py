from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db, get_db
from maia_market_intelligence import buscar_oportunidades, detectar_activos_tempranos
from maia_global_scanner import escanear_mercado_global
import requests
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
# PAGINA PROYECTOS (ARREGLA EL 404)
# =========================

@app.route("/proyectos")
def proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT id, titulo as nombre FROM proyectos_guardados ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("proyectos.html", proyectos=proyectos)

# =========================
# ALERTAS MAIA
# =========================

@app.route("/maia_alertas")
def maia_alertas():

    conn = get_db()

    alertas = conn.execute(
        "SELECT * FROM maia_alertas ORDER BY id DESC LIMIT 10"
    ).fetchall()

    conn.close()

    return jsonify([dict(a) for a in alertas])

# =========================
# ENERGY HARVESTER
# =========================

def maia_energy_harvester():

    queries = [

        "hydropower project for sale",
        "small hydro project investment",
        "renewable energy project investment opportunity",
        "energy project seeking investors",
        "run of river hydro project investment",
        "hydropower concession project",
        "hydropower tender",
        "renewable energy M&A project"

    ]

    resultados = []

    try:

        for q in queries:

            r = requests.get(
                "https://duckduckgo.com/html/",
                params={"q": q},
                timeout=15
            )

            if r.status_code == 200:

                bloques = r.text.split("result__a")

                for b in bloques[1:6]:

                    try:

                        titulo = b.split(">")[1].split("<")[0]
                        link = b.split('href="')[1].split('"')[0]

                        resultados.append({

                            "titulo": titulo,
                            "pais": "Detectado en web",
                            "tipo_activo": "energia",
                            "capacidad_mw": "N/D",
                            "empresa": "Fuente web",
                            "contacto": link

                        })

                    except:
                        pass

    except:
        pass

    return resultados

# =========================
# MAIA MASTER SCANNER
# ACTIVA TODOS LOS MOTORES
# =========================

@app.route("/maia_master_scan")
def maia_master_scan():

    oportunidades = []

    try:

        a = buscar_oportunidades()
        b = detectar_activos_tempranos()
        c = escanear_mercado_global()
        d = maia_energy_harvester()

        oportunidades.extend(a)
        oportunidades.extend(b)
        oportunidades.extend(c)
        oportunidades.extend(d)

    except Exception as e:

        return jsonify({"error": str(e)})

    return jsonify({

        "motor": "MAIA MASTER ENERGY SCANNER",
        "total_oportunidades": len(oportunidades),
        "resultados": oportunidades

    })

# =========================
# CHAT MAIA
# =========================

@app.route("/maia_chat", methods=["POST"])
def maia_chat():

    data = request.get_json()

    pregunta = data.get("message", "").lower()

    respuesta = "MAIA no tiene suficiente información para responder."

    if "van" in pregunta:

        respuesta = "El VAN mide la rentabilidad descontando flujos futuros."

    elif "tir" in pregunta:

        respuesta = "La TIR es la tasa de retorno que iguala el VAN a cero."

    elif "riesgo" in pregunta:

        respuesta = "El riesgo depende de volatilidad de ingresos y CAPEX."

    elif "scan" in pregunta or "buscar proyectos" in pregunta:

        resultados = maia_master_scan()

        respuesta = "MAIA ejecutó un escaneo global del mercado energético."

    return jsonify({"reply": respuesta})

# =========================
# HEALTH CHECK
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