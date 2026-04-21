# -*- coding: utf-8 -*-
import random

class BuilderCore:
    def calcular_modelo_pro(self, data):
        try:
            # Captura de datos del usuario
            capacidad = float(data.get('capacidad') or 23.42)
            capex_total = float(str(data.get('capex', '90389977843')).replace('.', '').replace(',', ''))
            ppa = float(data.get('ppa') or 323)
            años = 25
            tasa_wacc = 0.115

            # --- ESTRUCTURA DE COSTOS ---
            opex_anual = (capacidad * 16500000) + 450000000 # O&M + Gastos Fijos
            generacion_anual = capacidad * 1920 * 1000 * 0.985
            ingresos = generacion_anual * ppa
            
            # EBITDA y Flujo Neto Profesional
            ebitda = ingresos - opex_anual
            depreciacion = capex_total / 15
            impuestos = max(0, (ebitda - depreciacion) * 0.35)
            fcl = ebitda - impuestos # Flujo de Caja Libre

            # VPN Nativo
            vpn = -capex_total
            for t in range(1, años + 1):
                vpn += fcl / ((1 + tasa_wacc) ** t)

            # --- MONTECARLO REAL ---
            exitos = 0
            for _ in range(1000):
                v_ppa = ppa * random.uniform(0.90, 1.10)
                v_fcl = (generacion_anual * v_ppa) - opex_anual - impuestos
                v_vpn = -capex_total + sum([v_fcl/((1+tasa_wacc)**t) for t in range(1, años+1)])
                if v_vpn > 0: exitos += 1

            return {
                "vpn": f"$ {int(vpn):,}",
                "ebitda": f"$ {int(ebitda):,}",
                "fcl": f"$ {int(fcl):,}",
                "probabilidad": f"{(exitos/10):.1f}%",
                "chart": [int(fcl) for _ in range(10)]
            }
        except Exception as e:
            return {"error": str(e)}

builder_engine = BuilderCore()