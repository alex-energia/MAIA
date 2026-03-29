# ==========================================
# MAIA SISTEMA INDUSTRIAL INTELIGENTE
# + SIMULADOR DE DRONE REAL
# ==========================================

import json
import time
import random

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
# 🚀 SIMULADOR DE DRONE (NUEVO NIVEL)
# ==========================================
def simular_drone():

    estado = {
        "pos": [0.0, 0.0, 0.0],
        "vel": [0.0, 0.0, 0.0]
    }

    datos = []

    for t in range(150):

        try:
            # 🔥 dinámica simple
            ax = random.uniform(0.1, 0.3)
            ay = random.uniform(0.1, 0.3)
            az = random.uniform(0.05, 0.15)

            estado["vel"][0] += ax * 0.1
            estado["vel"][1] += ay * 0.1
            estado["vel"][2] += az * 0.1

            estado["pos"][0] += estado["vel"][0] * 0.1
            estado["pos"][1] += estado["vel"][1] * 0.1
            estado["pos"][2] += estado["vel"][2] * 0.1

            # 🔥 visión
            try:
                vision_data = vision.analizar_entorno()
            except:
                vision_data = None

            # 🔥 decisiones
            decision = procesar_entrada("analizar estabilidad drone")

            paquete = {
                "t": t,
                "x": round(estado["pos"][0], 2),
                "y": round(estado["pos"][1], 2),
                "z": round(estado["pos"][2], 2),
                "vx": round(estado["vel"][0], 2),
                "vy": round(estado["vel"][1], 2),
                "vz": round(estado["vel"][2], 2),
                "vision": vision_data or "clear",
                "decision": decision.get("tipo"),
                "estado": "OK"
            }

            datos.append(paquete)

            time.sleep(0.01)

        except Exception as e:
            datos.append({"error": str(e)})

    return datos

# ==========================================
# 🔥 EJECUCIÓN AUTOMÁTICA (WEB)
# ==========================================
print("🚀 Ejecutando simulación MAIA...")

# 🔥 PARTE 1: simulación drone
telemetria = simular_drone()

# 🔥 PARTE 2: inteligencia
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
# 📡 SALIDA FINAL (CRÍTICA PARA FRONTEND)
# ==========================================
salida_final = telemetria[-50:]  # 🔥 SOLO LO ÚLTIMO

print("###DATA_START###")
print(json.dumps(salida_final))
print("###DATA_END###")
print("OK")