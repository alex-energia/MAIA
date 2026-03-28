import random

class VisionSystem:

    def __init__(self):
        self.ultima_deteccion = None

    def analizar_entorno(self):
        """
        Simula percepción del entorno
        """
        probabilidad = random.random()

        if probabilidad < 0.1:
            self.ultima_deteccion = {
                "tipo": "obstaculo",
                "distancia": round(random.uniform(1, 5), 2),
                "riesgo": "alto"
            }
        elif probabilidad < 0.2:
            self.ultima_deteccion = {
                "tipo": "zona_segura",
                "distancia": round(random.uniform(5, 15), 2),
                "riesgo": "bajo"
            }
        else:
            self.ultima_deteccion = None

        return self.ultima_deteccion