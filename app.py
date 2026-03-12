from flask import Flask, render_template, request, jsonify, redirect
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
# PAGINA PROYECTOS
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
# CREAR PROYECTO
# =========================

@app.route("/proyectos/nuevo")
def nuevo_proyecto():

    return """
    <h2>Crear nuevo proyecto</h2>

    <form method="post" action="/guardar_proyecto">

    Nombre del proyecto:<br>
    <input name="nombre"><br><br>

    <button type="submit">Guardar</button>

    </form>
    """


@app.route("/guardar_proyecto", methods=["POST"])
def guardar_proyecto():

    nombre = request.form.get("nombre")

    conn = get_db()

    conn.execute(
        "INSERT INTO proyectos_guardados (titulo) VALUES (?)",
        (nombre,)
    )

    conn.commit()
    conn.close()

    return redirect("/proyectos")


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

    for q in queries:

        try:

            r = requests.get(
                "https://duckduckgo.com/html/",
                params={"q": q},
                timeout=5
            )

            if r.status_code == 200:

                bloques = r.text.split("result__a")

                for b in bloques[1:3]:

                    try:

                        titulo = b.split(">")[1].split("<")[0]
                        link = b.split('href="')[1].split('"')[0]

                        resultados.append({

                            "titulo": titulo,
                            "pais": "web",
                            "tipo_activo": "energia",
                            "capacidad_mw": "N/D",
                            "empresa": "fuente web",
                            "contacto": link

                        })

                    except:
                        pass

        except:
            pass

    return resultados


# =========================
# HYDRO DEAL HUNTER
# =========================

def maia_hydro_deal_hunter():

    queries = [

        "hydropower project for sale colombia",
        "hydropower concession latin america",
        "small hydro plant investment 1 mw",
        "hydropower asset acquisition",
        "hydro project seeking investors"

    ]

    deals = []

    for q in queries:

        try:

            r = requests.get(
                "https://duckduckgo.com/html/",
                params={"q": q},
                timeout=5
            )

            bloques = r.text.split("result__a")

            for b in bloques[1:3]:

                try:

                    titulo = b.split(">")[1].split("<")[0]
                    link = b.split('href="')[1].split('"')[0]

                    deals.append({

                        "titulo": titulo,
                        "pais": "global",
                        "tipo_activo": "hidroelectrica",
                        "capacidad_mw": "1+ MW",
                        "empresa": "market source",
                        "contacto": link

                    })

                except:
                    pass

        except:
            pass

    return deals


# =========================
# MAIA OPORTUNIDADES
# =========================

@app.route("/maia_oportunidades")
def maia_oportunidades():

    resultados = []

    try:
        resultados.extend(buscar_oportunidades())
    except:
        pass

    try:
        resultados.extend(maia_energy_harvester())
    except:
        pass

    try:
        resultados.extend(maia_hydro_deal_hunter())
    except:
        pass

    return jsonify({

        "total_oportunidades": len(resultados),
        "oportunidades": resultados

    })


# =========================
# MAIA MASTER SCANNER
# =========================

@app.route("/maia_master_scan")
def maia_master_scan():

    oportunidades = []

    try:
        oportunidades.extend(buscar_oportunidades())
    except:
        pass

    try:
        oportunidades.extend(detectar_activos_tempranos())
    except:
        pass

    try:
        oportunidades.extend(escanear_mercado_global())
    except:
        pass

    try:
        oportunidades.extend(maia_energy_harvester())
    except:
        pass

    try:
        oportunidades.extend(maia_hydro_deal_hunter())
    except:
        pass

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