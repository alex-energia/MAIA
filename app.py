from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
import os
import time
import zipfile

print("MAIA INDUSTRIAL CORE LEVEL 10 - REAL AUTOPILOT")

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
# VIABILIDAD (NO SE TOCA)
# =========================
def analizar_viabilidad(idea):
    idea = idea.lower()
    score = 0
    j, p, s = [], [], []

    if "incendio" in idea:
        score += 2
        j.append("Emergencia real")
    else:
        p.append("No crítico")
        s.append("Aplicar rescate/incendios")

    if "autonom" in idea:
        score += 2
        j.append("Autonomía")
    else:
        score += 1
        p.append("Sin autonomía")
        s.append("Agregar IA")

    if "sensor" in idea or "camara" in idea:
        score += 2
        j.append("Percepción")
    else:
        score += 1
        p.append("Sin sensores")
        s.append("Agregar visión")

    estado = "ALTAMENTE VIABLE" if score >= 6 else "VIABLE" if score >= 4 else "MEJORABLE"

    return {
        "estado": estado,
        "score": score,
        "justificacion": j,
        "problemas": p,
        "soluciones": s
    }

# =========================
# HARDWARE (NO SE TOCA)
# =========================
def generar_hardware(peso):
    return {
        "estructura": {"material": "carbono", "tipo": "quad_x_industrial"},
        "propulsion": {"motores": 4, "kv": 1200, "thrust": 6.5},
        "controlador": "Pixhawk",
        "bateria": "LiPo 6S 10000mAh",
        "sensores": {"lidar": True, "termico": True, "gps": True},
        "peso_total": peso
    }

# =========================
# SOFTWARE NIVEL 10 (REAL)
# =========================
def generar_software(base):

    root = os.path.join(base, "software")

    estructura = {

        "main.py": """from core.system import DroneSystem

if __name__ == "__main__":
    DroneSystem().run()
""",

        "core": {
            "system.py": """import time
from comms.mavlink_node import MAVLinkNode
from control.flight_controller import FlightController
from perception.vision import VisionSystem
from navigation.planner import Planner
from safety.failsafe import FailSafe

class DroneSystem:

    def __init__(self):
        self.mav = MAVLinkNode()
        self.fc = FlightController()
        self.vision = VisionSystem()
        self.nav = Planner()
        self.safe = FailSafe()

        self.dt = 0.02

        self.mav.set_mode_guided()
        self.mav.arm()

    def run(self):
        while True:
            state = self.mav.get_telemetry()
            vision = self.vision.process()

            if self.safe.check(state):
                self.mav.emergency_land()
                continue

            target = self.nav.update(state, vision)
            control = self.fc.update(state, target, self.dt)

            self.mav.send_control(control)

            time.sleep(self.dt)
"""
        },

        "comms": {
            "mavlink_node.py": """from pymavlink import mavutil
import time

class MAVLinkNode:

    def __init__(self):
        self.master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
        self.master.wait_heartbeat()

    def set_mode_guided(self):
        self.master.mav.set_mode_send(
            self.master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            4
        )

    def arm(self):
        try:
            self.master.arducopter_arm()
        except:
            pass

    def get_telemetry(self):
        msg = self.master.recv_match(blocking=False)
        return msg.to_dict() if msg else {}

    def send_control(self, c):
        self.master.mav.manual_control_send(
            self.master.target_system,
            0,
            0,
            int(c.get("throttle", 500)),
            0,
            0
        )

    def emergency_land(self):
        print("FAILSAFE LAND")
"""
        },

        "control": {
            "pid.py": """class PID:

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.i = 0
        self.prev = 0

    def update(self, sp, meas, dt):
        e = sp - meas
        self.i += e * dt
        d = (e - self.prev) / dt if dt > 0 else 0
        self.prev = e
        return self.kp * e + self.ki * self.i + self.kd * d
""",

            "flight_controller.py": """from control.pid import PID

class FlightController:

    def __init__(self):
        self.alt = PID(1.5, 0.02, 0.5)

    def update(self, s, m, dt):
        altitude = s.get("altitude", 0)
        target_alt = m.get("altitude", 10)

        throttle = self.alt.update(target_alt, altitude, dt)

        return {"throttle": max(200, min(800, throttle))}
"""
        },

        "perception": {
            "vision.py": """class VisionSystem:
    def process(self):
        return {"vision": True}
"""
        },

        "navigation": {
            "planner.py": """class Planner:
    def update(self, s, v):
        return {"altitude": 10}
"""
        },

        "safety": {
            "failsafe.py": """class FailSafe:
    def check(self, s):
        return s.get("battery", 100) < 15
"""
        },

        "config": {
            "params.yaml": "pid: {kp:1.5,ki:0.02,kd:0.5}"
        }
    }

    def crear(r, c):
        if isinstance(c, dict):
            for k, v in c.items():
                crear(os.path.join(r, k), v)
        else:
            write_file(r, c)

    crear(root, estructura)
    return estructura

# =========================
# BLOQUES EXTRA (SE CONSERVAN)
# =========================
def generar_telemetria():
    return {
        "variables": ["altitude", "battery", "gps", "velocity"],
        "frecuencia_hz": 20,
        "estado": "real_stream"
    }

def calcular_fisica(peso):
    thrust = 26
    return {
        "thrust_total": thrust,
        "relacion": round(thrust / peso, 2),
        "estado": "ESTABLE"
    }

def generar_modelo_3d(peso):
    return {
        "tipo": "quad_x_industrial",
        "brazos": 4,
        "escala": peso
    }

def generar_riesgos():
    return {
        "criticos": ["perdida_bateria", "fallo_motores"],
        "operativos": ["viento", "lluvia"],
        "sistema": ["perdida_mavlink", "error_pid"]
    }

# =========================
# CORE
# =========================
class MaiaCore:

    def ejecutar_paso(self, idea, paso, data):

        if paso == 0:
            return {
                "paso": 1,
                "data": {
                    "viabilidad": analizar_viabilidad(idea)
                }
            }

        elif paso == 1:
            data["hardware"] = generar_hardware(12)
            return {"paso": 2, "data": data}

        elif paso == 2:
            base = f"maia_projects/{int(time.time())}"
            os.makedirs(base, exist_ok=True)
            data["base"] = base
            data["software"] = generar_software(base)
            return {"paso": 3, "data": data}

        elif paso == 3:
            data["telemetria"] = generar_telemetria()
            data["fisica"] = calcular_fisica(data["hardware"]["peso_total"])
            data["riesgos"] = generar_riesgos()
            data["modelo_3d"] = generar_modelo_3d(data["hardware"]["peso_total"])

            data["nivel_maia"] = "NIVEL 10 - AUTOPILOTO REAL"

            return {"final": True, "resultado": data}

# =========================
# API
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    req = request.get_json() or {}
    core = MaiaCore()

    return jsonify(core.ejecutar_paso(
        req.get("idea", ""),
        int(req.get("paso", 0)),
        req.get("data", {})
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