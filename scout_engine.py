# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Nivel 600: Enfoque 100% Negocios y Proyectos Reales (Excluye noticias)
        # Operadores agresivos: "tender", "contract", "FID", "award"
        asset_pillars = [
            'site:dgmarket.com "Hydroelectric" tender 2026',
            'site:tendersinfo.com "Solar" project award 2026',
            'site:iaea.org "SMR" construction contract 2026',
            'site:power-technology.com "Thermal" EPC project 2026',
            'site:geothermal-energy.org "Drilling" contract 2026',
            '"Neutrino Energy" investment agreement 2026',
            'site:hydrogen-central.com "FID" project 2026',
            'site:crunchbase.com "Startup" Series A investment 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in asset_pillars:
                    try:
                        time.sleep(0.5) # Velocidad máxima permitida
                        # Limitamos a 2 resultados críticos por pilar para evitar el Timeout del servidor
                        data = list(ddgs.text(q, max_results=2))
                        for hit in data:
                            results.append({
                                "id": f"BUS-600-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "pilar": q.split('"')[1] if '"' in q else "NEGOCIO TECH",
                                "vinculo": hit['href'],
                                "datos": hit.get('body', 'Analizando viabilidad del proyecto...')
                            })
                    except: continue 
        except: pass
        return results

scout_engine = ScoutCore()
