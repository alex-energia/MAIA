from core.motor_financiero import MotorFinanciero


class EvaluadorIntegral:

    def __init__(self):
        self.finanzas = MotorFinanciero()

    def evaluar(self, tecnologia, capacidad, pais, riesgo):

        inversion = capacidad * 950000
        energia_anual = capacidad * 8760 * 0.23
        ingresos = energia_anual * 70
        opex = inversion * 0.02

        # Construimos flujos manualmente (ya que no tienes generar_flujos)
        vida_proyecto = 20
        flujo_anual = ingresos - opex

        flujos = [-inversion] + [flujo_anual] * vida_proyecto

        # Supuesto simple de costo equity según riesgo
        if riesgo == "alto":
            costo_equity = 0.18
        elif riesgo == "medio":
            costo_equity = 0.14
        else:
            costo_equity = 0.10

        wacc = self.finanzas.calcular_wacc(costo_equity)
        van = self.finanzas.calcular_van(flujos, wacc)
        tir = self.finanzas.calcular_tir(flujos)

        if tir and tir > costo_equity:
            opinion = "Proyecto crea valor para el equity."
        elif tir and tir < wacc:
            opinion = "Proyecto destruye valor."
        else:
            opinion = "Proyecto financieramente neutro."

        return {
            "tecnologia": tecnologia,
            "pais": pais,
            "capacidad_mw": capacidad,
            "inversion_estimada": inversion,
            "energia_anual_mwh": energia_anual,
            "ingresos_anuales": ingresos,
            "opex_anual": opex,
            "costo_equity": costo_equity,
            "wacc": wacc,
            "van": van,
            "tir": tir,
            "opinion_estrategica": opinion
        }