class MaiaValidator:

    def validar(self, data):

        # 🔒 PROTECCIÓN (evita crashes)
        fisica = data.get("fisica", {})
        analisis = data.get("analisis", {})

        autonomia = fisica.get("autonomia", 0)
        consumo = fisica.get("consumo", 0)
        empuje = fisica.get("empuje", 0)
        peso = analisis.get("peso", 0)
        tipo = analisis.get("tipo", "general")

        errores = []
        soluciones = []
        explicacion_base = []

        # =========================
        # 🔴 VALIDACIONES BASE (TU LÓGICA)
        # =========================
        if autonomia < 5:
            errores.append("Autonomía extremadamente baja")
            soluciones.append("Usar batería de mayor capacidad")
        else:
            explicacion_base.append(f"Autonomía aceptable ({autonomia} min)")

        if consumo > 5000:
            errores.append("Consumo energético excesivo")
            soluciones.append("Optimizar eficiencia de motores")
        else:
            explicacion_base.append(f"Consumo dentro de rango ({consumo} W)")

        if peso > 15:
            errores.append("Peso estructural inviable")
            soluciones.append("Reducir materiales o rediseñar estructura")
        else:
            explicacion_base.append(f"Peso adecuado ({peso} kg)")

        # =========================
        # 🧠 NUEVA VALIDACIÓN REAL (CLAVE)
        # =========================
        empuje_minimo = peso * 9.81 * 2

        if empuje and empuje < empuje_minimo:
            errores.append("Empuje insuficiente para vuelo estable")
            soluciones.append("Aumentar potencia de motores o reducir peso")
        else:
            if empuje:
                explicacion_base.append("Relación empuje/peso adecuada para vuelo")

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
        # 📊 MÉTRICAS TÉCNICAS
        # =========================
        eficiencia = 0
        if consumo > 0:
            eficiencia = round(autonomia / consumo, 6)

        metricas = {
            "empuje_minimo_requerido": round(empuje_minimo, 2),
            "eficiencia_energetica": eficiencia
        }

        # =========================
        # 🧠 EXPLICACIÓN PROFESIONAL
        # =========================
        explicacion = self.generar_explicacion(
            errores,
            soluciones,
            explicacion_base,
            tipo,
            peso,
            autonomia,
            consumo,
            empuje,
            metricas
        )

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
                ],
                "explicacion": explicacion,
                "metricas": metricas
            }

        # =========================
        # 🔴 SI NO ES VIABLE
        # =========================
        return {
            "viabilidad": "NO VIABLE ❌",
            "errores": errores,
            "soluciones": soluciones,
            "explicacion": explicacion,
            "metricas": metricas
        }

    # =========================
    # 🧠 GENERADOR DE INFORME
    # =========================
    def generar_explicacion(
        self,
        errores,
        soluciones,
        base,
        tipo,
        peso,
        autonomia,
        consumo,
        empuje,
        metricas
    ):

        encabezado = f"""
Evaluación técnica del sistema UAV (Drone tipo: {tipo})

Parámetros analizados:
- Peso estructural: {peso} kg
- Autonomía estimada: {autonomia} min
- Consumo energético: {consumo} W
- Empuje generado: {empuje} N
"""

        if not errores:
            cuerpo = f"""
Diagnóstico:

{chr(10).join(['✔ ' + e for e in base])}

Métricas clave:
- Empuje mínimo requerido: {metricas["empuje_minimo_requerido"]} N
- Eficiencia energética: {metricas["eficiencia_energetica"]}

Conclusión:

El sistema es VIABLE desde el punto de vista de ingeniería.
Cumple con los requisitos mínimos de vuelo, estabilidad y consumo energético.
Se recomienda optimización para mejorar desempeño en condiciones reales.
"""
        else:
            cuerpo = f"""
Problemas detectados:

{chr(10).join(['❌ ' + e for e in errores])}

Soluciones recomendadas:

{chr(10).join(['🔧 ' + s for s in soluciones])}

Conclusión:

El sistema NO es viable en su estado actual.
Se requiere rediseño parcial o total antes de implementación real.
"""

        return encabezado + cuerpo