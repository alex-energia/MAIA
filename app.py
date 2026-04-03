from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
import os, time, zipfile

print("MAIA INDUSTRIAL CORE LEVEL 8 - REAL STACK")

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
# VIABILIDAD
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
# HARDWARE
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
# SOFTWARE REAL FIX
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

class DroneSystem:
    def __init__(self):
        self.mav = MAVLinkNode()
        self.mav.arm()

    def run(self):
        while True:
            data = self.mav.get_telemetry()
            print(data)
            time.sleep(0.05)
"""
        },
        "comms": {
            "mavlink_node.py": """from pymavlink import mavutil

class MAVLinkNode:
    def __init__(self):
        self.master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
        self.master.wait_heartbeat()

    def arm(self):
        try:
            self.master.arducopter_arm()
        except:
            pass

    def get_telemetry(self):
        msg = self.master.recv_match(blocking=False)
        if msg:
            return msg.to_dict()
        return {}
"""
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
            data["nivel_maia"] = "NIVEL 8 - SOFTWARE REAL FUNCIONAL"
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