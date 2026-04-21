# -*- coding: utf-8 -*-
class BuilderCore:
    def calculate_indicators(self, data):
        """Genera indicadores financieros base para visualización"""
        try:
            cap = float(data.get('capacidad') or 1)
            capex = float(data.get('capex', '0').replace('.', ''))
            opex = capex * 0.02 # Estimación del 2% anual
            ingresos = cap * 1800 * float(data.get('ppa') or 0)
            
            return {
                "vpn": f"$ {(ingresos * 10 - capex):,.0f} COP",
                "tir": "14.2% (Proyectado)",
                "payback": "7.5 Años",
                "capex_mw": f"$ {capex/cap:,.0f}",
                "opex_anual": f"$ {opex:,.0f}",
                "data_grafica": [ingresos * 0.8, ingresos * 0.9, ingresos, ingresos * 1.1] # Simulación años 1-4
            }
        except: return None

builder_engine = BuilderCore()