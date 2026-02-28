import random

def diagnosticar_planta():

    """
    Motor base de diagnóstico vegetal.
    Versión 1 simulada inteligente.
    Luego lo conectamos a visión real.
    """

    diagnosticos = [
        {
            "problema": "Posible deficiencia de nitrógeno",
            "confianza": 82,
            "recomendacion": "Aplicar fertilizante rico en nitrógeno y revisar drenaje."
        },
        {
            "problema": "Hongo foliar (mancha marrón)",
            "confianza": 76,
            "recomendacion": "Aplicar fungicida preventivo y evitar exceso de humedad."
        },
        {
            "problema": "Estrés hídrico",
            "confianza": 88,
            "recomendacion": "Regular frecuencia de riego y revisar exposición solar."
        },
        {
            "problema": "Plaga leve (áfidos)",
            "confianza": 79,
            "recomendacion": "Aplicar jabón potásico o control biológico."
        }
    ]

    resultado = random.choice(diagnosticos)

    return {
        "diagnostico": resultado["problema"],
        "nivel_confianza": resultado["confianza"],
        "recomendacion": resultado["recomendacion"]
    }