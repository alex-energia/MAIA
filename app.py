from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
import math
import trimesh
import numpy as np

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
        print("⚠️ Carpeta drones no encontrada")
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

    return jsonify({
        "status": "ok",
        "mensaje": "🧠 Proyecto guardado correctamente"
    })

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
# 🧠 SIMULACIÓN FÍSICA REAL
# =========================
def simular_vuelo(peso, empuje_total):
    gravedad = 9.81
    fuerza_peso = peso * gravedad
    empuje_n = empuje_total * gravedad

    relacion = empuje_n / fuerza_peso

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
    elif "agua" in idea:
        peso = 10

    empuje_necesario = peso * 2
    motor_ok = None

    for m in MOTORES:
        if m["empuje"] * 4 >= empuje_necesario:
            motor_ok = m
            break

    if not motor_ok:
        return {
            "viabilidad": "NO VIABLE ❌",
            "causas": ["Empuje insuficiente"]
        }

    empuje_total = motor_ok["empuje"] * 4
    simulacion = simular_vuelo(peso, empuje_total)

    return {
        "viabilidad": "VIABLE ✅",
        "analisis": {
            "tecnico": f"Empuje requerido {empuje_necesario}kg con {motor_ok['modelo']}",
            "economico": "Costo medio-alto",
            "profesional": "Requiere equipo especializado"
        },
        "software": {
            "arquitectura": "ROS2 + PX4",
            "modulos": ["flight_controller", "navigation", "vision_ai"],
            "algoritmos": ["PID", "SLAM", "A*", "Kalman"]
        },
        "hardware": [
            f"Motor: {motor_ok['modelo']}",
            "Pixhawk",
            "GPS",
            "Lidar",
            "Batería LiPo"
        ],
        "simulacion": simulacion,
        "modelo_3d": {
            "tipo": "quadcopter",
            "peso": peso
        },
        "garantia": "Validado con simulación física"
    }

# =========================
# 🔥 MODELO 3D PRO
# =========================
def generar_modelo_3d(_):
    cuerpo = trimesh.creation.box(extents=(0.4, 0.4, 0.08))

    brazos = []
    for ang in [0, 90, 45, -45]:
        b = trimesh.creation.box(extents=(0.7, 0.06, 0.06))
        b.apply_transform(
            trimesh.transformations.rotation_matrix(math.radians(ang), [0,0,1])
        )
        brazos.append(b)

    motores = []
    for x,y in [(0.35,0.35),(-0.35,0.35),(0.35,-0.35),(-0.35,-0.35)]:
        m = trimesh.creation.cylinder(radius=0.06, height=0.08)
        m.apply_translation([x,y,0.05])
        motores.append(m)

    drone = trimesh.util.concatenate([cuerpo] + brazos + motores)

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
    idea = data.get("idea", "")

    if len(idea.strip()) < 5:
        return jsonify({
            "viabilidad": "NO VIABLE ❌",
            "causas": ["Idea poco definida"]
        })

    return jsonify(analizar_drone_real(idea))

@app.route("/generar_3d", methods=["POST"])
def generar_3d():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "modelo_url": generar_modelo_3d(data)
    })

# =========================
# 🧠 VISOR 3D
# =========================
@app.route("/maia_visor_3d")
def maia_visor_3d():
    return render_template("maia_visor_3d.html")

# =========================
# RESTO
# =========================
@app.route("/ping")
def ping():
    return "OK", 200

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    categoria = request.args.get("categoria")
    if categoria:
        return jsonify([d for d in DRONES_BASE if d["categoria"] == categoria])
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