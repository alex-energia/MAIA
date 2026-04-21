# builder_engine.py - MOTOR FINANCIERO AVANZADO
import numpy as np

class ProjectBuilder:
    def run_montecarlo(self, capex, opex, ppa_price, iterations=1000):
        # Simulación de riesgo sobre el precio del kWh y TRM
        volatility = np.random.normal(0, 0.1, iterations)
        vpns = []
        for v in volatility:
            # Cálculo simplificado de VPN variando ingresos por volatilidad
            cash_flow = [-capex] + [ (ppa_price * (1+v)) - opex for _ in range(25)]
            vpns.append(np.interp(0.12, [0, 1], [cash_flow[0], sum(cash_flow[1:])]))
        
        return {
            "success_rate": float(np.mean(np.array(vpns) > 0) * 100),
            "max_vpn": float(np.max(vpns)),
            "min_vpn": float(np.min(vpns))
        }

builder_core = ProjectBuilder()
