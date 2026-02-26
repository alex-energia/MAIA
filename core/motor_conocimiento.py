# ==========================================
# MOTOR DE CONOCIMIENTO MAIA
# Especialista en Energía y Finanzas
# ==========================================

class MotorConocimiento:

    def responder(self, pregunta):

        pregunta = pregunta.lower()

        # =========================
        # ENERGÍA
        # =========================

        if "hidroelectrica" in pregunta or "hidroeléctrica" in pregunta:
            return """
ENERGÍA HIDROELÉCTRICA:

Es la generación de electricidad a partir del movimiento del agua.
Utiliza una caída hidráulica para mover turbinas conectadas a generadores.

Ventajas:
- Energía renovable
- Alta vida útil (>50 años)
- Bajo costo operativo

Riesgos:
- Impacto ambiental
- Dependencia climática

¿Desea bibliografía técnica sobre energía hidroeléctrica?
"""

        if "nuclear" in pregunta:
            return """
ENERGÍA NUCLEAR:

Generación eléctrica mediante fisión del uranio.
Produce alta densidad energética con bajas emisiones de CO2.

Ventajas:
- Energía base estable
- Cero emisiones directas

Riesgos:
- Alto CAPEX
- Gestión de residuos

¿Desea bibliografía técnica sobre energía nuclear?
"""

        if "geotermica" in pregunta or "geotérmica" in pregunta:
            return """
ENERGÍA GEOTÉRMICA:

Aprovecha el calor interno de la tierra.
Ideal para generación base continua.

Ventajas:
- Energía constante
- Baja emisión

Limitación:
- Requiere recurso geológico adecuado

¿Desea bibliografía técnica sobre energía geotérmica?
"""

        # =========================
        # FINANZAS
        # =========================

        if "capm" in pregunta:
            return """
MODELO CAPM:

Costo del capital = Rf + Beta (Rm - Rf)

Donde:
Rf = tasa libre de riesgo
Beta = sensibilidad al mercado
Rm = retorno del mercado

Sirve para calcular costo de equity.

¿Desea bibliografía académica del CAPM?
"""

        if "tir" in pregunta:
            return """
TIR (Tasa Interna de Retorno):

Es la tasa que hace el VAN igual a cero.
Si TIR > WACC → Proyecto viable.

¿Desea profundización técnica en TIR?
"""

        if "van" in pregunta:
            return """
VAN (Valor Actual Neto):

Es la suma de flujos descontados menos inversión inicial.
Si VAN > 0 → Proyecto genera valor.

¿Desea bibliografía técnica sobre VAN?
"""

        # =========================
        # RESPUESTA POR DEFECTO
        # =========================

        return """
MAIA no tiene aún esa respuesta cargada.
Estoy especializada en:

- Energía hidroeléctrica
- Energía nuclear
- Energía geotérmica
- Finanzas corporativas
- Modelos financieros

¿Desea ampliar el conocimiento en algún área específica?
"""