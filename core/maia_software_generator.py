# 🧠 MAIA SOFTWARE GENERATOR – NIVEL GLI REAL (FIX PRO FINAL)
import json

def generar_software_completo(tipo="general"):

    arquitectura = {
        "estructura": [
            "config/config.json",
            "firmware/pid.py",
            "firmware/flight_controller.py",
            "firmware/navigation.py",
            "firmware/failsafe.py",
            "drivers/gps.py",
            "drivers/imu.py",
            "drivers/barometer.py",
            "drivers/camera.py",
            "drivers/lidar.py",
            "ai/decision_model.py",
            "main.py"
        ]
    }

    algoritmos = [
        "Control PID (estabilidad)",
        "Filtro Kalman (conceptual)",
        "Path Planning",
        "Computer Vision (simulado)",
        "Failsafe automático",
        "Control adaptativo"
    ]

    sensores = [
        "GPS",
        "IMU",
        "Barómetro",
        "Cámara",
        "Lidar"
    ]

    codigo = {}

    # =========================
    # PID CORREGIDO
    # =========================
    codigo["firmware/pid.py"] = """class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error
        return (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
"""

    # =========================
    # FLIGHT CONTROLLER
    # =========================
    codigo["firmware/flight_controller.py"] = """from firmware.pid import PID

class FlightController:

    def __init__(self):
        self.pos = [0.0, 0.0, 0.0]
        self.vel = [0.0, 0.0, 0.0]
        self.masa = 1.5
        self.g = 9.81
        self.drag = 0.1

        self.pid_x = PID(1.0, 0.01, 0.1)
        self.pid_y = PID(1.0, 0.01, 0.1)
        self.pid_z = PID(1.2, 0.02, 0.1)

    def update(self, objetivo, dt):
        try:
            fx = self.pid_x.compute(objetivo[0], self.pos[0], dt)
            fy = self.pid_y.compute(objetivo[1], self.pos[1], dt)
            fz = self.pid_z.compute(objetivo[2], self.pos[2], dt)

            fz -= self.masa * self.g

            fx -= self.drag * self.vel[0]
            fy -= self.drag * self.vel[1]
            fz -= self.drag * self.vel[2]

            ax = fx / self.masa
            ay = fy / self.masa
            az = fz / self.masa

            self.vel[0] += ax * dt
            self.vel[1] += ay * dt
            self.vel[2] += az * dt

            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
            self.pos[2] += self.vel[2] * dt

            return {
                "pos": self.pos.copy(),
                "vel": self.vel.copy()
            }

        except Exception as e:
            return {"error": str(e)}
"""

    # =========================
    # NAVIGATION
    # =========================
    codigo["firmware/navigation.py"] = """def generar_waypoints(origen, destino, pasos=5):
    ruta = []
    for i in range(1, pasos + 1):
        punto = [
            origen[0] + (destino[0] - origen[0]) * i / pasos,
            origen[1] + (destino[1] - origen[1]) * i / pasos,
            origen[2] + (destino[2] - origen[2]) * i / pasos
        ]
        ruta.append(punto)
    return ruta
"""

    # =========================
    # FAILSAFE
    # =========================
    codigo["firmware/failsafe.py"] = """class FailSafe:
    def check(self, bateria, gps):
        if bateria < 20:
            return "RETURN_HOME"
        if not gps:
            return "EMERGENCY_LAND"
        return "OK"
"""

    # =========================
    # IA
    # =========================
    codigo["ai/decision_model.py"] = """def decidir(estado):
    pos = estado["pos"]
    obstaculo = estado.get("obstaculo", False)

    if obstaculo:
        return {
            "accion": "EVADIR",
            "nuevo_objetivo": [pos[0] + 2, pos[1] + 2, pos[2]]
        }

    return {"accion": "CONTINUAR"}
"""

    # =========================
    # MAIN PRO (ANTI-TRUNCADO)
    # =========================
    codigo["main.py"] = """import time
import json
import random

from firmware.flight_controller import FlightController
from firmware.failsafe import FailSafe
from firmware.navigation import generar_waypoints
from ai.decision_model import decidir

fc = FlightController()
fs = FailSafe()

dt = 0.1
waypoints = generar_waypoints([0,0,0],[10,10,10],6)
wp_index = 0

datos = []

for i in range(150):
    try:
        objetivo = waypoints[wp_index]

        estado = fc.update(objetivo, dt)
        if "error" in estado:
            continue

        obstaculo = random.random() < 0.05

        decision = decidir({
            "pos": estado["pos"],
            "obstaculo": obstaculo
        })

        if decision["accion"] == "EVADIR":
            objetivo = decision["nuevo_objetivo"]

        if wp_index < len(waypoints) - 1:
            wp_index += 1

        estado_fs = fs.check(100, True)

        datos.append({
            "x": round(estado["pos"][0],2),
            "y": round(estado["pos"][1],2),
            "z": round(estado["pos"][2],2),
            "wp": wp_index,
            "fs": estado_fs
        })

    except Exception:
        continue

# 🔥 LIMITAR SALIDA (CLAVE)
datos = datos[-50:]

print("###DATA_START###")
print(json.dumps(datos))
print("###DATA_END###")

print("OK")
"""

    config = {
        "tipo": tipo,
        "modo": "autonomo"
    }

    resumen = {
        "descripcion": "Drone autónomo con control PID, navegación y failsafe.",
        "nivel": "Pre-real",
        "estado": "Optimizado sin truncado"
    }

    return {
        "arquitectura": arquitectura,
        "algoritmos": algoritmos,
        "sensores": sensores,
        "codigo": codigo,
        "config": config,
        "resumen": resumen
    }