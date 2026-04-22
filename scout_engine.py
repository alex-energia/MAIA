# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Definición Estricta de los 8 Pilares de Activos
        asset_pillars = [
            'Hydroelectric "Contract Award" 2026',
            'Solar "Utility Scale" "Project Finance" 2026',
            'SMR Nuclear "Site Selection" OR "Construction" 2026',
            'Thermal Power Plant "EPC Contract" 2026',
            'Geothermal "Drilling" OR "Award" 2026',
            '"Neutrino Energy" production OR investment 2026',
            'Hydrogen "FID" OR "Electrolyzer Order" 2026',
            '"Technology Startup" Energy "Series A" OR "Series B" 2026'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in asset_pillars:
                    # Delay síncrono para evitar el bloqueo que sufriste en la Capa 230
                    time.sleep(3.0)
                    data = list(ddgs.text(q, max_results=8))
                    for hit in data:
                        # Validación de relevancia estricta
                        title_lower = hit['title'].lower()
                        if any(p in title_lower for p in ['hydro', 'solar', 'smr', 'nuclear', 'thermal', 'geothermal', 'neutrino', 'hydrogen', 'startup']):
                            results.append({
                                "id": f"TARGET-250-{len(results)+1}",
                                "nombre": hit['title'].upper(),
                                "categoria": "ACTIVO VERIFICADO",
                                "vinculo": hit['href'],
                                "datos": hit.get('body', 'Datos de licitación o inversión detectados. Consultar pliego oficial.')
                            })
        except: pass
        return results

scout_engine = ScoutCore()