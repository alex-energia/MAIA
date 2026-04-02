from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
import os
import time
import zipfile
import math

print("🔥 MAIA INDUSTRIAL CORE LEVEL 3")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

# =========================
# NO CACHE
# =========================
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

init_db()
app.register_blueprint(proyectos_bp)

# =========================
# FILE WRITER
# =========================
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# =========================
# 🧠 ANALISIS AVANZADO REAL
# =========================
def analizar_viabilidad(idea):
    idea = idea.lower()

    score = 0
    problemas = []
    soluciones = []

    if "incendio" in idea:
        score += 3
    else:
        problemas.append("No enfocado a problema crítico real")
        soluciones.append("Aplicar a emergencias (incendios, rescate, vigilancia)")

    if "autonom" in idea:
        score += 2
    else:
        problemas.append("Falta autonomía inteligente")
        soluciones.append("Implementar navegación autónoma con IA")

    if "camara" in idea or "sensor" in idea:
        score += 2
    else:
        problemas.append("Falta percepción del entorno")
        soluciones.append("Agregar sensores térmicos / LIDAR / visión")

    if "carga" in idea or "agua" in idea:
        score += 2
    else:
        soluciones.append("Agregar sistema de carga útil (extinción o logística)")

    if score >= 7:
        estado = "ALTAMENTE VIABLE"
    elif score >= 4:
        estado = "VIABLE CON MEJORAS"
    else:
        estado = "NO VIABLE"

    return {
        "estado": estado,
        "score": score,
        "problemas_detectados": problemas,
        "soluciones_propuestas": soluciones,
        "analisis": f"Evaluación técnica basada en misión, autonomía, percepción y carga útil."
    }

# =========================
# 💻 SOFTWARE INDUSTRIAL NIVEL 3
# =========================
def generar_software(base):
    root = os.path.join(base, "software")

    estructura = {
        "main.py": """from control.flight_controller import FlightController
from navigation.a_star import AStar
from perception.fire_detection import FireDetector
from systems.failsafe import FailSafe
from simulation.environment import Environment

def main():
    fc = FlightController()
    nav = AStar()
    vision = FireDetector()
    fs = FailSafe()
    env = Environment()

    while True:
        sensors = env.update()

        control = fc.update(sensors, 0.02)
        path = nav.find_path((0,0),(10,10))
        fire = vision.detect(sensors["temperature"])

        status = fs.check(sensors["battery"], sensors["signal"])

        if status != "OK":
            fc.return_home()

if __name__ == "__main__":
    main()
""",

        "control": {
            "pid.py": """class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0

    def update(self, setpoint, measured, dt):
        error = setpoint - measured
        self.integral += error * dt
        deriv = (error - self.prev_error) / dt if dt > 0 else 0

        output = self.kp * error + self.ki * self.integral + self.kd * deriv
        self.prev_error = error

        return output
""",
            "flight_controller.py": """from control.pid import PID

class FlightController:
    def __init__(self):
        self.alt = PID(1.2, 0.01, 0.4)
        self.roll = PID(0.8, 0.02, 0.3)
        self.pitch = PID(0.8, 0.02, 0.3)

    def update(self, sensors, dt):
        return {
            "throttle": self.alt.update(10, sensors["altitude"], dt),
            "roll": self.roll.update(0, sensors["roll"], dt),
            "pitch": self.pitch.update(0, sensors["pitch"], dt)
        }

    def return_home(self):
        print("🚨 RETURN HOME ACTIVATED")
"""
        },

        "navigation": {
            "a_star.py": """import heapq

class AStar:
    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def find_path(self, start, goal):
        open_set = [(0, start)]
        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return ["PATH_OK"]

            visited.add(current)

            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                neighbor = (current[0]+dx, current[1]+dy)

                if neighbor in visited:
                    continue

                priority = self.heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))

        return []
"""
        },

        "perception": {
            "fire_detection.py": """class FireDetector:
    def detect(self, temp):
        if temp > 70:
            return {"fire": True, "confidence": 0.97}
        return {"fire": False}
"""
        },

        "systems": {
            "failsafe.py": """class FailSafe:
    def check(self, battery, signal):
        if battery < 20:
            return "LOW_BATTERY"
        if not signal:
            return "SIGNAL_LOSS"
        return "OK"
"""
        },

        "simulation": {
            "environment.py": """import random

class Environment:
    def __init__(self):
        self.wind = 5
        self.temperature = 30

    def update(self):
        return {
            "altitude": 10,
            "roll": random.uniform(-0.2,0.2),
            "pitch": random.uniform(-0.2,0.2),
            "temperature": self.temperature,
            "battery": 80,
            "signal": True
        }
"""
        }
    }

    def crear(ruta, contenido):
        if isinstance(contenido, dict):
            for k, v in contenido.items():
                crear(os.path.join(ruta, k), v)
        else:
            write_file(ruta, contenido)

    crear(root, estructura)
    return estructura

# =========================
# HARDWARE
# =========================
def generar_hardware(peso):
    return {
        "estructura": "carbon fiber aerospace",
        "propulsion": {
            "motores": 4,
            "kv": 1200,
            "thrust_por_motor_kg": 6.5
        },
        "energia": {
            "bateria": "LiPo 6S 10000mAh",
            "voltaje": 22.2
        },
        "sensores": ["thermal","lidar","gps","imu"],
        "peso_total": peso
    }

# =========================
# FISICA
# =========================
def calcular_fisica(peso):
    thrust_total = 26
    relacion = thrust_total / peso
    return {
        "thrust_total": thrust_total,
        "relacion": round(relacion,2),
        "estado": "ESTABLE" if relacion>2 else "INESTABLE",
        "autonomia": round(40 - peso*0.5,2)
    }

# =========================
# TELEMETRIA
# =========================
def generar_telemetria():
    return {
        "protocolo": "MAVLink",
        "frecuencia_hz": 10,
        "datos": ["gps","imu","battery","altitude"]
    }

# =========================
# COMUNICACIONES
# =========================
def generar_comunicaciones():
    return {
        "tipo": "RF + LTE",
        "alcance_km": 15,
        "latencia_ms": 120
    }

# =========================
# MODELO 3D MEJORADO
# =========================
def generar_modelo_3d(base, peso):
    path = os.path.join(base,"models")
    os.makedirs(path,exist_ok=True)

    size = peso

    write_file(os.path.join(path,"drone.obj"), f"""
o drone
v {-size} 0 {-size}
v {size} 0 {-size}
v {size} 0 {size}
v {-size} 0 {size}
v 0 {size} 0
""")

    return {
        "tipo":"quad_x industrial",
        "detalle":"modelo base exportable CAD",
        "escala": size
    }

# =========================
# ZIP
# =========================
def exportar_zip(path):
    zip_path = path + ".zip"
    with zipfile.ZipFile(zip_path,'w') as zipf:
        for root,_,files in os.walk(path):
            for f in files:
                full=os.path.join(root,f)
                zipf.write(full, os.path.relpath(full,path))
    return zip_path

# =========================
# CORE
# =========================
class MaiaCore:

    def ejecutar_paso(self, idea, paso, data):

        if paso == 0:
            core = analizar_drone(idea)
            viabilidad = analizar_viabilidad(idea)

            return {"paso":1,"data":{
                "core":core,
                "viabilidad":viabilidad
            }}

        elif paso == 1:
            analisis = data["core"].get("analisis",{})
            peso = analisis.get("peso",12)

            data["hardware"] = generar_hardware(peso)
            data["analisis_pro"] = analisis

            return {"paso":2,"data":data}

        elif paso == 2:
            base = f"maia_projects/{int(time.time())}"
            os.makedirs(base,exist_ok=True)

            data["base"] = base
            data["software"] = generar_software(base)

            return {"paso":3,"data":data}

        elif paso == 3:
            peso = data["hardware"]["peso_total"]

            data["fisica"] = calcular_fisica(peso)
            data["telemetria"] = generar_telemetria()
            data["comunicaciones"] = generar_comunicaciones()

            return {"paso":4,"data":data}

        elif paso == 4:
            data["riesgos"] = [
                "viento extremo",
                "fallo bateria",
                "perdida señal",
                "sobrecalentamiento"
            ]
            return {"paso":5,"data":data}

        elif paso == 5:
            peso = data["hardware"]["peso_total"]
            data["modelo_3d"] = generar_modelo_3d(data["base"], peso)

            return {"paso":6,"data":data}

        elif paso == 6:
            data["zip"] = exportar_zip(data["base"])
            data["nivel_maia"] = "NIVEL 3 - INDUSTRIAL GOD MODE"

            return {"final":True,"resultado":data}

# =========================
# API
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    req = request.get_json() or {}
    idea = req.get("idea","")
    paso = int(req.get("paso",0))
    data = req.get("data",{})

    core = MaiaCore()
    return jsonify(core.ejecutar_paso(idea,paso,data))

# =========================
# VISTAS
# =========================
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
    app.run(host="0.0.0.0", port=10000)