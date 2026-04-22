# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # EXCLUSIÓN TOTAL DE RUIDO (Software, IA, Media)
        exclude = "-chat -gpt -ai -openai -chatbot -movie -film -netflix -app -software -essay -wikipedia"
        
        # FOCO: Eventos de Capital y Permisos de Red (Deep Infrastructure)
        capital_signals = '("Series A" OR "Series B" OR "closed funding" OR "equity round")'
        technical_permits = '("interconnection queue" OR "grid access" OR "feasibility study" OR "pre-factibilidad")'
        sectors = '("SMR nuclear" OR "Green Hydrogen" OR "Neutrino energy" OR "Offshore solar")'
        
        # Búsqueda en silos de información de alta autoridad
        query = f'(site:gov OR site:reuters.com OR site:bloomberg.com) {sectors} ({capital_signals} OR {technical_permits}) {exclude} after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                data = list(ddgs.text(query, max_results=100))
                for i, hit in enumerate(data):
                    # Hard-filter contra falsos positivos de IA
                    if any(x in hit['body'].lower() for x in ["openai", "chatbot", "gpt"]): continue
                    
                    results.append({
                        "id": f"INFILTRATOR-100-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar Lead de Inversión en LinkedIn",
                        "riesgo": "ACTIVO ESTRATÉGICO / CAPITAL DETECTADO",
                        "movil": "Requiere Acceso a Registro Mercantil",
                        "email": "blackbox@maia-core.io",
                        "fecha": "21/04/2026",
                        "fuente": hit['href'],
                        "resumen": f"INTELIGENCIA CRÍTICA: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
