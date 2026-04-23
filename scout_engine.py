# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Protocolo Nivel 400: Los 8 Pilares de Activos Reales
        asset_pillars = [
            'site:gov OR site:org "Hydroelectric" "award" 2026',
            'site:reuters.com "Solar" "Utility" "deal" 2026',
            'site:world-nuclear-news.org "SMR" "contract" 2026',
            '"Thermal Power" "EPC" "award" 2026',
            'site:thinkgeoenergy.com "Geothermal" "project" 2026',
            '"Neutrino Energy" "investment" 2026',
            '"Hydrogen" "FID" "contract" 2026',
            'site:crunchbase.com "Startup" "funding" 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in asset_pillars:
                    try:
                        # Tiempo de espera reducido para evitar Time-out de página
                        time.sleep(1.0) 
                        data = list(ddgs.text(q, max_results=5))
                        for hit in data:
                            results.append({
                                "id": f"AX-400-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "pilar": q.split('"')[1] if '"' in q else "TECH STARTUP",
                                "vinculo": hit['href'],
                                "datos": hit.get('body', 'Analizando pliegos de condiciones...')
                            })
                    except Exception:
                        continue 
        except Exception:
            pass
        return results

scout_engine = ScoutCore()
