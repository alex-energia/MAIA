# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
from datetime import datetime, timedelta

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Ampliamos el espectro: Buscamos acuerdos de suministro y MOUs (Memorándum de Entendimiento)
        queries = [
            'site:bloomberg.com "partnership" OR "agreement" ("Hydrogen" OR "SMR") 2026',
            'site:world-nuclear-news.org "SMR" "site selection" OR "licensing"',
            'site:reuters.com "investment" "clean energy" "neutrino" -wiki',
            '"Rolls-Royce SMR" "contract" 2026',
            '"Neutrino Energy Group" "production facility" OR "partnership"',
            'site:energy.gov "funding award" "hydrogen" 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in queries:
                    data = list(ddgs.text(q, max_results=15))
                    for hit in data:
                        # Filtro de calidad: Solo si el título tiene más de 20 caracteres (evita basura)
                        if len(hit['title']) > 20:
                            results.append({
                                "id": f"ACTIVO-160-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "ceo": "Analizar Firmantes del Acuerdo",
                                "riesgo": "SEÑAL POSITIVA - ALIANZA ESTRATÉGICA",
                                "movil": "Terminal de Noticias Financieras",
                                "email": "supply.160@maia-intelligence.io",
                                "fecha": "Actualizado Abril 2026",
                                "fuente": hit['href'],
                                "resumen": hit.get('body', 'Análisis de cadena de suministro disponible en el origen.')
                            })
        except: pass
        return results

scout_engine = ScoutCore()
