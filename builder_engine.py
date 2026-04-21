# -*- coding: utf-8 -*-
import numpy as np

class BuilderCore:
    def __init__(self):
        self.tasa_descuento = 0.12

    def calcular_modelo_completo(self, data):
        try:
            # Entrada de datos
            capacidad = float(data.get('capacidad') or 23.42)
            capex_base = float(data.get('capex', '0').replace('.', '').replace(',', ''))
            ppa = float(data.get('ppa') or 323)
            años = 25

            # --- DESGLOSE DE CAPEX (Basado en estándares de industria) ---
            desglose_capex = {
                "Equipos (Módulos/Inversores)": capex_base * 0.65,
                "Obra Civil y Montaje": capex_base * 0.20,
                "Interconexión y Redes": capex_base * 0.10,
                "Gestión y Seguros Construcción": capex_base * 0.05
            }

            # --- DESGLOSE DE OPEX ANUAL ---
            # Basado en un costo operativo de aprox $15,000 - $20,000 USD por MW/año
            opex_anual_detallado = {
                "Mantenimiento Preventivo/Correctivo": capacidad * 15000000, # COP
                "Seguridad y Vigilancia": 120000000, # Fijo anual
                "Seguros Todo Riesgo Daño Material": capex_base * 0.0025,
                "Arrendamiento y Gestión Predial": 80000000,
                "Personal Operativo": 250000000
            }
            total_opex_año = sum(opex_anual_detallado.values())

            # --- FLUJO DE CAJA ---
            generacion_anual = capacidad * 1900 * 0.98 # Horas sol con degradación técnica
            ingresos_anuales = generacion_anual * ppa
            flujo_neto = ingresos_anuales - total_opex_año
            
            flujos = [-capex_base] + [flujo_neto] * años
            vpn = np.npv(self.tasa_descuento, flujos)
            tir = np.irr(flujos)

            # --- SIMULACIÓN MONTECARLO (1.000 Escenarios sobre PPA y Disponibilidad) ---
            escenarios = []
            for _ in range(1000):
                v_ppa = ppa * np.random.normal(1, 0.08)
                v_disp = 1900 * np.random.normal(1, 0.03)
                v_ingresos = capacidad * v_disp * v_ppa
                v_vpn = np.npv(self.tasa_descuento, [-capex_base] + [(v_ingresos - total_opex_año)] * años)
                escenarios.append(v_vpn)

            return {
                "status": "SUCCESS",
                "indicadores": {
                    "vpn": f"$ {int(vpn):,}",
                    "tir": f"{tir*100:.2f}%",
                    "payback": f"{capex_base/flujo_neto:.1f} Años",
                    "probabilidad_exito": f"{(len([x for x in escenarios if x > 0])/1000)*100}%"
                },
                "capex_detallado": desglose_capex,
                "opex_detallado": opex_anual_detallado,
                "flujo_grafica": [int(flujo_neto) for _ in range(10)]
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

builder_engine = BuilderCore()
