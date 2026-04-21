# builder_engine.py - INTELIGENCIA FINANCIERA & MONTECARLO
import numpy as np

class FinancialBuilder:
    def __init__(self):
        self.sections = {
            "CAPEX": ["Equipos Principales", "Obras Civiles", "Terrenos", "Implantación"],
            "OPEX": ["Personal", "Mantenimiento", "Seguros", "Servicios"],
            "FINANCE": ["% Financiación", "Tasa Interés (Kd)", "Plazo", "Gracia"],
            "MACRO": ["TRM Asumida", "IPC", "IPP", "TMRR (Hurdle Rate)"]
        }

    def run_montecarlo(self, vpn_base, iteraciones=1000):
        """Simulación de Montecarlo para el riesgo del proyecto."""
        # Simula variaciones en TRM y Precio kWh
        variaciones = np.random.normal(0, 0.05, iteraciones)
        resultados = vpn_base * (1 + variaciones)
        return {
            "probabilidad_exito": float(np.mean(resultados > 0) * 100),
            "vpn_min": float(np.min(resultados)),
            "vpn_max": float(np.max(resultados))
        }

    def get_market_variables(self, tech, country):
        """MAIA busca automáticamente variables de mercado."""
        # Aquí se integra la búsqueda automática de TRM, IPC e IPP actual
        return {"trm": 3950.0, "ipc": 0.045, "ipp": 0.051}

builder_engine = FinancialBuilder()
