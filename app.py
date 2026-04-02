from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
import os, time, zipfile, random

print("🔥 MAIA INDUSTRIAL CORE LEVEL 4 GOD MODE")

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
# 🧠 ANALISIS AVANZADO
# =========================
def analizar_viabilidad(idea):
    idea = idea.lower()
    score = 0
    problemas = []
    soluciones = []

    if "incendio" in idea:
        score += 3
    else:
        problemas.append("No enfocado a problema crítico")
        soluciones.append("Aplicar a incendios o rescate")

    if "autonom" in idea:
        score += 2
    else:
        problemas.append("Falta autonomía")
        soluciones.append("Implementar navegación autónoma")

    if "camara" in idea or "sensor" in idea:
        score += 2
    else:
        problemas.append("Sin percepción")
        soluciones.append("Agregar sensores térmicos")

    if score >= 7:
        estado = "ALTAMENTE VIABLE"
    elif score >= 4:
        estado = "VIABLE CON MEJORAS"
    else:
        estado = "NO VIABLE"

    return {
        "estado": estado,
        "score": score,
        "problemas": problemas,
        "soluciones": soluciones
    }

# =========================
# 🔩 HARDWARE NIVEL 4
# =========================
def generar_hardware(peso):
    return {
        "estructura": {
            "material": "carbon fiber aerospace",
            "tipo": "quad_x industrial"
        },
        "propulsion": {
            "motores": 4,
            "kv": 1200,
            "thrust_por_motor_kg": 6.5,
            "esc": "BLHeli_32 45A"
        },
        "controlador_vuelo": "Pixhawk",
        "energia": {
            "bateria": "LiPo 6S 10000mAh",
            "voltaje": 22.2
        },
        "carga_util": {
            "tipo": "retardante incendios",
            "capacidad_l": 5
        },
        "sensores": {
            "termico": True,
            "lidar": True,
            "gps": True,
            "imu": True
        },
        "peso_total": peso
    }

# =========================
# 💻 SOFTWARE NIVEL 4 REAL
# =========================
def generar_software(base):
    root = os.path.join(base, "software")

    estructura = {
        "main.py": """from core.system import DroneSystem

def main():
    drone = DroneSystem()
    drone.run()

if __name__ == "__main__":
    main()
""",

        "core": {
            "system.py": """from control.flight_controller import FlightController
from ai.brain import Brain
from mission.executor import Executor
from simulation.environment import Environment
from telemetry.stream import Telemetry
from core.event_bus import EventBus

class DroneSystem:
    def __init__(self):
        self.fc = FlightController()
        self.brain = Brain()
        self.executor = Executor()
        self.env = Environment()
        self.telemetry = Telemetry()
        self.bus = EventBus()

    def run(self):
        while True:
            sensors = self.env.update()
            decision = self.brain.process(sensors)
            control = self.fc.update(sensors, decision)
            state = self.executor.execute(decision)
            self.telemetry.send(state)

            if state["fire"]:
                self.bus.emit("FIRE_DETECTED")
"""
        },

        "core/event_bus.py": """class EventBus:
    def emit(self, event):
        print("EVENT:", event)
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
        self.prev_error = error
        return self.kp*error + self.ki*self.integral + self.kd*deriv
""",
            "flight_controller.py": """from control.pid import PID

class FlightController:
    def __init__(self):
        self.alt = PID(1.2,0.01,0.4)

    def update(self, sensors, decision):
        return {
            "throttle": self.alt.update(10, sensors["altitude"], 0.02)
        }
"""
        },

        "ai": {
            "brain.py": """class Brain:
    def process(self, sensors):
        if sensors["temperature"] > 70:
            return {"action":"EXTINGUISH"}
        if sensors["battery"] < 20:
            return {"action":"RETURN"}
        return {"action":"PATROL"}
"""
        },

        "mission": {
            "executor.py": """import random

class Executor:
    def __init__(self):
        self.x=0
        self.y=0

    def execute(self, decision):
        self.x += random.uniform(0,1)
        self.y += random.uniform(0,1)

        return {
            "x": self.x,
            "y": self.y,
            "z": 10,
            "battery": random.randint(40,100),
            "fire": random.choice([True, False]),
            "action": decision["action"]
        }
"""
        },

        "telemetry": {
            "stream.py": """class Telemetry:
    def send(self, state):
        print("TELEMETRY:", state)
"""
        },

        "simulation": {
            "environment.py": """import random

class Environment:
    def update(self):
        return {
            "altitude": 10,
            "temperature": random.randint(20,100),
            "battery": random.randint(20,100)
        }
"""
        },

        "logs": {
            "system_log.py": """def log(msg):
    print("LOG:", msg)
"""
        }
    }

    def crear(ruta, contenido):
        if isinstance(contenido, dict):
            for k,v in contenido.items():
                crear(os.path.join(ruta,k), v)
        else:
            write_file(ruta, contenido)

    crear(root, estructura)
    return estructura

# =========================
# FISICA
# =========================
def calcular_fisica(peso):
    thrust = 26
    relacion = thrust / peso
    return {
        "thrust_total": thrust,
        "relacion": round(relacion,2),
        "estado": "ESTABLE" if relacion > 2 else "INESTABLE"
    }

# =========================
# TELEMETRIA
# =========================
def generar_telemetria():
    return {
        "variables": ["x","y","z","battery","fire"],
        "frecuencia_hz": 10
    }

# =========================
# MODELO 3D
# =========================
def generar_modelo_3d(base, peso):
    return {
        "tipo": "quad_x industrial",
        "escala": peso
    }

# =========================
# CORE
# =========================
class MaiaCore:
    def ejecutar_paso(self, idea, paso, data):

        if paso == 0:
            return {"paso":1,"data":{
                "core": analizar_drone(idea),
                "viabilidad": analizar_viabilidad(idea)
            }}

        elif paso == 1:
            data["hardware"] = generar_hardware(12)
            return {"paso":2,"data":data}

        elif paso == 2:
            base = f"maia_projects/{int(time.time())}"
            os.makedirs(base,exist_ok=True)
            data["base"] = base
            data["software"] = generar_software(base)
            return {"paso":3,"data":data}

        elif paso == 3:
            data["fisica"] = calcular_fisica(data["hardware"]["peso_total"])
            data["telemetria"] = generar_telemetria()
            return {"paso":4,"data":data}

        elif paso == 4:
            data["riesgos"] = ["viento extremo","fallo bateria","perdida señal"]
            return {"paso":5,"data":data}

        elif paso == 5:
            data["modelo_3d"] = generar_modelo_3d(data["base"], data["hardware"]["peso_total"])
            return {"paso":6,"data":data}

        elif paso == 6:
            data["zip"] = exportar_zip(data["base"])
            data["nivel_maia"] = "NIVEL 4 - AUTONOMOUS SYSTEM"
            return {"final":True,"resultado":data}

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
# API
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    req = request.get_json() or {}
    core = MaiaCore()
    return jsonify(core.ejecutar_paso(
        req.get("idea",""),
        int(req.get("paso",0)),
        req.get("data",{})
    ))

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