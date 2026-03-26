class MaiaValidator:

    def validar(self, data):

        # 🔒 PROTECCIÓN (evita crashes)
        fisica = data.get("fisica", {})
        analisis = data.get("analisis", {})

        autonomia = fisica.get("autonomia", 0)
        consumo = fisica.get("consumo", 0)
        empuje = fisica.get("empuje", 0)
        peso = analisis.get("peso", 0)

        errores = []
        soluciones = []

        # =========================
        # 🔴 VALIDACIONES BASE (TU LÓGICA)
        # =========================

        if autonomia < 5:
            errores.append("Autonomía extremadamente baja")
            soluciones.append("Usar batería de mayor capacidad")

        if consumo > 5000:
            errores.append("Consumo energético excesivo")
            soluciones.append("Optimizar eficiencia de motores")

        if peso > 15:
            errores.append("Peso estructural inviable")
            soluciones.append("Reducir materiales o rediseñar estructura")

        # =========================
        # 🧠 NUEVA VALIDACIÓN REAL (CLAVE)
        # =========================

        # Empuje mínimo requerido (factor seguridad 2x)
        empuje_minimo = peso * 9.81 * 2

        if empuje and empuje < empuje_minimo:
            errores.append("Empuje insuficiente para vuelo estable")
            soluciones.append("Aumentar potencia de motores o reducir peso")

        # =========================
        # 🧠 VALIDACIONES AVANZADAS
        # =========================

        if autonomia == 0:
            errores.append("No se pudo calcular autonomía")
            soluciones.append("Revisar parámetros de batería")

        if consumo == 0:
            errores.append("Consumo no calculado correctamente")
            soluciones.append("Revisar modelo energético")

        # =========================
        # 🟢 SI ES VIABLE → OPTIMIZAR
        # =========================

        if not errores:
            return {
                "viabilidad": "VIABLE ✅",
                "errores": [],
                "soluciones": [
                    "Optimizar consumo para aumentar autonomía",
                    "Implementar control PID en el flight controller",
                    "Agregar redundancia en sensores (GPS/IMU)",
                    "Optimizar distribución de peso"
                ]
            }

        # =========================
        # 🔴 SI NO ES VIABLE
        # =========================

        return {
            "viabilidad": "NO VIABLE ❌",
            "errores": errores,
            "soluciones": soluciones
        }
