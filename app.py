from flask import Flask, render_template, request, jsonify, session, send_file
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime

# 🔥 PROTECCIÓN IMPORTS PESADOS
try:
    from bs4 import BeautifulSoup
except:
    BeautifulSoup = None

import math

try:
    import numpy as np
except:
    np = None

import time
import threading
import subprocess
import zipfile
import re
import sys

# 🔥 PROTECCIÓN TRIMESH
try:
    import trimesh
except:
    trimesh = None

print("🔥 MAIA STARTING...")

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
# ESTADO GLOBAL
# =========================
estado_maia = {
    "progreso": 0,
    "estado": "IDLE",
    "mensaje": ""
}

resultado_global = {}

# =========================
# MEMORIA
# =========================
MEMORY_FILE = "maia_memory.json"

def cargar_memoria():
    try:
        if not os.path.exists(MEMORY_FILE):
            return {"proyectos": []}
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"proyectos": []}

def guardar_memoria(memoria):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memoria, f, indent=4)
    except:
        pass

def registrar_proyecto(data):
    memoria = cargar_memoria()
    memoria["proyectos"].append(data)
    guardar_memoria(memoria)

# =========================
# UTILIDADES
# =========================
def nombre_seguro(nombre):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nombre)

def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

# =========================
# CREAR PROYECTO
# =========================
def crear_proyecto(nombre, peso):
    nombre = nombre_seguro(nombre)
    base = f"maia_projects/{nombre}"
    os.makedirs(base, exist_ok=True)

    generar_archivo(f"{base}/flight_controller.py", f"""
class FlightController:
    def __init__(self):
        self.altura = 0
        self.velocidad = 0

    def update(self, thrust, peso):
        g = 9.81
        fuerza = thrust - peso * g
        aceleracion = fuerza / peso
        self.velocidad += aceleracion * 0.1
        self.altura += self.velocidad * 0.1
        return self.altura
""")

    generar_archivo(f"{base}/failsafe.py", """
class FailSafe:
    def check(self, bateria, gps):
        if bateria < 20:
            return "RETURN_HOME"
        if not gps:
            return "EMERGENCY_LAND"
        return "OK"
""")

    generar_archivo(f"{base}/main.py", f"""
from flight_controller import FlightController
from failsafe import FailSafe

fc = FlightController()
fs = FailSafe()

peso = {peso}
thrust = peso * 2

for i in range(50):
    altura = fc.update(thrust, peso)
    estado = fs.check(100, True)
    print(f"Altura: {{altura:.2f}} | Estado: {{estado}}")
""")

    return base

# =========================
# EJECUCIÓN
# =========================
def ejecutar_main(ruta):
    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=ruta,
            capture_output=True,
            text=True,
            timeout=3
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

# =========================
# ZIP
# =========================
def exportar_zip(ruta):
    zip_path = ruta + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(ruta):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, ruta))
    return zip_path

# =========================
# CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        print(f"🧠 {val}% - {msg}")
        time.sleep(0.2)

    def analizar(self, idea):
        self.progreso(10, "Analizando IA...")
        idea = idea.lower()

        peso = 5
        tipo = "general"

        if "incendio" in idea:
            peso += 6
            tipo = "emergencia"

        if "mineria" in idea:
            peso += 4
            tipo = "industrial"

        if "seguridad" in idea:
            peso += 2
            tipo = "vigilancia"

        return {"peso": peso, "tipo": tipo}

    def ejecutar(self, idea):
        global resultado_global

        try:
            print("🔥 Ejecutando MAIA:", idea)

            analisis = self.analizar(idea)

            self.progreso(40, "Generando proyecto...")
            ruta = crear_proyecto(f"drone_{int(time.time())}", analisis["peso"])

            self.progreso(70, "Simulando...")
            salida = ejecutar_main(ruta)

            zip_path = exportar_zip(ruta)

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": "VIABLE ✅",
                "analisis": analisis,
                "salida": salida,
                "software_generado": ruta,
                "zip": zip_path
            }

        except Exception as e:
            print("💥 ERROR:", str(e))
            resultado_global = {
                "viabilidad": "ERROR ❌",
                "error": str(e)
            }

# =========================
# THREAD
# =========================
def proceso_maia(idea):
    core = MaiaCore()
    core.ejecutar(idea)

# =========================
# 🔥 ENDPOINT REAL DINÁMICO
# =========================
@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    try:
        carpeta = os.path.join("templates", "drones")

        if not os.path.exists(carpeta):
            print("❌ Carpeta drones no existe")
            return jsonify([])

        archivos = os.listdir(carpeta)

        drones = []

        for archivo in archivos:
            if archivo.endswith(".html"):
                nombre = archivo.replace(".html", "").replace("_", " ").title()
                ruta = f"/static/drones/{archivo}"

                drones.append({
                    "nombre": nombre,
                    "ruta": ruta
                })

        print("✅ Drones encontrados:", len(drones))
        return jsonify(drones)

    except Exception as e:
        print("💥 ERROR drones:", str(e))
        return jsonify([])

# =========================
# VOZ
# =========================
@app.route("/maia_voz", methods=["POST"])
def maia_voz():
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta", "")
    return jsonify({"respuesta": f"MAIA responde a: {pregunta}"})

@app.route("/maia_chat")
def maia_chat():
    return "<h2>💬 Chat MAIA próximamente</h2>"

# =========================
# ENDPOINTS BASE
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    if len(idea.strip()) < 3:
        return jsonify({"error": "Idea muy corta"})

    threading.Thread(target=proceso_maia, args=(idea,)).start()
    return jsonify({"status": "ok"})

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/descargar_proyecto")
def descargar_proyecto():
    zip_path = resultado_global.get("zip")

    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)

    return "No disponible", 404

@app.route("/guardar_proyecto", methods=["POST"])
def guardar_proyecto():
    try:
        data = request.get_json(silent=True) or {}

        registrar_proyecto({
            "nombre": data.get("nombre", "Drone MAIA"),
            "tipo": data.get("tecnologia", "general"),
            "fecha": datetime.now().isoformat()
        })

        return jsonify({"status": "guardado"})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/maia_capacidades")
def maia_capacidades():
    return jsonify({
        "fase": 13,
        "capacidades": [
            "Capa 1 → Interfaz",
            "Capa 2 → Backend",
            "Capa 3 → IA",
            "Simulación",
            "Memoria"
        ]
    })

@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 MAIA corriendo en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)