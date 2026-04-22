# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # PROTOCOLO DE EXCLUSIÓN TOTAL DE RUIDO
        exclude = "-movie -film -netflix -pelicula -cast -book -trailer"
        
        # MATRIZ DE CAPITAL Y FASES TÉCNICAS (UPME STYLE GLOBAL)
        # Buscamos: Farm-out, Equity Partners, Prefactibilidad, Rondas de inversión
        keywords = '("farm-out" OR "equity partner" OR "pre-feasibility" OR "factibilidad" OR "series A funding" OR "asset divestment")'
        sectores = '("SMR nuclear" OR "green hydrogen" OR "neutrino energy" OR "solar utility" OR "wind offshore")'
        
        # Filtro de dominios de alta autoridad: Gobiernos, LinkedIn y Portales M&A
        query = f'(site:gov OR site:linkedin.com OR site:reuters.com) {keywords} {sectores} {exclude} after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                # Profundidad máxima de 40 conexiones para asegurar un "hit" positivo
                data = list(ddgs.text(query, max_results=40))
                for i, hit in enumerate(data):
                    results.append({
                        "id": f"HUNTER-54-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar Perfil de Inversión / LinkedIn",
                        "riesgo": "ANÁLISIS DE CAPITAL SEMILLA / SERIE A",
                        "movil": "Disponible en Registro Mercantil Regional",
                        "email": "deals@maia-intelligence.io",
                        "fecha": "21/04/2026",
                        "fuente": hit['href'],
                        "resumen": f"DETECCIÓN DE ACTIVO: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
