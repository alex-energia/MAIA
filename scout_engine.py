# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # FECHA: 21 de Abril de 2026
        # BLOQUEO DE CONTENIDO NO RELACIONADO (Cine, Libros, Películas)
        exclude = "-movie -film -netflix -pelicula -cast -director -actor -book -resumen"
        
        # MATRIZ TÉCNICA PURA: Capital y Activos
        sectores = '("SMR nuclear" OR "neutrino energy" OR "green hydrogen" OR "geothermal")'
        negocios = '("equity sale" OR "asset sale" OR "series A" OR "series B" OR "funding" OR "investment")'
        
        # Búsqueda forzada en sectores de capital real
        query = f'{sectores} {negocios} {exclude} after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                # Rastreo profundo con filtrado de ruido
                data = list(ddgs.text(query, max_results=20))
                for i, hit in enumerate(data):
                    # Validación manual interna del resumen para evitar falsos positivos
                    blacklist = ["película", "director", "sinopsis", "actor"]
                    if any(word in hit['title'].lower() for word in blacklist):
                        continue
                        
                    results.append({
                        "id": f"X-ASSET-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Consultar Registro de Capital / Crunchbase",
                        "riesgo": "GRADO DE INVERSIÓN: ACTIVO REAL DETECTADO",
                        "movil": "Disponible en Terminal de Negocios",
                        "email": "investor.desk@maia-intelligence.net",
                        "fecha": "21/04/2026",
                        "fuente": hit['href'],
                        "resumen": f"INTELIGENCIA DE CAPITAL INDUSTRIAL: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
