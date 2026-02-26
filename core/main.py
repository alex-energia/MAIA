# ==========================================
# MAIA SISTEMA INSTITUCIONAL INTELIGENTE
# Motor Financiero + Motor de Conocimiento
# ==========================================

from core.motor_financiero import MotorFinanciero
from core.motor_conocimiento import MotorConocimiento

print("MAIA SISTEMA INSTITUCIONAL ACTIVADO")
print("Modo dual: Financiero + Conocimiento")
print("Formato financiero:")
print("tecnologia capacidad_MW pais riesgo_regulatorio")
print("Ejemplo:")
print("solar 50 colombia 0.02")
print("Escribe 'salir' para cerrar\n")

motor_financiero = MotorFinanciero()
motor_conocimiento = MotorConocimiento()

while True:

    entrada = input("MAIA> ")

    if entrada.lower() == "salir":
        print("Cerrando MAIA...")
        break

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

            resultado = motor_financiero.evaluar_proyecto(
                tecnologia,
                capacidad,
                pais,
                riesgo
            )

            print(resultado)

        except ValueError:
            print("Error en formato financiero. Use:")
            print("tecnologia capacidad_MW pais riesgo_regulatorio")

    # =========================
    # MODO CONOCIMIENTO
    # =========================
    else:
        respuesta = motor_conocimiento.responder(entrada)
        print(respuesta)