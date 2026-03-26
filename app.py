from flask import Flask, render_template, request, jsonify, send_file
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator

import os, json, time, threading, subprocess, zipfile, re, sys

print("🔥 MAIA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_secret_ultra"

init_db()
app.register_blueprint(proyectos_bp)

estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}

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
# 🧊 MOTOR 3D
# =========================
def generar_modelo_3d(base, peso):
    model_path = os.path.join(base, "models")
    os.makedirs(model_path, exist_ok=True)

    escala = max(1, peso / 5)

    obj = f"""o Drone
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

    stl = f"""solid drone
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
# 🧠 GENERADOR PROYECTO
# =========================
def crear_proyecto(nombre, peso, tipo="general"):
    nombre = nombre_seguro(nombre)
    base = f"maia_projects/{nombre}"
    os.makedirs(base, exist_ok=True)

    generar_archivo(f"{base}/config/config.json", json.dumps({
        "peso": peso,
        "tipo": tipo,
        "control": "PID"
    }, indent=4))

    generar_archivo(f"{base}/firmware/pid.py", """
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, target, current):
        error = target - current
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp*error + self.ki*self.integral + self.kd*derivative
""")

    generar_archivo(f"{base}/firmware/flight.py", """
from pid import PID

class FlightController:
    def __init__(self):
        self.pid = PID(1.2, 0.02, 0.1)
        self.altura = 0

    def update(self, objetivo):
        control = self.pid.compute(objetivo, self.altura)
        self.altura += control * 0.1
        return self.altura
""")

    generar_archivo(f"{base}/firmware/failsafe.py", """
class FailSafe:
    def check(self, bateria, gps):
        if bateria < 20:
            return "RETURN_HOME"
        if not gps:
            return "EMERGENCY_LAND"
        return "OK"
""")

    generar_archivo(f"{base}/main.py", """
from firmware.flight import FlightController
from firmware.failsafe import FailSafe

fc = FlightController()
fs = FailSafe()

for i in range(50):
    altura = fc.update(10)
    estado = fs.check(100, True)
    print(f"Altura: {altura:.2f} | Estado: {estado}")
""")

    generar_modelo_3d(base, peso)

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
        return result.stdout or result.stderr
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
# 🧠 CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        time.sleep(1)

    def ejecutar(self, idea):
        global resultado_global

        try:
            self.progreso(20, "Analizando idea...")
            core_data = analizar_drone(idea)

            analisis = core_data.get("analisis", {})
            fisica = core_data.get("fisica", {})

            self.progreso(50, "Validando...")
            validator = MaiaValidator()
            validacion = validator.validar(core_data)

            # 🔥 HARDWARE REAL
            hardware = [
                "Motores brushless",
                "ESC 30A",
                "Batería LiPo",
                "Controlador de vuelo (Pixhawk)",
                "GPS + IMU"
            ]

            # 🔥 SOFTWARE REAL
            software = {
                "arquitectura": [
                    "firmware/pid.py",
                    "firmware/flight.py",
                    "firmware/failsafe.py",
                    "config/config.json",
                    "main.py"
                ],
                "algoritmos": [
                    "Control PID",
                    "Simulación discreta",
                    "Failsafe automático"
                ]
            }

            # 🔥 DIAGNÓSTICO PRO
            if validacion["viabilidad"] == "VIABLE ✅":
                explicacion = f"""
Sistema viable:

- Empuje suficiente ({fisica.get("empuje")})
- Autonomía: {fisica.get("autonomia")} min
- Consumo optimizado

Diseño apto para prototipo real.
"""
            else:
                explicacion = f"""
Sistema NO viable:

Errores:
{chr(10).join(validacion["errores"])}

Soluciones:
{chr(10).join(validacion["soluciones"])}
"""

            self.progreso(75, "Generando sistema...")

            ruta = crear_proyecto(
                f"drone_{int(time.time())}",
                analisis.get("peso", 5)
            )

            salida = ejecutar_main(ruta)
            zip_path = exportar_zip(ruta)

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion["viabilidad"],
                "explicacion": explicacion,
                "analisis": analisis,
                "fisica": fisica,
                "errores": validacion["errores"],
                "soluciones": validacion["soluciones"],
                "software": software,
                "hardware": hardware,
                "modelo_3d": f"{ruta}/models/drone.obj",
                "salida": salida,
                "software_generado": ruta,
                "zip": zip_path
            }

            estado_maia["estado"] = "COMPLETADO"

        except Exception as e:
            resultado_global = {"error": str(e)}

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

    threading.Thread(target=proceso_maia, args=(idea,), daemon=True).start()

    return jsonify({"status": "ok"})

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/maia_capacidades")
def maia_capacidades():
    return jsonify({
        "fase": 16,
        "capacidades": [
            "Diseño de drones",
            "Software embebido",
            "Simulación",
            "Modelo 3D",
            "Hardware real",
            "Validación técnica"
        ]
    })

@app.route("/descargar_proyecto")
def descargar_proyecto():
    zip_path = resultado_global.get("zip")
    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    return "No disponible", 404

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
    app.run(host="0.0.0.0", port=port, threaded=True)
