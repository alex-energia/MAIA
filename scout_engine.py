# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # FECHA LÍMITE: 21 de Marzo de 2026 (Vigencia 30 días)
        # BÚSQUEDA NIVEL 31: Triangulación de Fondos, Brokers y Rondas
        capital_terms = '("Series A funding" OR "Series B" OR "seed round" OR "private equity" OR "venture capital" OR "investment round")'
        asset_terms = '("asset for sale" OR "divestment" OR "project acquisition" OR "equity offering" OR "partnership opportunity")'
        tech_terms = '("SMR nuclear" OR "green hydrogen" OR "neutrino energy" OR "geothermal project")'
        
        # Incursión en dominios de Brokers y Fondos de Inversión (Internacional)
        query = f'({capital_terms} OR {asset_terms}) {tech_terms} 2026 after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                # Maximizamos la recolección para filtrar solo lo más relevante
                search_data = list(ddgs.text(query, max_results=25))
                for i, hit in enumerate(search_data):
                    results.append({
                        "id": f"CAP-31-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar Estructura de Capital en Crunchbase / Bloomberg",
                        "riesgo": "GRADO DE INVERSIÓN: ANÁLISIS DE LIQUIDEZ ACTIVO",
                        "movil": "Disponible en Terminal de Broker",
                        "email": "capital.scout@maia-intelligence.net",
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                        "fuente": hit['href'],
                        "resumen": f"INTELIGENCIA DE CAPITAL: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()