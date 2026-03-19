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
    {"nombre": "Drone submarino detección de petróleo", "ruta": "/dron_submarino_petroleo", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "MAIA Punto Eléctrico", "ruta": "/maia_punto_electrico", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Drone Purificador Atmosférico", "ruta": "/drone_purificador_atmosferico", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Drone Generador de Agua Atmosférica", "ruta": "/drone_generador_agua", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Drone Autónomo de Control de Incendios", "ruta": "/drone_control_incendios", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Drone de Lluvia por Ionización Atmosférica", "ruta": "/drone_lluvia_ionizacion", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Sistema Autónomo Híbrido de Descontaminación de Ríos", "ruta": "/drone_descontaminacion_rios", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Drone Todo Terreno MAIA", "ruta": "/drone_todo_terreno", "estado": "aprobado", "categoria": "industrial"},
    {"nombre": "Sistema Autónomo de Vigilancia y Respuesta Urbana en Enjambre", "ruta": "/drone_vigilancia_urbana", "estado": "aprobado", "categoria": "militar"},
    {"nombre": "Drone de Detección de Minas", "ruta": "/drone_deteccion_minas", "estado": "aprobado", "categoria": "militar"},
    # 🔥 DRONE SMARTPHONE (COMERCIAL)
    {
        "nombre": "Mini Drone Asistente Integrado para Smartphone MAIA",
        "ruta": "/drone_smartphone_maia",
        "estado": "aprobado",
        "categoria": "comercial",
        "introduccion": """
        El Mini Drone Asistente Integrado para Smartphone MAIA es una evolución del dispositivo móvil,
        convirtiendo el celular en una plataforma aérea inteligente.
        """,
        "software": [
            "IA de estabilización automática",
            "Control desde app móvil"
        ],
        "hardware": [
            "Hélices compactas",
            "Cámara HD",
            "Batería integrada"
        ]
    }
]

# =========================
# 🔥 MAIA INVENT MEJORADO
# =========================
PROBLEMAS_REALES = [
    "contaminación del aire",
    "contaminación de ríos",
    "incendios forestales",
    "rescate en desastres",
    "seguridad urbana",
    "tráfico en ciudades",
    "agricultura ineficiente",
    "minería ilegal",
    "cambio climático",
    "vigilancia ambiental"
]

def obtener_nombres_drones():
    return [d["nombre"].lower() for d in DRONES_BASE]

def generar_drone_unico():
    nombres_existentes = obtener_nombres_drones()
    for _ in range(15):
        problema = random.choice(PROBLEMAS_REALES)
        nombre = f"Drone Autónomo para {problema.title()}"
        if nombre.lower() not in nombres_existentes:
            return {
                "nombre": nombre,
                "introduccion": f"Este drone aborda {problema} usando inteligencia artificial avanzada.",
                "viabilidad": "Alta viabilidad tecnológica.",
                "software": [
                    "IA de navegación",
                    "análisis en tiempo real",
                    "detección de patrones"
                ],
                "hardware": [
                    "sensores especializados",
                    "cámara HD",
                    "GPS",
                    "batería"
                ]
            }
    return {"error": "No se pudo generar drone único"}

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# MAIA DRONES
# =========================
@app.route("/maia_drone")
def maia_drone():
    return render_template("maia_drone.html")

# 🔥 NUEVA RUTA (CORRIGE ERROR 404)
@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    return jsonify(DRONES_BASE)

@app.route("/maia_drones_lista")
def maia_drones_lista():
    return jsonify(DRONES_BASE)

# =========================
# DRONE SMARTPHONE
# =========================
@app.route("/drone_smartphone_maia")
def drone_smartphone_maia():
    return render_template("drones/drone_smartphone_maia.html")

# =========================
# GENERADOR MEJORADO
# =========================
@app.route("/generar_drone_maia", methods=["GET"])
def generar_drone_maia():
    return jsonify(generar_drone_unico())

# =========================
# GUARDAR DRONE
# =========================
@app.route("/guardar_drone_maia", methods=["POST"])
def guardar_drone_maia():
    data = request.get_json()
    nombre = data.get("nombre", "")
    tipo = data.get("tipo")
    if "smartphone" in nombre.lower():
        tipo = "comercial"
    conn = get_db()
    conn.execute(
        """
        INSERT INTO proyectos_guardados (titulo, tecnologia, pais, ciudad)
        VALUES (?, ?, ?, ?)
        """,
        (nombre, tipo, "Global", "MAIA")
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
# 🔥 MAIA VOZ Y CHAT
# =========================
@app.route("/maia_voz", methods=["POST"])
def maia_voz():
    data = request.get_json()
    pregunta = data.get("pregunta","")
    # Reglas de interacción MAIA
    respuesta = f"MAIA (experta integral en finanzas, economía, energía, hidroeléctricas, solar, eólica, nuclear, geotérmica, diagnóstico de plantas, peso de ganado, diseño, construcción, software y hardware en drones) recibió tu pregunta: {pregunta}. ¿Deseas que te entregue la bibliografía?"
    return jsonify({"respuesta": respuesta})

@app.route("/maia_subir_archivo", methods=["POST"])
def maia_subir_archivo():
    archivos = request.files.getlist('archivos')
    nombres = [a.filename for a in archivos]
    return jsonify({"status":"ok","archivos":nombres})

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)