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
# 🔒 LOCK GLOBAL
# =========================
lock_maia = threading.Lock()

# =========================
# 🔥 ESTADO GLOBAL
# =========================
estado_maia = {
    "progreso": 0,
    "estado": "IDLE",
    "mensaje": ""
}

resultado_global = {}

# =========================
# 🧠 MEMORIA MAIA
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
# LOGGER
# =========================
def log_event(tipo, mensaje):
    print(f"🧠 [{tipo}] {mensaje}")

# =========================
# SANITIZAR
# =========================
def nombre_seguro(nombre):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nombre)

# =========================
# GENERADOR ARCHIVOS
# =========================
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
# VALIDACIÓN
# =========================
def validar_proyecto(ruta):
    errores = []
    for archivo in os.listdir(ruta):
        if archivo.endswith(".py"):
            ruta_archivo = os.path.join(ruta, archivo)
            try:
                subprocess.run(
                    [sys.executable, "-m", "py_compile", ruta_archivo],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                errores.append(e.stderr)
    return errores

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
            timeout=5
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
# ANÁLISIS NEGATIVO
# =========================
def generar_analisis_negativo(idea):
    return f"""La idea '{idea}' presenta limitaciones críticas:
- Relación peso/empuje insuficiente
- Riesgo de inestabilidad en vuelo
- Consumo energético elevado
💡 Recomendaciones:
- Reducir peso estructural
- Incrementar potencia de motores
- Optimizar aerodinámica
- Redefinir misión del drone"""

# =========================
# CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        with lock_maia:
            estado_maia["progreso"] = val
            estado_maia["mensaje"] = msg
            estado_maia["estado"] = "PROCESANDO"
        log_event("PROGRESO", f"{val}% - {msg}")
        time.sleep(0.2)

    def analizar(self, idea):
        self.progreso(10, "Analizando con IA")

        memoria = cargar_memoria()
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

        proyectos = memoria["proyectos"]

        if proyectos:
            try:
                promedio = sum(p["peso"] for p in proyectos if p.get("peso")) / len(proyectos)
                if promedio > 8:
                    peso -= 1
                else:
                    peso += 1
            except:
                pass

        return {"peso": peso, "tipo": tipo}

    def ejecutar(self, idea):
        try:
            print("🔥 Ejecutando MAIA con idea:", idea)

            analisis = self.analizar(idea)

            if analisis["peso"] > 30:
                return {
                    "viabilidad": "NO VIABLE ❌",
                    "analisis": analisis,
                    "error": generar_analisis_negativo(idea)
                }

            self.progreso(30, "Generando software")
            nombre = f"drone_{int(time.time())}"
            ruta = crear_proyecto(nombre, analisis["peso"])

            self.progreso(50, "Validando código")
            errores = validar_proyecto(ruta)

            self.progreso(70, "Ejecutando simulación")
            salida = ejecutar_main(ruta)

            self.progreso(85, "Empaquetando")
            zip_path = exportar_zip(ruta)

            self.progreso(100, "Completado")

            registrar_proyecto({
                "idea": idea,
                "tipo": analisis["tipo"],
                "peso": analisis["peso"],
                "viabilidad": "VIABLE"
            })

            return {
                "viabilidad": "VIABLE ✅" if not errores else "REVISAR ⚠️",
                "analisis": analisis,
                "errores": errores,
                "salida": salida,
                "software_generado": ruta,
                "zip": zip_path
            }

        except Exception as e:
            print("💥 ERROR MAIA:", str(e))
            return {
                "viabilidad": "ERROR ❌",
                "error": str(e)
            }

# =========================
# PROCESO ASYNC
# =========================
def proceso_maia(idea):
    global resultado_global

    with lock_maia:
        estado_maia["progreso"] = 0
        estado_maia["estado"] = "INICIANDO"
        estado_maia["mensaje"] = "Arrancando IA..."

    core = MaiaCore()
    resultado = core.ejecutar(idea)

    with lock_maia:
        resultado_global = resultado

# =========================
# ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    if len(idea.strip()) < 5:
        return jsonify({"error": "Idea insuficiente"})

    hilo = threading.Thread(target=proceso_maia, args=(idea,))
    hilo.start()

    return jsonify({"status": "procesando"})

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/ping")
def ping():
    return "OK MAIA"

@app.route("/descargar_proyecto")
def descargar_proyecto():
    zip_path = resultado_global.get("zip")
    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return "No disponible", 404

@app.route("/maia_capacidades")
def maia_capacidades():
    return jsonify({
        "fase": 13,
        "capacidades": [
            "Capa 1 → Interfaz (UI)",
            "Capa 2 → API Flask",
            "Capa 3 → Núcleo Inteligente",
            "Simulación de drones",
            "Aprendizaje automático básico",
            "Memoria persistente"
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
    try:
        port = int(os.environ.get("PORT", 10000))
        print(f"🚀 MAIA corriendo en puerto {port}")
        app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
    except Exception as e:
        print("💥 ERROR INICIANDO MAIA:", str(e))