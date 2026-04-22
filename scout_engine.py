# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Pilares de Búsqueda Sensible Nivel 300
        asset_pillars = [
            'site:gov OR site:org "Hydroelectric" "procurement" 2026',
            'site:reuters.com OR site:bloomberg.com "Solar" "Utility" "Agreement" 2026',
            'site:world-nuclear-news.org "SMR" "Construction" OR "Contract" 2026',
            '"Thermal Power" "EPC Award" 2026',
            'site:thinkgeoenergy.com "Geothermal" "Drilling Contract" 2026',
            '"Neutrino Energy" OR "Neutrinovoltaic" "Investment" 2026',
            '"Hydrogen" "Final Investment Decision" 2026',
            'site:crunchbase.com OR site:techcrunch.com "Startup" "Series A" OR "Series B" 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in asset_pillars:
                    try:
                        # Rotación de tiempo para evitar detección de bot
                        time.sleep(2.5) 
                        data = list(ddgs.text(q, max_results=7))
                        for hit in data:
                            results.append({
                                "id": f"DATA-300-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "pilar": q.split('"')[1] if '"' in q else "TECH STARTUP",
                                "vinculo": hit['href'],
                                "datos": hit.get('body', 'Análisis de activo en curso...')
                            })
                    except: continue 
        except Exception: pass
        return results

scout_engine = ScoutCore()