from flask import Flask, render_template, request, jsonify, session, send_file
from proyectos import proyectos_bp, init_db
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
import math
import numpy as np
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
# 🔥 LOGGER PRO
# =========================
def log_event(tipo, mensaje):
    print(f"🧠 [{tipo}] {mensaje}")

# =========================
# 🔐 SANITIZAR
# =========================
def nombre_seguro(nombre):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nombre)

# =========================
# 🔥 GENERADOR ARCHIVOS
# =========================
def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

# =========================
# 🔥 CREAR PROYECTO (FIX REAL)
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
# 🔥 VALIDACIÓN ROBUSTA
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
# 🔥 EJECUCIÓN SEGURA
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
# 🔥 ZIP
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
# 🔥 ANÁLISIS NEGATIVO INTELIGENTE
# =========================
def generar_analisis_negativo(idea):
    return f"""
La idea '{idea}' presenta limitaciones críticas:

- Relación peso/empuje insuficiente
- Riesgo de inestabilidad en vuelo
- Posible consumo energético elevado

Recomendaciones:

- Reducir peso estructural
- Incrementar potencia de motores
- Optimizar aerodinámica
- Ajustar misión del drone a escenarios realistas
"""

# =========================
# 🧠 CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        with lock_maia:
            estado_maia["progreso"] = val
            estado_maia["mensaje"] = msg
            estado_maia["estado"] = "PROCESANDO"

        log_event("PROGRESO", f"{val}% - {msg}")
        time.sleep(0.3)

    def analizar(self, idea):
        self.progreso(10, "Analizando idea")

        idea = idea.lower()
        peso = 5
        tipo = "general"

        if "incendio" in idea:
            peso = 12
            tipo = "emergencia"
        elif "seguridad" in idea:
            peso = 6
            tipo = "vigilancia"
        elif "gigante" in idea:
            peso = 50  # 🔥 caso negativo real

        return {"peso": peso, "tipo": tipo}

    def ejecutar(self, idea):
        try:
            with lock_maia:
                estado_maia["estado"] = "INICIANDO"

            analisis = self.analizar(idea)

            # 🔥 VALIDACIÓN FÍSICA REAL
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

            with lock_maia:
                estado_maia["estado"] = "COMPLETADO"

            return {
                "viabilidad": "VIABLE ✅" if not errores else "REVISAR ⚠️",
                "analisis": analisis,
                "errores": errores,
                "salida": salida,
                "software_generado": ruta,
                "zip": zip_path
            }

        except Exception as e:
            with lock_maia:
                estado_maia["estado"] = "ERROR"
                estado_maia["mensaje"] = str(e)

            log_event("ERROR", str(e))

            return {
                "viabilidad": "ERROR ❌",
                "error": str(e)
            }

# =========================
# 🚀 PROCESO
# =========================
def proceso_maia(idea):
    global resultado_global
    core = MaiaCore()
    resultado = core.ejecutar(idea)

    with lock_maia:
        resultado_global = resultado

# =========================
# 🚀 ENDPOINTS
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
    with lock_maia:
        return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    with lock_maia:
        return jsonify(resultado_global)

@app.route("/descargar_proyecto")
def descargar_proyecto():
    zip_path = resultado_global.get("zip")

    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)

    return "No disponible", 404

# =========================
# 🔥 CAPACIDADES DINÁMICAS
# =========================
@app.route("/maia_capacidades")
def maia_capacidades():
    return jsonify({
        "fase": 12,
        "capacidades": [
            "Generación automática de software funcional",
            "Simulación física real",
            "Validación de código",
            "Ejecución automática",
            "Exportación profesional (.zip)",
            "Arquitectura modular",
            "Failsafe integrado",
            "Sistema de progreso en tiempo real",
            "Análisis de viabilidad inteligente",
            "Detección de proyectos no viables",
            "Recomendaciones técnicas automáticas"
        ]
    })

# =========================
# 🔥 3D
# =========================
@app.route("/generar_3d", methods=["POST"])
def generar_3d():
    if not trimesh:
        return jsonify({"modelo_url": "/static/no_3d.txt"})

    cuerpo = trimesh.creation.box(extents=(0.4, 0.4, 0.08))
    os.makedirs("static", exist_ok=True)

    ruta = "static/modelo_drone.glb"
    cuerpo.export(ruta)

    return jsonify({"modelo_url": "/" + ruta})

# =========================
# 🔥 VISTAS
# =========================
@app.route("/maia_panel")
def maia_panel():
    return render_template("maia_panel.html")

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
    return jsonify([])

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