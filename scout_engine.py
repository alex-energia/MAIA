# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # PROTOCOLO DE EXCLUSIÓN TOTAL: Eliminamos ruido de IA y consumo
        exclude = "-chat -gpt -ai -openai -chatbot -movie -film -netflix -app -software -essay -wikipedia"
        
        # FOCO: Dinero Real y Permisos de Ingeniería (UPME Global Style)
        terminos_capital = '("Series A" OR "Series B" OR "funding round" OR "capital injection" OR "private placement")'
        permisos_red = '("interconnection queue" OR "grid access permit" OR "feasibility study" OR "Fase 2")'
        sectores = '("SMR nuclear" OR "Green Hydrogen" OR "Neutrino energy" OR "Long-duration storage")'
        
        # Búsqueda en dominios de alta fidelidad: Registros gubernamentales y Reuters/Bloomberg
        query = f'(site:gov OR site:reuters.com OR site:energy-storage.news) {sectores} ({terminos_capital} OR {permisos_red}) {exclude} after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                data = list(ddgs.text(query, max_results=70))
                for i, hit in enumerate(data):
                    # Filtro de seguridad: Bloqueo de falsos positivos
                    if any(x in hit['body'].lower() for x in ["openai", "chat", "gpt"]): continue
                        
                    results.append({
                        "id": f"DEEP-94-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Identificar vía Registro Mercantil Regional",
                        "riesgo": "SEÑAL DE CAPITAL / FASE TÉCNICA DETECTADA",
                        "movil": "Disponible en Terminal Financiera / Registro de Red",
                        "email": "intel.94@maia-core.io",
                        "fecha": "21/04/2026",
                        "fuente": hit['href'],
                        "resumen": f"DETECCIÓN DE SEÑAL CRÍTICA: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
