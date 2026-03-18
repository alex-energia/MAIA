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
    {"nombre": "Drone submarino detección de petróleo", "ruta": "/dron_submarino_petroleo", "estado": "aprobado"},
    {"nombre": "MAIA Punto Eléctrico", "ruta": "/maia_punto_electrico", "estado": "aprobado"},
    {"nombre": "Drone Purificador Atmosférico", "ruta": "/drone_purificador_atmosferico", "estado": "aprobado"},
    {"nombre": "Drone Generador de Agua Atmosférica", "ruta": "/drone_generador_agua", "estado": "aprobado"},
    {"nombre": "Drone Autónomo de Control de Incendios", "ruta": "/drone_control_incendios", "estado": "aprobado"},
    {"nombre": "Drone de Lluvia por Ionización Atmosférica", "ruta": "/drone_lluvia_ionizacion", "estado": "aprobado"},
    {"nombre": "Sistema Autónomo Híbrido de Descontaminación de Ríos", "ruta": "/drone_descontaminacion_rios", "estado": "aprobado"},
    {"nombre": "Sistema Autónomo de Vigilancia y Respuesta Urbana en Enjambre", "ruta": "/drone_vigilancia_urbana", "estado": "aprobado"}
]

# =========================
# UTILIDAD CLAVE (ANTI-REPETICIÓN REAL)
# =========================
def obtener_nombres_existentes():
    nombres = set([d["nombre"].lower() for d in DRONES_BASE])
    try:
        conn = get_db()
        rows = conn.execute("SELECT titulo FROM proyectos_guardados").fetchall()
        conn.close()
        for r in rows:
            nombres.add(r["titulo"].lower())
    except:
        pass
    return nombres

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
# MAIA MODULOS
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
# 🚀 GENERADOR MAIA (REEMPLAZA EL PROBLEMA)
# =========================
@app.route("/generar_drone_maia", methods=["GET"])
def generar_drone_maia():

    existentes = obtener_nombres_existentes()

    problemas = [
        "control de disturbios urbanos",
        "seguridad en eventos masivos",
        "detección de amenazas en fronteras",
        "rescate en zonas de desastre",
        "protección de fauna silvestre",
        "optimización logística autónoma",
        "inspección de infraestructura crítica",
        "control de tráfico inteligente",
        "vigilancia aérea estratégica",
        "operaciones tácticas en entornos hostiles"
    ]

    tecnologias = [
        "IA adaptativa",
        "enjambre autónomo",
        "visión computacional avanzada",
        "red neuronal distribuida",
        "aprendizaje en tiempo real",
        "arquitectura descentralizada"
    ]

    funciones = [
        "respuesta autónoma",
        "detección predictiva",
        "intervención táctica",
        "coordinación inteligente",
        "análisis en tiempo real",
        "neutralización automatizada"
    ]

    for _ in range(50):

        problema = random.choice(problemas)
        tecnologia = random.choice(tecnologias)
        funcion = random.choice(funciones)

        nombre = f"Sistema Autónomo de {funcion.title()} para {problema.title()} con {tecnologia.title()}"

        if nombre.lower() not in existentes:
            break

    return jsonify({
        "nombre": nombre,
        "introduccion": f"Este sistema utiliza {tecnologia} para ejecutar {funcion} frente a {problema}.",
        "viabilidad": "Alta viabilidad tecnológica y escalabilidad global.",
        "software": [
            "IA de toma de decisiones",
            "visión computacional",
            "coordinación en enjambre",
            "análisis predictivo",
            "respuesta automática"
        ],
        "hardware": [
            "sensores multispectrales",
            "cámara térmica",
            "GPS de alta precisión",
            "módulo de comunicación mesh",
            "estructura resistente",
            "batería inteligente"
        ]
    })

# =========================
# GUARDAR DRONE MAIA
# =========================
@app.route("/guardar_drone_maia", methods=["POST"])
def guardar_drone_maia():
    data = request.get_json()

    conn = get_db()
    conn.execute(
        """
        INSERT INTO proyectos_guardados (titulo, tecnologia, pais, ciudad)
        VALUES (?, ?, ?, ?)
        """,
        (
            data.get("nombre"),
            data.get("tipo"),
            "Global",
            "MAIA"
        )
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# =========================
# EVALUADOR
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json()
    idea = data.get("idea", "").lower()

    resultado = {"impacto": 0, "innovacion": 0, "viabilidad": 0, "mensaje": ""}

    if any(p in idea for p in ["agua","energia","salud","medio ambiente"]):
        resultado["impacto"] += 3

    if any(p in idea for p in ["ia","autónomo","enjambre"]):
        resultado["innovacion"] += 3

    if any(p in idea for p in ["escalable","industrial","global"]):
        resultado["viabilidad"] += 3

    total = sum(resultado.values())

    if total >= 7:
        resultado["mensaje"] = "🚀 Alta calidad"
    elif total >= 4:
        resultado["mensaje"] = "⚠️ Mejorable"
    else:
        resultado["mensaje"] = "❌ Débil"

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