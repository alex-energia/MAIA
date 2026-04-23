# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Protocolo 500: 8 Pilares con enfoque geográfico diversificado
        # Se reducen resultados por pilar para garantizar que el servidor responda a tiempo
        asset_pillars = [
            'site:reuters.com OR site:worldbank.org "Hydroelectric" "contract" 2026',
            'site:energy-storage.news OR site:pv-magazine.com "Solar" "deal" 2026',
            'site:world-nuclear-news.org "SMR" OR "Micro-reactor" "construction" 2026',
            'site:power-technology.com "Thermal Power" "EPC" 2026',
            'site:thinkgeoenergy.com "Geothermal" "award" 2026',
            '"Neutrino Energy" OR "Neutrinovoltaic" "investment" 2026',
            'site:h2-view.com "Hydrogen" "FID" OR "project" 2026',
            'site:techcrunch.com OR site:dealroom.co "Startup" "Series A" 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in asset_pillars:
                    try:
                        # Delay mínimo para maximizar velocidad sin ser bloqueado
                        time.sleep(0.8) 
                        # Pedimos solo 3 resultados por pilar (24 en total) para evitar el Timeout
                        data = list(ddgs.text(q, max_results=3))
                        for hit in data:
                            results.append({
                                "id": f"G500-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "pilar": q.split('"')[1] if '"' in q else "STARTUP",
                                "vinculo": hit['href'],
                                "datos": hit.get('body', 'Extrayendo metadatos del activo...')
                            })
                    except:
                        continue 
        except:
            pass
        return results

scout_engine = ScoutCore()