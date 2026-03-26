from flask import Flask, render_template, request, jsonify, send_file
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator

import os
import json
from datetime import datetime
import time
import threading
import subprocess
import zipfile
import re
import sys

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
estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}
RESULT_FILE = "maia_resultado.json"

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
# 🔥 GENERADOR 3D REAL
# =========================
def generar_modelo_3d(base, peso, tipo):
    model_path = os.path.join(base, "models")
    os.makedirs(model_path, exist_ok=True)

    escala = max(1, peso / 5)

    obj = f"""
o Drone
v 0 0 0
v {escala} 0 0
v {escala} {escala} 0
v 0 {escala} 0
v 0 0 {escala}
v {escala} 0 {escala}
v {escala} {escala} {escala}
v 0 {escala} {escala}
f 1 2 3 4
f 5 6 7 8
"""
    stl = f"""
solid drone
facet normal 0 0 0
outer loop
vertex 0 0 0
vertex {escala} 0 0
vertex {escala} {escala} 0
endloop
endfacet
endsolid drone
"""

    generar_archivo(f"{model_path}/drone.obj", obj)
    generar_archivo(f"{model_path}/drone.stl", stl)

# =========================
# 🔥 CREAR PROYECTO PRO
# =========================
def crear_proyecto(nombre, peso, tipo="general"):
    nombre = nombre_seguro(nombre)
    base = f"maia_projects/{nombre}"
    os.makedirs(base, exist_ok=True)

    # CONFIG
    generar_archivo(f"{base}/config/drone_config.json", json.dumps({
        "peso": peso,
        "tipo": tipo,
        "motores": 4,
        "control": "PID"
    }, indent=4))

    # PID
    generar_archivo(f"{base}/firmware/pid_controller.py", """
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, measured):
        error = setpoint - measured
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp*error + self.ki*self.integral + self.kd*derivative
""")

    # FLIGHT CONTROLLER
    generar_archivo(f"{base}/firmware/flight_controller.py", """
from pid_controller import PID

class FlightController:
    def __init__(self):
        self.pid = PID(1.0, 0.01, 0.1)
        self.altura = 0

    def update(self, objetivo, actual):
        control = self.pid.compute(objetivo, actual)
        self.altura += control * 0.1
        return self.altura
""")

    # FAILSAFE
    generar_archivo(f"{base}/firmware/failsafe.py", """
class FailSafe:
    def check(self, bateria, gps):
        if bateria < 20:
            return "RETURN_HOME"
        if not gps:
            return "EMERGENCY_LAND"
        return "OK"
""")

    # MAIN
    generar_archivo(f"{base}/main.py", f"""
from firmware.flight_controller import FlightController
from firmware.failsafe import FailSafe

fc = FlightController()
fs = FailSafe()

altura = 0

for i in range(50):
    altura = fc.update(10, altura)
    estado = fs.check(100, True)
    print(f"Altura: {{altura:.2f}} | Estado: {{estado}}")
""")

    # MODELO 3D
    generar_modelo_3d(base, peso, tipo)

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
            timeout=5
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

def exportar_zip(ruta):
    zip_path = ruta + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(ruta):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, ruta))
    return zip_path

# =========================
# CORE MAIA
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        print(f"🧠 {val}% - {msg}")
        time.sleep(1)

    def ejecutar(self, idea):
        global resultado_global

        try:
            print("🔥 Ejecutando MAIA:", idea)

            # CAPA 1
            self.progreso(20, "🧠 Analizando idea...")
            core_data = analizar_drone(idea)

            analisis = core_data.get("analisis", {})
            fisica = core_data.get("fisica", {})

            # CAPA 2
            self.progreso(50, "⚖️ Validando...")
            validator = MaiaValidator()
            validacion = validator.validar(core_data)

            # CAPA 3
            self.progreso(75, "💻 Generando sistema...")
            ruta = crear_proyecto(
                f"drone_{int(time.time())}",
                analisis.get("peso", 5),
                analisis.get("tipo", "general")
            )

            salida = ejecutar_main(ruta)
            zip_path = exportar_zip(ruta)

            self.progreso(100, "✅ Completado")

            resultado_global = {
                "viabilidad": validacion["viabilidad"],
                "analisis": analisis,
                "fisica": fisica,
                "errores": validacion["errores"],
                "soluciones": validacion["soluciones"],
                "salida": salida,
                "software_generado": ruta,
                "zip": zip_path
            }

        except Exception as e:
            resultado_global = {"viabilidad": "ERROR ❌", "error": str(e)}

# =========================
# THREAD
# =========================
def proceso_maia(idea):
    MaiaCore().ejecutar(idea)

# =========================
# ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    estado_maia["progreso"] = 0
    estado_maia["mensaje"] = "Iniciando..."
    estado_maia["estado"] = "PROCESANDO"

    threading.Thread(target=proceso_maia, args=(idea,), daemon=True).start()
    return jsonify({"status": "ok"})

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/descargar_proyecto")
def descargar_proyecto():
    zip_path = resultado_global.get("zip")
    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return "No disponible", 404

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
