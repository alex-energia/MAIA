# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Pilares de Búsqueda Sensible Nivel 300 - Optimizados
        asset_pillars = [
            'site:sam.gov "Hydroelectric" 2026',
            'site:reuters.com "Solar Utility" "Agreement" 2026',
            'site:world-nuclear-news.org "SMR" 2026',
            '"Thermal Power" EPC 2026',
            'site:thinkgeoenergy.com "Geothermal" 2026',
            '"Neutrino Energy" investment 2026',
            '"Hydrogen" FID 2026',
            'site:crunchbase.com "Startup" 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in asset_pillars:
                    try:
                        # Reducción de tiempo de espera por pilar para evitar timeout del servidor
                        time.sleep(1.2) 
                        data = list(ddgs.text(q, max_results=4))
                        for hit in data:
                            results.append({
                                "id": f"DATA-300-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "pilar": q.split('"')[1] if '"' in q else "STARTUP",
                                "vinculo": hit['href'],
                                "datos": hit.get('body', 'Analizando...')
                            })
                    except: continue 
        except Exception: pass
        return results

scout_engine = ScoutCore()
