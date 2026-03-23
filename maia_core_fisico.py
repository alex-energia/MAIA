import math

class MaiaCoreFisico:

    def calcular_fisica(self, peso):
        g = 9.81

        empuje_requerido = peso * g * 2.2  # margen realista
        potencia_motor = empuje_requerido * 1.5

        consumo_watts = potencia_motor * 4
        capacidad_bateria = 22000  # mAh (ejemplo industrial)
        voltaje = 22.2  # LiPo 6S

        energia_wh = (capacidad_bateria / 1000) * voltaje

        autonomia_min = (energia_wh / consumo_watts) * 60

        return {
            "empuje": round(empuje_requerido, 2),
            "potencia": round(potencia_motor, 2),
            "consumo": round(consumo_watts, 2),
            "autonomia": round(autonomia_min, 2)
        }

    def analizar_tipo(self, idea):
        idea = idea.lower()

        if "incendio" in idea:
            return {"peso": 12, "tipo": "emergencia"}
        elif "seguridad" in idea:
            return {"peso": 6, "tipo": "vigilancia"}
        elif "mineria" in idea:
            return {"peso": 10, "tipo": "industrial"}
        else:
            return {"peso": 5, "tipo": "general"}

    def ejecutar(self, idea):
        analisis = self.analizar_tipo(idea)
        fisica = self.calcular_fisica(analisis["peso"])

        return {
            "analisis": analisis,
            "fisica": fisica
        }