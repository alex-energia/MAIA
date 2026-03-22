from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

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
# 🔥 CARGA DRONES (PROTEGIDA)
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
                "categoria": categoria,
                "introduccion": f"Descripción completa de {titulo}.",
                "viabilidad": "Alta viabilidad para aplicaciones específicas.",
                "software": [
                    "Control inteligente via MAIA App",
                    "Detección automática de obstáculos",
                    "Modo seguimiento y selfie",
                    "Grabación de video HD"
                ],
                "hardware": [
                    "Motores brushless",
                    "Batería de larga duración",
                    "Cámara integrada 12MP",
                    "Sensores de proximidad y GPS",
                    "LEDs de iluminación"
                ]
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
# 🧠 MEMORIA PERSISTENTE (JSON REAL)
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
# 🧠 GUARDAR PROYECTO COMPLETO
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
# 📂 VER MEMORIA
# =========================
@app.route("/maia_memoria")
def maia_memoria():
    return jsonify(cargar_memoria())

@app.route("/maia_memoria_view")
def maia_memoria_view():
    return render_template("maia_memoria.html")

# =========================
# 🚀 MAIA INVENT (INGENIERÍA TOTAL)
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    if len(idea.strip()) < 5:
        return jsonify({
            "viabilidad": "NO VIABLE ❌",
            "causas": [
                "Idea poco definida",
                "No hay objetivo claro",
                "Falta enfoque técnico"
            ]
        })

    resultado = {
        "viabilidad": "VIABLE ✅",
        "analisis": {
            "tecnico": "Sistema realizable con sensores, IA y control autónomo.",
            "economico": "Costo medio, escalable según producción.",
            "profesional": "Alta aplicación en industria, seguridad o medio ambiente."
        },
        "software": {
            "modulos": [
                "Control de vuelo PID",
                "Sistema GPS inteligente",
                "Visión artificial con OpenCV",
                "IA de navegación autónoma",
                "Comunicación con MAIA"
            ],
            "algoritmos": [
                "SLAM",
                "A* Pathfinding",
                "Red neuronal",
                "Control adaptativo"
            ]
        },
        "hardware": [
            "Frame de carbono",
            "Motores brushless",
            "ESC 40A",
            "Controlador Pixhawk",
            "GPS Ublox",
            "Lidar",
            "Cámara HD",
            "Batería LiPo"
        ],
        "modelo_3d": "Drone tipo quadcopter modular con sensores frontales.",
        "garantia": "Sistema funcional basado en control PID + sensores + IA."
    }

    return jsonify(resultado)

# =========================
# TEST
# =========================
@app.route("/ping")
def ping():
    return "OK", 200

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# API DRONES
# =========================
@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    categoria = request.args.get("categoria")
    if categoria:
        return jsonify([d for d in DRONES_BASE if d["categoria"] == categoria])
    return jsonify(DRONES_BASE)

# =========================
# MEMORIA CHAT
# =========================
def obtener_memoria_chat():
    if "historial" not in session:
        session["historial"] = []
    return session["historial"]

def guardar_memoria_chat(pregunta, respuesta):
    historial = obtener_memoria_chat()
    historial.append({"pregunta": pregunta, "respuesta": respuesta})
    if len(historial) > 10:
        historial.pop(0)
    session["historial"] = historial

# =========================
# VOZ
# =========================
@app.route("/maia_voz", methods=["POST"])
def maia_voz():
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta", "")

    respuesta = f"MAIA IA: análisis avanzado para -> {pregunta}"

    guardar_memoria_chat(pregunta, respuesta)
    return jsonify({"respuesta": respuesta})

# =========================
# MÓDULOS
# =========================
@app.route("/maia_simulador")
def maia_simulador():
    return render_template("maia_simulador.html")

@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_lab")
def maia_lab():
    return render_template("maia_lab.html")

@app.route("/maia_architect")
def maia_architect():
    return render_template("maia_architect.html")

@app.route("/maia_ganado")
def maia_ganado():
    return render_template("maia_ganado.html")

@app.route("/maia_plantas")
def maia_plantas():
    return render_template("maia_plantas.html")

@app.route("/maia_traductor")
def maia_traductor():
    return render_template("maia_traductor.html")

@app.route("/maia_proyectos")
def maia_proyectos():
    return render_template("proyectos.html")

# =========================
# CHAT
# =========================
@app.route("/maia_chat")
def maia_chat():
    return render_template("maia_chat.html")

# =========================
# DRONES
# =========================
@app.route("/drones/<drone_file>")
def abrir_drone(drone_file):
    ruta_html = f"drones/{drone_file}.html"
    if os.path.exists(os.path.join(app.template_folder, ruta_html)):
        return render_template(ruta_html)
    return "Drone no encontrado", 404

# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)