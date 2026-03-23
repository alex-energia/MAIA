class MaiaValidator:

    def validar(self, data):
        errores = []
        soluciones = []

        autonomia = data["fisica"]["autonomia"]
        consumo = data["fisica"]["consumo"]

        if autonomia < 5:
            errores.append("Autonomía extremadamente baja")
            soluciones.append("Usar batería de mayor capacidad")

        if consumo > 5000:
            errores.append("Consumo energético excesivo")
            soluciones.append("Optimizar eficiencia de motores")

        if data["analisis"]["peso"] > 15:
            errores.append("Peso estructural inviable")
            soluciones.append("Reducir materiales o rediseñar estructura")

        if errores:
            return {
                "viabilidad": "NO VIABLE ❌",
                "errores": errores,
                "soluciones": soluciones
            }

        return {
            "viabilidad": "VIABLE ✅",
            "errores": [],
            "soluciones": []
        }