from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
import math
import numpy as np

# 🔥 PROTECCIÓN TRIMESH (NO ROMPE RENDER)
try:
    import trimesh
except:
    trimesh = None

# =========================
# APP
# =========================
app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_secret_ultra"

# =========================
# INIT
# =========================
init_db()
app.register_blueprint(proyectos_bp)

# =========================
# 🔥 CARGA DRONES
# =========================
def cargar_drones_base():
    drones = []
    carpeta_drones = os.path.join(app.template_folder, "drones")

    if not os.path.exists(carpeta_drones):
        return []

    for archivo in os.listdir(carpeta_drones):
        if archivo.endswith(".html"):
            ruta = "/drones/" + archivo.replace(".html", "")
            path_completo = os.path.join(carpeta_drones, archivo)

            try:
                with open(path_completo, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    titulo = soup.title.string.strip() if soup.title else archivo.replace(".html", "")
            except:
                titulo = archivo.replace(".html", "")

            lower = archivo.lower()

            if "minas" in lower or "militar" in lower:
                categoria = "militar"
            elif "todo_terreno" in lower or "smartphone" in lower:
                categoria = "comercial"
            else:
                categoria = "industrial"

            drones.append({
                "nombre": titulo,
                "ruta": ruta,
                "categoria": categoria
            })

    return drones

# =========================
# DATA GLOBAL
# =========================
try:
    DRONES_BASE = cargar_drones_base()
except:
    DRONES_BASE = []

# =========================
# 🧠 MEMORIA JSON
# =========================
MEMORIA_PATH = "memoria_maia.json"

def cargar_memoria():
    if not os.path.exists(MEMORIA_PATH):
        return []
    try:
        with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_memoria(data):
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# 🧠 GUARDAR PROYECTO
# =========================
@app.route("/maia_guardar_proyecto", methods=["POST"])
def maia_guardar_proyecto():
    data = request.get_json(silent=True) or {}

    memoria = cargar_memoria()

    proyecto = {
        "modulo": data.get("modulo"),
        "nombre": data.get("nombre"),
        "descripcion": data.get("descripcion"),
        "analisis": data.get("analisis"),
        "software": data.get("software"),
        "hardware": data.get("hardware"),
        "modelo_3d": data.get("modelo_3d"),
        "simulacion": data.get("simulacion"),
        "extra": data.get("extra", {}),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    memoria.append(proyecto)
    guardar_memoria(memoria)

    return jsonify({"status": "ok", "mensaje": "🧠 Proyecto guardado correctamente"})

# =========================
# 📂 VER MEMORIA
# =========================
@app.route("/maia_memoria")
def maia_memoria():
    return jsonify(cargar_memoria())

@app.route("/maia_memoria_view")
def maia_memoria_view():
    return render_template("maia_memoria.html")

# =========================
# 🔬 BASE HARDWARE
# =========================
MOTORES = [
    {"modelo": "T-Motor MN4014", "empuje": 3.5},
    {"modelo": "T-Motor U8 Lite", "empuje": 7.2}
]

# =========================
# 🧠 SIMULACIÓN
# =========================
def simular_vuelo(peso, empuje_total):
    gravedad = 9.81
    relacion = (empuje_total * gravedad) / (peso * gravedad)

    if relacion < 1:
        estado = "NO DESPEGA ❌"
    elif relacion < 1.5:
        estado = "INESTABLE ⚠️"
    else:
        estado = "ESTABLE ✅"

    return {
        "peso": peso,
        "empuje_total": empuje_total,
        "relacion": round(relacion, 2),
        "estado": estado
    }

# =========================
# 🧠 MOTOR INGENIERÍA
# =========================
def analizar_drone_real(idea):
    idea = idea.lower()

    peso = 5
    if "incendio" in idea:
        peso = 12
    elif "seguridad" in idea:
        peso = 6

    empuje_necesario = peso * 2

    motor_ok = None
    for m in MOTORES:
        if m["empuje"] * 4 >= empuje_necesario:
            motor_ok = m
            break

    if not motor_ok:
        return {"viabilidad": "NO VIABLE ❌"}

    empuje_total = motor_ok["empuje"] * 4

    return {
        "viabilidad": "VIABLE ✅",
        "analisis": {"tecnico": "Empuje suficiente"},
        "software": {"arquitectura": "ROS2"},
        "hardware": [motor_ok["modelo"]],
        "simulacion": simular_vuelo(peso, empuje_total),
        "modelo_3d": {"tipo": "quadcopter"}
    }

# =========================
# 🔥 MODELO 3D
# =========================
def generar_modelo_3d(_):
    if not trimesh:
        return "/static/no_3d.txt"

    cuerpo = trimesh.creation.box(extents=(0.4, 0.4, 0.08))
    drone = trimesh.util.concatenate([cuerpo])

    os.makedirs("static", exist_ok=True)
    ruta = "static/modelo_drone.glb"
    drone.export(ruta)

    return "/" + ruta

# =========================
# 🚀 ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    return jsonify(analizar_drone_real(data.get("idea", "")))

@app.route("/generar_3d", methods=["POST"])
def generar_3d():
    return jsonify({"modelo_url": generar_modelo_3d({})})

# =========================
# 🔥 🔥 🔥 RUTAS FALTANTES (AQUÍ ESTABA EL ERROR)
# =========================
@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_lab")
def maia_lab():
    return render_template("maia_lab.html")

@app.route("/maia_simulador")
def maia_simulador():
    return render_template("maia_simulador.html")

@app.route("/maia_architect")
def maia_architect():
    return render_template("maia_architect.html")

# =========================
# RESTO
# =========================
@app.route("/ping")
def ping():
    return "OK"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    return jsonify(DRONES_BASE)

@app.route("/maia_chat")
def maia_chat():
    return render_template("maia_chat.html")

@app.route("/drones/<drone_file>")
def abrir_drone(drone_file):
    ruta_html = f"drones/{drone_file}.html"
    if os.path.exists(os.path.join(app.template_folder, ruta_html)):
        return render_template(ruta_html)
    return "Drone no encontrado", 404

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)