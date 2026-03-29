# ==========================================
# MAIA SISTEMA INSTITUCIONAL INTELIGENTE
# Motor Financiero + Motor de Conocimiento
# + MODO AUTO PARA WEB (FIX TIMEOUT)
# ==========================================

import json
import time
import os

from core.evaluador_integral import EvaluadorIntegral
from core.motor_conocimiento import MotorConocimiento
from ai.vision import VisionSystem

print("MAIA SISTEMA INSTITUCIONAL ACTIVADO")
print("Modo dual: Financiero + Conocimiento")

evaluador = EvaluadorIntegral()
motor_conocimiento = MotorConocimiento()
vision = VisionSystem()

historial = []

# ==========================================
# 🔥 DETECCIÓN MODO AUTOMÁTICO
# ==========================================
MODO_AUTO = True  # ← 🔥 FORZAMOS PARA MAIA WEB

# ==========================================
# 🚀 FUNCION DE PROCESO
# ==========================================
def procesar_entrada(entrada):

    resultado_final = {}

    # 🔥 VISIÓN
    try:
        vision_data = vision.analizar_entorno()
    except:
        vision_data = None

    partes = entrada.split()

    # =========================
    # MODO FINANCIERO
    # =========================
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

    # =========================
    # MODO CONOCIMIENTO
    # =========================
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
# 🤖 MODO AUTOMÁTICO (WEB)
# ==========================================
if MODO_AUTO:

    inputs_demo = [
        "solar 50 colombia 0.02",
        "analizar estabilidad de drone",
        "riesgos de energia eolica",
        "optimizacion de baterias"
    ]

    for entrada in inputs_demo:
        try:
            resultado = procesar_entrada(entrada)

            historial.append({
                "timestamp": time.time(),
                "input": entrada,
                "output": resultado
            })

            time.sleep(0.2)

        except Exception as e:
            historial.append({
                "error": str(e)
            })

# ==========================================
# 💻 MODO INTERACTIVO (CONSOLA)
# ==========================================
else:

    print("Formato financiero:")
    print("tecnologia capacidad_MW pais riesgo_regulatorio")
    print("Escribe 'salir' para cerrar\n")

    while True:
        try:
            entrada = input("MAIA> ").strip()

            if not entrada:
                print("⚠️ Entrada vacía")
                continue

            if entrada.lower() == "salir":
                print("Cerrando MAIA...")
                break

            resultado = procesar_entrada(entrada)

            print(resultado)

            historial.append({
                "timestamp": time.time(),
                "input": entrada,
                "output": resultado
            })

            historial = historial[-20:]

        except KeyboardInterrupt:
            print("\nInterrupción manual")
            break

        except Exception as e:
            print("ERROR GLOBAL:", e)

# ==========================================
# 📡 SALIDA PARA MAIA WEB
# ==========================================
try:
    if not historial:
        historial = [{"error": "sin datos"}]
except Exception as e:
    historial = [{"error": str(e)}]

print("###DATA_START###")
print(json.dumps(historial))
print("###DATA_END###")
print("OK")