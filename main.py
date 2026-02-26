# ==========================================
# MAIA SISTEMA INSTITUCIONAL INTELIGENTE
# Motor Financiero + Motor de Conocimiento
# ==========================================

from core.evaluador_integral import EvaluadorIntegral
from core.motor_conocimiento import MotorConocimiento

print("MAIA SISTEMA INSTITUCIONAL ACTIVADO")
print("Modo dual: Financiero + Conocimiento")
print("Formato financiero:")
print("tecnologia capacidad_MW pais riesgo_regulatorio")
print("Ejemplo:")
print("solar 50 colombia 0.02")
print("Escribe 'salir' para cerrar\n")

evaluador = EvaluadorIntegral()
motor_conocimiento = MotorConocimiento()

while True:

    entrada = input("MAIA> ")

    if entrada.lower() == "salir":
        print("Cerrando MAIA...")
        break

    partes = entrada.split()

    # Si tiene exactamente 4 partes, intenta modo financiero
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

            print(resultado)

        except Exception as e:
            print("ERROR REAL:")
            print(e)

    else:
        # Si no es formato financiero, va a conocimiento
        respuesta = motor_conocimiento.responder(entrada)
        print(respuesta)