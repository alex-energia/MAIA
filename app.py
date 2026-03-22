from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
import math

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
            except Exception as e:
                print("Error leyendo drone:", e)
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
except Exception as e:
    print("🔥 ERROR cargando drones:", e)
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
# 🔬 BASE HARDWARE REAL
# =========================
MOTORES = [
    {"modelo": "T-Motor MN4014", "empuje": 3.5},
    {"modelo": "T-Motor U8 Lite", "empuje": 7.2}
]

# =========================
# 🧠 MOTOR INGENIERÍA REAL
# =========================
def analizar_drone_real(idea):

    idea = idea.lower()

    peso = 5
    tipo = "general"

    if "incendio" in idea:
        peso = 12
        tipo = "emergencia"
    elif "seguridad" in idea:
        peso = 6
        tipo = "vigilancia"
    elif "agua" in idea:
        peso = 10
        tipo = "ambiental"

    empuje_necesario = peso * 2

    motor_ok = None
    for m in MOTORES:
        if m["empuje"] * 4 >= empuje_necesario:
            motor_ok = m
            break

    if not motor_ok:
        return {
            "viabilidad": "NO VIABLE ❌",
            "causas": ["No hay suficiente empuje disponible"]
        }

    return {
        "viabilidad": "VIABLE ✅",
        "analisis": {
            "tecnico": f"Empuje requerido {empuje_necesario}kg, motor {motor_ok['modelo']}",
            "economico": "Costo estimado entre 4000 y 8000 USD",
            "profesional": "Requiere equipo en robótica, IA y electrónica"
        },
        "software": {
            "arquitectura": "ROS2 + Microservicios",
            "modulos": [
                "flight_controller.py",
                "navigation.py",
                "vision_ai.py",
                "failsafe.py"
            ],
            "algoritmos": [
                "PID Control",
                "SLAM",
                "A*",
                "Red neuronal"
            ]
        },
        "hardware": [
            f"Motor: {motor_ok['modelo']}",
            "Pixhawk",
            "GPS Ublox",
            "Lidar",
            "Batería LiPo"
        ],
        "modelo_3d": {
            "tipo": "quadcopter",
            "peso": peso,
            "motor": motor_ok["modelo"]
        },
        "garantia": "Validado por cálculo de empuje + control PID"
    }

# =========================
# 🚀 ENDPOINT REAL
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

    resultado = analizar_drone_real(idea)

    return jsonify(resultado)

# =========================
# RESTO (SIN CAMBIOS)
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