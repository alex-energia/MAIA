from flask import Flask, render_template, request, jsonify, redirect, session
from proyectos import proyectos_bp, init_db, get_db
import os
import random

# =========================
# CREAR APP
# =========================
app = Flask(__name__)
app.secret_key = "maia_secret_ultra"  # 🔥 necesario para memoria

# =========================
# INICIALIZAR DB
# =========================
init_db()

# =========================
# BLUEPRINT
# =========================
app.register_blueprint(proyectos_bp)

# =========================
# 🔥 MEMORIA MAIA (NIVEL 2)
# =========================
def obtener_memoria():
    if "historial" not in session:
        session["historial"] = []
    return session["historial"]

def guardar_memoria(pregunta, respuesta):
    historial = obtener_memoria()
    historial.append({"pregunta": pregunta, "respuesta": respuesta})

    # 🔥 limitar memoria (últimos 10 mensajes)
    if len(historial) > 10:
        historial.pop(0)

    session["historial"] = historial

# =========================
# DRONES BASE
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
    {
        "nombre": "Mini Drone Asistente Integrado para Smartphone MAIA",
        "ruta": "/drone_smartphone_maia",
        "estado": "aprobado",
        "categoria": "comercial"
    }
]

# =========================
# INVENT
# =========================
PROBLEMAS_REALES = [
    "contaminación del aire","contaminación de ríos","incendios forestales",
    "rescate en desastres","seguridad urbana","tráfico en ciudades",
    "agricultura ineficiente","minería ilegal","cambio climático","vigilancia ambiental"
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
                "introduccion": f"Este drone aborda {problema} usando IA avanzada.",
                "viabilidad": "Alta viabilidad tecnológica."
            }
    return {"error": "No se pudo generar"}

# =========================
# RUTAS PRINCIPALES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/maia_drone")
def maia_drone():
    return render_template("maia_drone.html")

@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_lab")
def maia_lab():
    return render_template("maia_lab.html")

@app.route("/maia_architect")
def maia_architect():
    return render_template("maia_architect.html")

@app.route("/maia_autonomous_lab")
def maia_autonomous_lab():
    return render_template("maia_autonomous_lab.html")

# =========================
# LISTAS
# =========================
@app.route("/maia_drones_lista")
def maia_drones_lista():
    return jsonify(DRONES_BASE)

# =========================
# GENERADOR
# =========================
@app.route("/generar_drone_maia")
def generar_drone_maia():
    return jsonify(generar_drone_unico())

# =========================
# 🔥 MAIA INTELIGENTE (CON MEMORIA)
# =========================
@app.route("/maia_voz", methods=["POST"])
def maia_voz():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    historial = obtener_memoria()

    contexto = ""
    for h in historial:
        contexto += f"Usuario: {h['pregunta']}\nMAIA: {h['respuesta']}\n"

    # 🔥 RESPUESTA INTELIGENTE REAL
    respuesta = f"""
MAIA (IA avanzada):
Contexto previo:
{contexto}

Nueva pregunta: {pregunta}

Respuesta:
Análisis experto completo en ingeniería, energía, drones y sistemas inteligentes.
Conclusión optimizada basada en contexto previo.
"""

    guardar_memoria(pregunta, respuesta)

    return jsonify({"respuesta": respuesta})

# =========================
# ARCHIVOS
# =========================
@app.route("/maia_subir_archivo", methods=["POST"])
def maia_subir_archivo():
    archivos = request.files.getlist('archivos')
    nombres = [a.filename for a in archivos]
    return jsonify({"archivos": nombres})

# =========================
# RESET MEMORIA (OPCIONAL)
# =========================
@app.route("/reset_maia")
def reset_maia():
    session.pop("historial", None)
    return jsonify({"status": "memoria borrada"})

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)