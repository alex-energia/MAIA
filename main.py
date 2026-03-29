# ==========================================
# MAIA SISTEMA INDUSTRIAL INTELIGENTE
# + SIMULADOR DE DRONE REAL (NIVEL BRUTAL)
# ==========================================

import json
import time
import random
import math

from core.evaluador_integral import EvaluadorIntegral
from core.motor_conocimiento import MotorConocimiento
from ai.vision import VisionSystem

print("🔥 MAIA SISTEMA INDUSTRIAL ACTIVADO")

evaluador = EvaluadorIntegral()
motor_conocimiento = MotorConocimiento()
vision = VisionSystem()

historial = []

# ==========================================
# 🧠 PROCESADOR ORIGINAL (NO SE BORRA)
# ==========================================
def procesar_entrada(entrada):

    resultado_final = {}

    try:
        vision_data = vision.analizar_entorno()
    except:
        vision_data = None

    partes = entrada.split()

    if len(partes) == 4:
        try:
            tecnologia = partes[0].lower()
            capacidad = float(partes[1])
            pais = partes[2].lower()
            riesgo = float(partes[3])

            resultado = evaluador.evaluar(
                tecnologia,
                capacidad,
                pais,
                riesgo
            )

            resultado_final = {
                "tipo": "financiero",
                "entrada": entrada,
                "resultado": resultado
            }

        except Exception as e:
            resultado_final = {
                "tipo": "error_financiero",
                "error": str(e)
            }

    else:
        try:
            respuesta = motor_conocimiento.responder(entrada)

            resultado_final = {
                "tipo": "conocimiento",
                "entrada": entrada,
                "respuesta": respuesta
            }

        except Exception as e:
            resultado_final = {
                "tipo": "error_conocimiento",
                "error": str(e)
            }

    resultado_final["vision"] = vision_data
    return resultado_final

# ==========================================
# 🧠 CONTROL PID REAL
# ==========================================
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error

        return (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )

# ==========================================
# 🚁 DRONE FÍSICO
# ==========================================
class Drone:

    def __init__(self):

        self.pos = [0.0, 0.0, 0.0]
        self.vel = [0.0, 0.0, 0.0]

        self.mass = 12
        self.battery = 100

        self.pid_z = PID(2.5, 0.2, 0.8)

        self.estado = "DESPEGANDO"

    def update(self, target_z, dt):

        # CONTROL ALTURA
        error_z = target_z - self.pos[2]
        thrust = self.pid_z.update(error_z, dt)

        # FÍSICA
        az = (thrust - 9.81 * self.mass) / self.mass

        self.vel[2] += az * dt
        self.pos[2] += self.vel[2] * dt

        # MOVIMIENTO HORIZONTAL (simulado)
        self.vel[0] += random.uniform(-0.2, 0.2)
        self.vel[1] += random.uniform(-0.2, 0.2)

        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

        # CONSUMO
        consumo = abs(thrust) * 0.0008
        self.battery -= consumo

        # ESTADOS
        if self.pos[2] > 15:
            self.estado = "EN_MISION"

        if self.battery < 30:
            self.estado = "RETORNO"

        if self.battery < 10:
            self.estado = "CRITICO"

        return {
            "x": round(self.pos[0], 2),
            "y": round(self.pos[1], 2),
            "z": round(self.pos[2], 2),
            "vx": round(self.vel[0], 2),
            "vy": round(self.vel[1], 2),
            "vz": round(self.vel[2], 2),
            "battery": round(self.battery, 2),
            "estado": self.estado,
            "thrust": round(thrust, 2)
        }

# ==========================================
# 🚀 SIMULADOR DE DRONE PRO
# ==========================================
def simular_drone():

    drone = Drone()
    datos = []

    dt = 0.1
    pasos = 200

    target_altitude = 20

    for t in range(pasos):

        try:
            data = drone.update(target_altitude, dt)

            # VISIÓN
            try:
                vision_data = vision.analizar_entorno()
            except:
                vision_data = "clear"

            # DECISIÓN IA
            decision = procesar_entrada("optimizar estabilidad drone")

            paquete = {
                "t": t,
                **data,
                "vision": vision_data,
                "decision": decision.get("tipo", "IA"),
                "alerta": (
                    "⚠️ batería baja" if data["battery"] < 30 else None
                )
            }

            datos.append(paquete)

            if drone.battery <= 5:
                break

        except Exception as e:
            datos.append({"error": str(e)})

    return datos

# ==========================================
# 🔥 EJECUCIÓN AUTOMÁTICA (WEB)
# ==========================================

print("🚀 Ejecutando simulación MAIA...")

telemetria = simular_drone()

# INTELIGENCIA (NO SE BORRA)
inputs_demo = [
    "solar 50 colombia 0.02",
    "optimizar bateria drone",
    "riesgos vuelo autonomo"
]

for entrada in inputs_demo:
    try:
        resultado = procesar_entrada(entrada)

        historial.append({
            "timestamp": time.time(),
            "input": entrada,
            "output": resultado
        })

    except Exception as e:
        historial.append({"error": str(e)})

# ==========================================
# 📡 SALIDA FINAL
# ==========================================

salida_final = telemetria[-50:]

print("###DATA_START###")
print(json.dumps(salida_final))
print("###DATA_END###")
print("OK")