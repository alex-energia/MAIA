# -*- coding: utf-8 -*-
import numpy as np

class FinancialBuilder:
    def process_model(self, data):
        # Extracción de variables del modelo Morrosquillo
        capex = float(data.get('capex', 0))
        opex = float(data.get('opex', 0))
        ingresos = float(data.get('ingresos', 0))
        trm = float(data.get('trm', 3900))
        
        # Simulación Montecarlo (1000 iteraciones sobre VPN)
        # Variamos ingresos y TRM en un rango de volatilidad del 10%
        sims = []
        for _ in range(1000):
            var = np.random.normal(1, 0.1)
            vpn_sim = (ingresos * var * 10) - capex # Simplificación para flujo a 10 años
            sims.append(vpn_sim)
            
        return {
            "vpn_base": (ingresos * 10) - capex,
            "tir_est": ((ingresos / capex) * 100) if capex > 0 else 0,
            "montecarlo_exito": (np.array(sims) > 0).mean() * 100,
            "max_risk": np.min(sims)
        }

builder_engine = FinancialBuilder()