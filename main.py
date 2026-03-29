# ==========================================
# MAIA SISTEMA INDUSTRIAL INTELIGENTE
# + SIMULADOR DE DRONE REAL (OPTIMIZADO)
# ==========================================

import json
import time
import random
import math
import threading

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
        vision_data = "no_data"

    partes = entrada.split()

    if len(partes) == 4:
        try:
            tecnologia = partes[0].lower()
            capacidad = float(partes[1])
            pais = partes[2].lower()
            riesgo = float(partes[3])

            resultado = evaluador.evaluar(
                tecnologia, capacidad, pais, riesgo
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
# 🧠 CONTROL PID (FIXED)
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
        try:
            error_z = target_z - self.pos[2]
            thrust = self.pid_z.update(error_z, dt)

            az = (thrust - 9.81 * self.mass) / self.mass

            self.vel[2] += az * dt
            self.pos[2] += self.vel[2] * dt

            # Movimiento suave
            self.vel[0] += random.uniform(-0.1, 0.1)
            self.vel[1] += random.uniform(-0.1, 0.1)

            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt

            consumo = abs(thrust) * 0.0005
            self.battery -= consumo

            # Estados inteligentes
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

        except Exception as e:
            return {"error": str(e)}


# ==========================================
# 🚀 SIMULADOR OPTIMIZADO (ANTI-TIMEOUT)
# ==========================================
def simular_drone():
    drone = Drone()
    datos = []

    dt = 0.1
    max_time = 5  # 🔥 límite real en segundos
    start_time = time.time()

    target_altitude = 20

    t = 0
    while True:
        try:
            if time.time() - start_time > max_time:
                break

            data = drone.update(target_altitude, dt)

            # Visión (no bloqueante)
            try:
                vision_data = vision.analizar_entorno()
            except:
                vision_data = "clear"

            decision = procesar_entrada("optimizar estabilidad drone")

            paquete = {
                "t": t,
                **data,
                "vision": vision_data,
                "decision": decision.get("tipo", "IA"),
                "alerta": (
                    "⚠️ batería baja" if data.get("battery", 100) < 30 else None
                )
            }

            datos.append(paquete)

            if drone.battery <= 5:
                break

            t += 1

        except Exception as e:
            datos.append({"error": str(e)})
            break

    return datos


# ==========================================
# 🔥 EJECUCIÓN
# ==========================================
print("🚀 Ejecutando simulación MAIA...")

try:
    telemetria = simular_drone()
except Exception as e:
    telemetria = [{"error": str(e)}]


# ==========================================
# 🧠 INTELIGENCIA
# ==========================================
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
# 📡 SALIDA FINAL (SIEMPRE GARANTIZADA)
# ==========================================
salida_final = telemetria[-50:] if telemetria else [{"error": "sin datos"}]

print("###DATA_START###")
print(json.dumps(salida_final))
print("###DATA_END###")
print("OK")