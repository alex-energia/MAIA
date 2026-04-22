# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # PROTOCOLO DE EXCLUSIÓN RADICAL (Nivel 74)
        # Eliminamos: Chat, AI, Películas, Wikipedia y términos genéricos de software
        exclude = "-chat -gpt -ai -openai -chatbot -movie -film -wikipedia -amazon -store -app -essay"
        
        # FOCO EN ACTIVOS DE FASE 1 Y 2 (UPME STYLE GLOBAL)
        # Términos de mercado secundario y cesión de participación
        mercado_negocio = '("farm-out" OR "divestment" OR "equity sale" OR "project for sale" OR "stake sale" OR "pre-feasibility")'
        tecnologias = '("SMR nuclear" OR "Neutrino energy" OR "Green Hydrogen" OR "Offshore Wind" OR "Geothermal")'
        
        # Solo buscamos en dominios industriales y gubernamentales
        query = f'(site:gov OR site:edu OR site:reuters.com OR site:energy.gov) {tecnologias} {mercado_negocio} {exclude} after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                # Rastreo profundo con mayor número de resultados para filtrar
                data = list(ddgs.text(query, max_results=50))
                for i, hit in enumerate(data):
                    # Filtro de seguridad manual extra
                    blacklist = ["openai", "chatbot", "gpt", "movie", "film"]
                    if any(x in hit['title'].lower() for x in blacklist): continue
                        
                    results.append({
                        "id": f"RAW-74-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar M&A Advisor / Director de Proyecto",
                        "riesgo": "ACTIVO INDUSTRIAL DE ALTA PRIORIDAD",
                        "movil": "Acceso Restringido - Requiere NDA",
                        "email": "raw.intel@maia-intelligence.io",
                        "fecha": "21/04/2026",
                        "fuente": hit['href'],
                        "resumen": f"INFORME TÉCNICO DE ACTIVO: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
