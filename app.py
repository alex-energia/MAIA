from flask import Flask, render_template, request, jsonify, redirect
from proyectos import proyectos_bp, init_db, get_db
import os
import random

# =========================
# CREAR APP
# =========================
app = Flask(__name__)

# =========================
# INICIALIZAR DB
# =========================
init_db()

# =========================
# BLUEPRINT
# =========================
app.register_blueprint(proyectos_bp)

# =========================
# DRONES BASE (OFICIAL)
# =========================
DRONES_BASE = [
    {
        "nombre": "Drone submarino detección de petróleo",
        "ruta": "/dron_submarino_petroleo",
        "estado": "aprobado"
    },
    {
        "nombre": "MAIA Punto Eléctrico",
        "ruta": "/maia_punto_electrico",
        "estado": "aprobado"
    },
    {
        "nombre": "Drone Purificador Atmosférico",
        "ruta": "/drone_purificador_atmosferico",
        "estado": "aprobado"
    },
    {
        "nombre": "Drone Generador de Agua Atmosférica",
        "ruta": "/drone_generador_agua",
        "estado": "aprobado"
    },
    {
        "nombre": "Drone Autónomo de Control de Incendios",
        "ruta": "/drone_control_incendios",
        "estado": "aprobado"
    },
    {
        "nombre": "Drone de Lluvia por Ionización Atmosférica",
        "ruta": "/drone_lluvia_ionizacion",
        "estado": "aprobado"
    },
    {
        "nombre": "Sistema Autónomo Híbrido de Descontaminación de Ríos",
        "ruta": "/drone_descontaminacion_rios",
        "estado": "aprobado"
    },
    {
        "nombre": "Sistema Autónomo de Vigilancia y Respuesta Urbana en Enjambre",
        "ruta": "/drone_vigilancia_urbana",
        "estado": "aprobado"
    }
]

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# PROYECTOS
# =========================
@app.route("/proyectos")
def proyectos():
    conn = get_db()
    proyectos = conn.execute(
        "SELECT id, titulo as nombre FROM proyectos_guardados ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("proyectos.html", proyectos=proyectos)

@app.route("/proyectos/<int:id>")
def ver_proyecto(id):
    conn = get_db()
    proyecto = conn.execute(
        "SELECT * FROM proyectos_guardados WHERE id=?",
        (id,)
    ).fetchone()
    conn.close()

    if proyecto is None:
        return "Proyecto no encontrado"

    return render_template("proyecto_detalle.html", proyecto=proyecto)

@app.route("/proyectos/nuevo")
def nuevo_proyecto():
    return render_template("nuevo_proyecto.html")

@app.route("/guardar_proyecto", methods=["POST"])
def guardar_proyecto():
    data = request.form or request.get_json()

    conn = get_db()
    conn.execute(
        """
        INSERT INTO proyectos_guardados
        (titulo, tecnologia, pais, ciudad, moneda, horizonte, potencia, unidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("nombre"),
            data.get("tecnologia"),
            data.get("pais"),
            data.get("ciudad"),
            data.get("moneda"),
            data.get("horizonte"),
            data.get("potencia"),
            data.get("unidad"),
        ),
    )
    conn.commit()
    conn.close()

    return redirect("/proyectos")

# =========================
# MAIA DRONES
# =========================
@app.route("/maia_drone")
def maia_drone():
    return render_template("maia_drone.html")

@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    return jsonify(DRONES_BASE)

# =========================
# 🔥 MAIA MODULOS
# =========================
@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_lab")
def maia_lab():
    return render_template("maia_lab.html")

@app.route("/maia_architect")
def maia_architect():
    return render_template("maia_architect.html")

@app.route("/maia_simulador")
def maia_simulador():
    return render_template("maia_simulador.html")

# =========================
# 🚀 GENERADOR AUTOMÁTICO MAIA
# =========================
@app.route("/generar_drone_maia", methods=["GET"])
def generar_drone_maia():

    problemas = [
        "escasez de agua",
        "contaminación urbana",
        "inseguridad ciudadana",
        "incendios forestales",
        "falta de energía en zonas rurales",
        "contaminación de ríos"
    ]

    tecnologias = [
        "enjambre autónomo",
        "inteligencia artificial distribuida",
        "sensores avanzados",
        "comunicación en red",
        "sistemas híbridos aire-agua"
    ]

    problema = random.choice(problemas)
    tecnologia = random.choice(tecnologias)

    nombre = f"Drone Autónomo para {problema.title()}"

    introduccion = f"Este drone ha sido diseñado para abordar el problema de {problema}, utilizando {tecnologia}, permitiendo una solución escalable y de alto impacto a nivel global."

    viabilidad = "El proyecto es viable debido a la disponibilidad actual de sensores, inteligencia artificial y sistemas de automatización, permitiendo su implementación progresiva en entornos urbanos e industriales."

    software = [
        "IA de navegación autónoma",
        "Sistema de toma de decisiones en tiempo real",
        "Comunicación entre drones (enjambre)",
        "Análisis de datos en la nube"
    ]

    hardware = [
        "Sensores ambientales",
        "Cámara de alta resolución",
        "GPS de precisión",
        "Batería de larga duración",
        "Módulo de comunicación"
    ]

    return jsonify({
        "nombre": nombre,
        "introduccion": introduccion,
        "viabilidad": viabilidad,
        "software": software,
        "hardware": hardware
    })

# =========================
# EVALUADOR
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json()
    idea = data.get("idea", "").lower()

    resultado = {
        "impacto": 0,
        "innovacion": 0,
        "viabilidad": 0,
        "mensaje": ""
    }

    if any(p in idea for p in ["agua","energía","energia","salud","medio ambiente","contaminación","alimentos","incendio"]):
        resultado["impacto"] += 3

    if any(p in idea for p in ["autónomo","enjambre","ia","inteligente","automatizado"]):
        resultado["innovacion"] += 3

    if any(p in idea for p in ["escalable","industrial","ciudad","global"]):
        resultado["viabilidad"] += 3

    total = resultado["impacto"] + resultado["innovacion"] + resultado["viabilidad"]

    if total >= 7:
        resultado["mensaje"] = "🚀 Idea altamente disruptiva y viable"
    elif total >= 4:
        resultado["mensaje"] = "⚠️ Buena idea, pero se puede mejorar"
    else:
        resultado["mensaje"] = "❌ Idea débil, no cumple con la consigna MAIA"

    return jsonify(resultado)

# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)