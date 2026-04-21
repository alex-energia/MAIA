# -*- coding: utf-8 -*-
# builder_engine.py - CEREBRO FINANCIERO V.12

class BuilderCore:
    def __init__(self):
        # El modelo de Morrosquillo I queda como referencia interna
        self.morrosquillo_ref = {
            "capacidad": 23.42,
            "capex": 90389977843,
            "ppa": 323,
            "kd": 0.1164
        }

    def process_financials(self, data):
        """
        Aquí programaremos la TIR, VPN y Flujos en el siguiente paso.
        """
        try:
            # Ejemplo de cálculo de inversión por MW
            cap = float(data.get('capacidad', 0) or 0)
            capex = float(str(data.get('capex', 0)).replace('.', '').replace(',', '') or 0)
            
            return {
                "status": "CALCULADO",
                "inversion_mw": f"$ {capex/cap:,.0f}" if cap > 0 else 0,
                "msg": "Estructura de flujo de caja lista para inyectar fórmulas."
            }
        except Exception as e:
            return {"status": "ERROR", "msg": str(e)}

builder_engine = BuilderCore()