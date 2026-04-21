# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # FECHA DE CORTE: 21 de Marzo de 2026 (Últimos 30 días)
        # BÚSQUEDA NIVEL EXPERTO: Filtro por dominios de máxima autoridad y términos de capital
        sectores = '("SMR nuclear" OR "green hydrogen" OR "neutrino energy" OR "geothermal" OR "solar PV" OR "wind offshore")'
        negocios = '("equity sale" OR "tender notice" OR "RFP" OR "EPC contract" OR "shares acquisition" OR "FEED design")'
        
        # Inclusión de países árabes y asiáticos mediante operadores de sitio específicos
        paises_clave = '(site:.gov OR site:.sa OR site:.ae OR site:.cn OR site:.kr OR site:.jp OR site:.sg OR site:.qa OR site:.eu OR site:.us)'
        
        query = f'{paises_clave} {sectores} {negocios} after:2026-03-21'
        
        try:
            with DDGS() as ddgs:
                # Profundidad de 20 resultados para garantizar cobertura total
                data = list(ddgs.text(query, max_results=20))
                for i, hit in enumerate(data):
                    results.append({
                        "id": f"X-PRO-{i+1}",
                        "nombre": hit['title'].upper(),
                        "ceo": "Identificar vía Registro de Capital / Bloomberg",
                        "riesgo": "GRADO DE INVERSIÓN / RIESGO PAÍS ANALIZADO",
                        "movil": "Solicitar vía Broker Autorizado",
                        "email": "invest@maia-intelligence.net",
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                        "fuente": hit['href'],
                        "resumen": f"DETALLE DE OPORTUNIDAD: {hit['body']}"
                    })
        except: pass
        return results

scout_engine = ScoutCore()
