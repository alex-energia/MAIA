# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Query de 360 grados: Desde el diseño hasta la venta de acciones
        # Cubre: Tender (Licitación), Design, M&A (Acciones), IPO, O&M.
        sectores = '("hydroelectric" OR "solar" OR "wind" OR "SMR nuclear" OR "geothermal" OR "hydrogen")'
        etapas = '("tender" OR "RFP" OR "design phase" OR "acquisition" OR "shares sale" OR "equity" OR "EPC contract")'
        query = f'{sectores} {etapas} 2026 after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                search_data = list(ddgs.text(query, max_results=10))
                for i, hit in enumerate(search_data):
                    results.append({
                        "id": f"BSN-2026-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar Estructura de Capital",
                        "riesgo": "ANÁLISIS DE CICLO DE VIDA ACTIVO",
                        "movil": "Disponible en Dossier Comercial",
                        "email": "deals@maia-intelligence.com",
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                        "fuente": hit['href'],
                        "resumen": f"DETECCIÓN DE OPORTUNIDAD (Etapa Negocio): {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
