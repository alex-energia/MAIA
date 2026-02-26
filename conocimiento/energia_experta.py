class ConocimientoEnergetico:

    def __init__(self):

        self.tecnologias = {

            "solar": {
                "factor_planta": (0.18, 0.28),
                "capex_mw_usd": (700000, 1200000),
                "riesgo": "medio",
                "tipo_generacion": "intermitente"
            },

            "eolica": {
                "factor_planta": (0.30, 0.45),
                "capex_mw_usd": (1200000, 1800000),
                "riesgo": "medio",
                "tipo_generacion": "intermitente"
            },

            "nuclear": {
                "factor_planta": (0.85, 0.95),
                "capex_mw_usd": (5000000, 9000000),
                "riesgo": "alto",
                "tipo_generacion": "base_load"
            },

            "geotermica": {
                "factor_planta": (0.70, 0.90),
                "capex_mw_usd": (2500000, 6000000),
                "riesgo": "alto_exploracion",
                "tipo_generacion": "base_load"
            }
        }

    def evaluar_tecnologia(self, nombre):

        if nombre not in self.tecnologias:
            return "Tecnologia no registrada"

        data = self.tecnologias[nombre]

        return f"""
Tecnologia: {nombre.upper()}
Factor de planta típico: {data['factor_planta'][0]*100}% - {data['factor_planta'][1]*100}%
CAPEX típico USD/MW: {data['capex_mw_usd'][0]} - {data['capex_mw_usd'][1]}
Nivel de riesgo: {data['riesgo']}
Tipo de generación: {data['tipo_generacion']}
"""