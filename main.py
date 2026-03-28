# ==========================================
# MAIA SISTEMA INSTITUCIONAL INTELIGENTE
# Motor Financiero + Motor de Conocimiento
# ==========================================

import json
import time

from core.evaluador_integral import EvaluadorIntegral
from core.motor_conocimiento import MotorConocimiento

# 🔥 NUEVO: VISIÓN
from ai.vision import VisionSystem

print("MAIA SISTEMA INSTITUCIONAL ACTIVADO")
print("Modo dual: Financiero + Conocimiento")
print("Formato financiero:")
print("tecnologia capacidad_MW pais riesgo_regulatorio")
print("Ejemplo:")
print("solar 50 colombia 0.02")
print("Escribe 'salir' para cerrar\n")

evaluador = EvaluadorIntegral()
motor_conocimiento = MotorConocimiento()

# 🔥 NUEVO
vision = VisionSystem()

# =========================
# TELEMETRÍA BASE
# =========================
historial = []

while True:
    try:
        entrada = input("MAIA> ").strip()

        if not entrada:
            print("⚠️ Entrada vacía")
            continue

        if entrada.lower() == "salir":
            print("Cerrando MAIA...")
            break

        # 🔥 VISIÓN ACTIVA
        vision_data = vision.analizar_entorno()

        if vision_data:
            print("📡 VISIÓN DETECTÓ:")
            print(vision_data)

        partes = entrada.split()
        resultado_final = {}

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

                print(resultado)

            except Exception as e:
                resultado_final = {
                    "tipo": "error_financiero",
                    "error": str(e)
                }

                print("ERROR REAL:")
                print(e)

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

                print(respuesta)

            except Exception as e:
                resultado_final = {
                    "tipo": "error_conocimiento",
                    "error": str(e)
                }

                print("ERROR REAL:")
                print(e)

        # 🔥 AGREGAR VISIÓN A RESULTADO
        resultado_final["vision"] = vision_data

        # =========================
        # GUARDAR TELEMETRÍA
        # =========================
        historial.append({
            "timestamp": time.time(),
            "input": entrada,
            "output": resultado_final
        })

        # limitar tamaño
        historial = historial[-20:]

    except KeyboardInterrupt:
        print("\nInterrupción manual")
        break

    except Exception as e:
        print("ERROR GLOBAL:", e)

# =========================
# SALIDA FINAL (PARA MAIA WEB)
# =========================
try:
    if not historial:
        historial = [{"error": "sin datos"}]
except Exception as e:
    historial = [{"error": str(e)}]

print("###DATA_START###")
print(json.dumps(historial))
print("###DATA_END###")
print("OK")