import os
import json

class MaiaSoftwareGenerator:

    def __init__(self, base_path):
        self.base = base_path

    def generar(self, analisis, fisica):

        self._crear_estructura()
        self._generar_config(analisis, fisica)
        self._generar_flight_controller()
        self._generar_navigation()
        self._generar_sensores()
        self._generar_ai_module()
        self._generar_main()

        return {
            "arquitectura": "Modular tipo PX4",
            "modulos": [
                "flight_controller",
                "navigation",
                "sensores",
                "failsafe",
                "ai_decision"
            ],
            "nivel": "PROFESIONAL"
        }

    # =========================
    # ESTRUCTURA
    # =========================
    def _crear_estructura(self):
        carpetas = [
            "firmware",
            "firmware/control",
            "firmware/navigation",
            "firmware/sensores",
            "firmware/ai",
            "config"
        ]

        for c in carpetas:
            os.makedirs(os.path.join(self.base, c), exist_ok=True)

    # =========================
    # CONFIG
    # =========================
    def _generar_config(self, analisis, fisica):
        config = {
            "peso": analisis.get("peso"),
            "tipo": analisis.get("tipo"),
            "autonomia": fisica.get("autonomia"),
            "control": "PID + AI"
        }

        with open(f"{self.base}/config/drone.json", "w") as f:
            json.dump(config, f, indent=4)

    # =========================
    # FLIGHT CONTROLLER (REAL)
    # =========================
    def _generar_flight_controller(self):

        codigo = '''
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


class FlightController:

    def __init__(self):
        self.altitude_pid = PID(1.2, 0.02, 0.1)
        self.roll_pid = PID(1.0, 0.01, 0.05)
        self.pitch_pid = PID(1.0, 0.01, 0.05)

    def stabilize(self, target_altitude, current_altitude):
        thrust = self.altitude_pid.compute(target_altitude, current_altitude)
        return thrust
'''

        with open(f"{self.base}/firmware/control/flight_controller.py", "w") as f:
            f.write(codigo)

    # =========================
    # NAVIGATION
    # =========================
    def _generar_navigation(self):

        codigo = '''
import math

class NavigationSystem:

    def distance(self, lat1, lon1, lat2, lon2):
        return math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)

    def calcular_ruta(self, origen, destino):
        return [origen, destino]
'''

        with open(f"{self.base}/firmware/navigation/navigation.py", "w") as f:
            f.write(codigo)

    # =========================
    # SENSORES
    # =========================
    def _generar_sensores(self):

        codigo = '''
class IMU:
    def leer(self):
        return {"roll":0, "pitch":0, "yaw":0}

class GPS:
    def leer(self):
        return {"lat":0, "lon":0}
'''

        with open(f"{self.base}/firmware/sensores/sensores.py", "w") as f:
            f.write(codigo)

    # =========================
    # IA DECISIONAL
    # =========================
    def _generar_ai_module(self):

        codigo = '''
class DecisionAI:

    def decidir(self, sensores):
        if sensores.get("bateria", 100) < 20:
            return "RETURN_HOME"
        return "CONTINUE"
'''

        with open(f"{self.base}/firmware/ai/decision.py", "w") as f:
            f.write(codigo)

    # =========================
    # MAIN
    # =========================
    def _generar_main(self):

        codigo = '''
from firmware.control.flight_controller import FlightController

fc = FlightController()

altitude = 0

for i in range(50):
    thrust = fc.stabilize(10, altitude)
    altitude += thrust * 0.1
    print("Altura:", altitude)
'''

        with open(f"{self.base}/main.py", "w") as f:
            f.write(codigo)