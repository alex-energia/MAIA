# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Query enfocada en licitaciones, RFPs y desarrollos de infraestructura 2026
        query = 'energy infrastructure "tender" "RFP" "bidding" 2026 "MW capacity"'
        try:
            with DDGS() as ddgs:
                data = list(ddgs.text(query, max_results=10))
                for i, hit in enumerate(data):
                    # Calificación de Riesgo basada en keywords de negocio
                    risk = "BAJO"
                    if any(x in hit['body'].lower() for x in ["delay", "court", "opposed"]): risk = "ALTO"
                    
                    results.append({
                        "id": f"OP-2026-{i+1}",
                        "nombre": hit['title'].upper(),
                        "resumen": f"OPORTUNIDAD DE NEGOCIO: {hit['body']}",
                        "ubicacion": "COORDENADAS EN FUENTE",
                        "fuente": hit['href'],
                        "riesgo": risk,
                        "contacto": "Consultar en pliego de condiciones (ver link)"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
