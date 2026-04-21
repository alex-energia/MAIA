# scout_engine.py - CÁPSULA BLINDADA MAIA
from duckduckgo_search import DDGS
import datetime

class ScoutEngine:
    def __init__(self):
        self.vault = [
            {
                "id": "CORP-USA-001", "Nombre": "NuScale VOYGR SMR", "Ubicación": "USA",
                "Potencia": "462 MW", "Tecnología": "SMR Nuclear", "CEO": "John Hopkins",
                "Contacto": "ir@nuscalepower.com", "Celular": "+1 503-350-3900",
                "Dirección": "Portland, Oregon", "Resumen": "Proyecto SMR líder con certificación NRC."
            }
        ]

    def execute_brutal_search(self, country, tech):
        results = [a for a in self.vault if (country == "TODOS" or country.lower() in a['Ubicación'].lower())]
        # Ingesta en tiempo real
        query = f'"{tech}" project {country} "MW" CEO contact 2026'
        with DDGS() as ddgs:
            hits = list(ddgs.text(query, max_results=5))
            for h in hits:
                results.append({
                    "id": "LIVE-SCAN", "Nombre": h['title'][:50], "Ubicación": country,
                    "Tecnología": tech, "Resumen": h['body'][:200], "Contacto": h['href']
                })
        return results

scout_core = ScoutEngine()
