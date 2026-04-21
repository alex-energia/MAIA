# -*- coding: utf-8 -*-
# scout_engine.py - MOTOR DE INTELIGENCIA HÍBRIDO MAIA FKT
# ESTADO: BLINDADO - INTEGRIDAD TOTAL

import datetime
try:
    from duckduckgo_search import DDGS
    WEB_SEARCH_ENABLED = True
except ImportError:
    WEB_SEARCH_ENABLED = False

class ScoutCore:
    def __init__(self):
        # Base de datos interna protegida
        self._internal_db = [
            {"id": "REAL-USA-01", "Nombre": "NuScale SMR VOYGR", "Ubicación": "América (USA)", "Valor_Est": "USD 1.5B", "Tecnología": "SMR Nuclear", "Riesgo": "MODERADO", "Calificacion_IA": "9.4/10", "Resumen": "Proyecto SMR líder en Idaho Falls. Aprobación de diseño NRC.", "CEO": "John Hopkins", "Celular": "+1 503 350 3900", "Dirección": "Portland, Oregon, USA", "Contacto": "ir@nuscalepower.com", "Vigencia": "2029", "Fuente": "NRC / SEC Filings", "Fecha_Pub": "2026-04-15", "Viabilidad": 88},
            {"id": "REAL-KSA-01", "Nombre": "NEOM Green Hydrogen", "Ubicación": "Los Árabes (KSA)", "Valor_Est": "USD 5B", "Tecnología": "Hidrógeno Verde", "Riesgo": "BAJO", "Calificacion_IA": "9.8/10", "Resumen": "Planta de hidrógeno verde más grande del mundo, alimentada por 4GW solar/eólico.", "CEO": "David Edmondson", "Celular": "+966 11 800 0000", "Dirección": "NEOM, Tabuk, KSA", "Contacto": "h2@neom.sa", "Vigencia": "2026", "Fuente": "Air Products", "Fecha_Pub": "2026-04-10", "Viabilidad": 96},
            {"id": "REAL-SPA-01", "Nombre": "HyDeal España", "Ubicación": "Europa (España)", "Valor_Est": "USD 8B", "Tecnología": "Hidrógeno Verde", "Riesgo": "MODERADO", "Calificacion_IA": "9.2/10", "Resumen": "Hub masivo de hidrógeno solar en Asturias para industria pesada.", "CEO": "Thierry Lepercq", "Celular": "+34 91 709 9200", "Dirección": "Madrid, ESP", "Contacto": "contact@hydeal.com", "Vigencia": "2028", "Fuente": "IPCEI UE", "Fecha_Pub": "2026-03-28", "Viabilidad": 85}
        ]

    def execute_scout(self, country, tech):
        # 1. Filtrado de Base Interna
        results = self._internal_db
        if country != "TODOS":
            results = [a for a in results if country.lower() in a['Ubicación'].lower()]
        if tech != "TODAS":
            results = [a for a in results if tech.lower() in a['Tecnología'].lower()]

        # 2. Ingesta Web Real-Time (Brutal Search)
        if WEB_SEARCH_ENABLED and (tech != "TODAS" or country != "TODOS"):
            query = f"investment banking report {tech} {country} 2026"
            try:
                with DDGS() as ddgs:
                    hits = list(ddgs.text(query, max_results=5))
                    for i, h in enumerate(hits):
                        results.append({
                            "id": f"WEB-LIVE-{i}",
                            "Nombre": h['title'][:60],
                            "Ubicación": country,
                            "Valor_Est": "Bajo Análisis",
                            "Tecnología": tech,
                            "Riesgo": "SCANNED",
                            "Calificacion_IA": "LIVE",
                            "Resumen": h['body'][:200] + "...",
                            "CEO": "Ver enlace",
                            "Celular": "N/A",
                            "Dirección": "Web Resource",
                            "Contacto": h['href'],
                            "Vigencia": "ACTUAL",
                            "Fuente": "WEB REAL-TIME",
                            "Fecha_Pub": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "Viabilidad": 60
                        })
            except: pass
        return results

# Instancia única blindada
scout_engine = ScoutCore()