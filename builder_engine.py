# -*- coding: utf-8 -*-
import numpy as np

class BuilderCore:
    def run_model(self, data):
        try:
            # Captura de datos del formulario
            capex = float(data.get('capex', '0').replace('.', ''))
            capacidad = float(data.get('capacidad') or 1)
            ppa = float(data.get('ppa') or 0)
            
            # 1. FLUJO DE CAJA SIMPLIFICADO (10 AÑOS)
            periodos = 10
            ingresos_anuales = capacidad * 1850 * ppa # 1850 horas sol/año
            opex_anual = capex * 0.02
            flujo_anual = ingresos_anuales - opex_anual
            
            # 2. CÁLCULO DE INDICADORES
            vpn = np.npv(0.12, [-capex] + [flujo_anual] * periodos) # Tasa 12%
            tir = np.irr([-capex] + [flujo_anual] * periodos)
            
            # 3. BASE PARA MONTECARLO (Simulación de 1000 escenarios)
            # Variamos el PPA y el OPEX aleatoriamente
            escenarios_vpn = []
            for _ in range(1000):
                v_ppa = ppa * np.random.normal(1, 0.1) # 10% volatilidad
                v_ingresos = capacidad * 1850 * v_ppa
                v_vpn = np.npv(0.12, [-capex] + [v_ingresos - opex_anual] * periodos)
                escenarios_vpn.append(v_vpn)

            return {
                "vpn": f"$ {int(vpn):,}",
                "tir": f"{tir*100:.2f}%",
                "payback": f"{capex/flujo_anual:.1f} Años" if flujo_anual > 0 else "N/A",
                "montecarlo_avg": f"$ {int(np.mean(escenarios_vpn)):,}",
                "probabilidad_exito": f"{len([x for x in escenarios_vpn if x > 0]) / 10:.1f}%",
                "chart_data": [int(flujo_anual) for _ in range(5)]
            }
        except Exception as e:
            return {"error": str(e)}

builder_engine = BuilderCore()