# -*- coding: utf-8 -*-
# scout_engine.py - MAIA REAL-TIME SCOUT [DENSITY MODE]
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def __init__(self):
        self._vault = [] 

    def get_risk_rating(self, text):
        text = text.lower()
        if any(w in text for w in ["delay", "protest", "legal", "debt", "risk", "conflict"]):
            return "ALTO"
        if any(w in text for w in ["approved", "certified", "complete", "stable", "partnership"]):
            return "BAJO"
        return "MODERADO"

    def execute_brutal_search(self, country, tech):
        results = []
        query = f'"{tech}" energy infrastructure project {country} "MW" CEO contact 2026'
        
        try:
            with DDGS() as ddgs:
                hits = list(ddgs.text(query, max_results=15))
                for i, h in enumerate(hits):
                    risk = self.get_risk_rating(h['body'])
                    results.append({
                        "id": f"REAL-{i}",
                        "Nombre": h['title'][:75],
                        "Ubicación": country.upper(),
                        "Tecnología": tech.upper(),
                        "Resumen": h['body'][:450],
                        "Contacto": h['href'],
                        "CEO": "Consultar en fuente original",
                        "Riesgo": risk,
                        "Fecha_Rastreo": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    })
        except Exception as e:
            print(f"Error de conexión: {e}")
                
        return results

    def generate_summary_table(self, results):
        """Genera el resumen estadístico para el cuadro final"""
        summary = {}
        for r in results:
            t = r['Tecnología']
            summary[t] = summary.get(t, 0) + 1
        return summary

scout_engine = ScoutCore()
