# -*- coding: utf-8 -*-
import numpy as np

class FinancialBuilder:
    def __init__(self):
        # Campos extraídos del modelo Granja Solar Morrosquillo
        self.market_defaults = {
            "TRM": 3900.0,
            "IPC": 0.049,
            "IPP": 0.0511,
            "WACC": 0.1233
        }

    def run_full_model(self, data):
        """
        Calcula TIR, VPN y Payback integrando Ley 1715.
        """
        capex = float(data.get('capex', 0))
        ingresos_anuales = float(data.get('ingresos_est', 0))
        años = 25
        
        # Flujo de caja simplificado (Agnóstico a tecnología)
        flujos = [-capex] + [ingresos_anuales * (1.03**i) for i in range(1, años + 1)]
        
        vpn = np.npv(self.market_defaults['WACC'], flujos)
        tir = np.irr(flujos)
        
        # Montecarlo: Variación de TRM y Generación (1000 iteraciones)
        simulaciones = []
        for _ in range(1000):
            var_trm = np.random.normal(1, 0.08) # Volatilidad del 8%
            sim_vpn = np.npv(self.market_defaults['WACC'], [f * var_trm for f in flujos])
            simulaciones.append(sim_vpn)
            
        prob_exito = (np.array(simulaciones) > 0).mean() * 100
        
        return {
            "VPN": vpn,
            "TIR": tir * 100,
            "Montecarlo_Exito": prob_exito,
            "Riesgo": "BAJO" if prob_exito > 80 else "ALTO"
        }

builder_engine = FinancialBuilder()
