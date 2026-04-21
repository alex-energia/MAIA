# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Dominios estratégicos incluyendo ME y Asia (KSA, UAE, China, KR, JP, SG, QA)
        regiones = '(site:.gov OR site:.sa OR site:.ae OR site:.cn OR site:.kr OR site:.jp OR site:.sg OR site:.qa OR site:.eu)'
        
        # Matriz 360: Energía (todas las ramas), Startups, Neutrinos y Capital
        sectores = '("SMR nuclear" OR "green hydrogen" OR "neutrino energy" OR "solar" OR "wind" OR "geothermal")'
        etapas = '("tender" OR "RFP" OR "equity sale" OR "shares" OR "EPC" OR "design phase" OR "sovereign fund")'
        
        # Vigencia: 30 días (desde el 21 de Marzo de 2026)
        query = f'{regiones} {sectores} {etapas} 2026 after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                # Aumentamos a 15 resultados para cubrir la expansión geográfica
                search_data = list(ddgs.text(query, max_results=15))
                for i, hit in enumerate(search_data):
                    results.append({
                        "id": f"GLB-360-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar Registro de Inversión Local",
                        "riesgo": "GRADO DE INVERSIÓN GLOBAL",
                        "movil": "Disponible en Terminal de Datos",
                        "email": "global.scout@maia-intelligence.com",
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                        "fuente": hit['href'],
                        "resumen": f"DETECCIÓN ESTRATÉGICA (Región Expandida): {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
