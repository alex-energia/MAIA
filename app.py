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
    {"nombre": "Sistema Autónomo de Vigilancia y Respuesta Urbana en Enjambre", "ruta": "/drone_vigilancia_urbana", "estado": "aprobado"},

    # 🔥 NUEVO DRONE MAIA (ASISTENTE CELULAR)
    {
        "nombre": "Mini Drone Asistente Integrado para Smartphone MAIA",
        "ruta": "/drone_smartphone_maia",
        "estado": "aprobado",
        "categoria": "comercial",

        # 🔥 INTRODUCCIÓN + VIABILIDAD (NIVEL PROFESIONAL)
        "introduccion": """
        El Mini Drone Asistente Integrado para Smartphone MAIA es una evolución del concepto de dispositivo móvil,
        transformando el celular en una plataforma aérea inteligente. Este sistema permite desplegar un micro-drone
        directamente desde el teléfono o su estuche, brindando capacidades de grabación aérea, iluminación,
        vigilancia y asistencia en tiempo real.

        Su viabilidad es alta debido a los avances actuales en miniaturización de motores, baterías compactas,
        microestabilización y conectividad inalámbrica. Tecnologías como drones nano, módulos magnéticos,
        carga inversa y chips de bajo consumo ya existen en el mercado, lo que permite integrar este sistema
        en smartphones o accesorios tipo case sin necesidad de infraestructura adicional.

        Este drone representa una nueva categoría: asistentes personales físicos inteligentes.
        """,

        "software": [
            "IA de estabilización automática",
            "Control desde app móvil",
            "Seguimiento inteligente (tracking)",
            "Reconocimiento facial y entorno",
            "Streaming en tiempo real",
            "Modo seguridad con alertas",
            "Integración con GPS del smartphone"
        ],

        "hardware": [
            "Hélices retráctiles ultra compactas",
            "Cámara HD / 4K miniaturizada",
            "Linterna LED integrada",
            "Batería compartida con smartphone",
            "Módulo tipo estuche magnético",
            "Conectividad Bluetooth / WiFi",
            "Sensores de proximidad y estabilidad"
        ]
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

# 🔥 LISTA PARA SIMULADOR
@app.route("/maia_drones_lista")
def maia_drones_lista():
    return jsonify([d["nombre"] for d in DRONES_BASE])

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
# GENERADOR ORIGINAL
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

    return jsonify({
        "nombre": nombre,
        "introduccion": f"Este drone aborda {problema} usando {tecnologia}.",
        "viabilidad": "Alta viabilidad tecnológica.",
        "software": [
            "IA de navegación",
            "sistema autónomo",
            "análisis en tiempo real"
        ],
        "hardware": [
            "sensores",
            "cámara",
            "GPS",
            "batería"
        ]
    })

# =========================
# GUARDAR DRONE MAIA
# =========================
@app.route("/guardar_drone_maia", methods=["POST"])
def guardar_drone_maia():
    data = request.get_json()
    nombre = data.get("nombre", "")
    tipo = data.get("tipo")

    # 🔥 FORZAR A COMERCIAL SI ES SMARTPHONE
    if "smartphone" in nombre.lower():
        tipo = "comercial"

    conn = get_db()
    conn.execute(
        """
        INSERT INTO proyectos_guardados (titulo, tecnologia, pais, ciudad)
        VALUES (?, ?, ?, ?)
        """,
        (
            nombre,
            tipo,
            "Global",
            "MAIA"
        )
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# =========================
# DRONE SMARTPHONE
# =========================
@app.route("/drone_smartphone_maia")
def drone_smartphone_maia():
    return render_template("drones/drone_smartphone_maia.html")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)