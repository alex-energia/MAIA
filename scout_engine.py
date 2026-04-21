# -*- coding: utf-8 -*-
# scout_engine.py - MAIA DENSITY SHIELD V.1
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def __init__(self):
        # Listas Maestras para los Desplegables
        self.Paises = ["COLOMBIA", "USA", "ESPAÑA", "MÉXICO", "CHILE", "ARABIA SAUDITA", "BRASIL", "PANAMÁ"]
        self.Tecnologias = ["SOLAR", "EÓLICA", "HIDROELÉCTRICA", "HIDRÓGENO VERDE", "SMR NUCLEAR", "NEUTRINO", "BIOMASA"]

    def get_risk_rating(self, text):
        """Analiza el riesgo basado en semántica de red"""
        text = text.lower()
        if any(w in text for w in ["delay", "protest", "legal", "debt", "risk", "conflict", "stopped"]):
            return "ALTO"
        if any(w in text for w in ["approved", "certified", "complete", "stable", "partnership", "success"]):
            return "BAJO"
        return "MODERADO"

    def execute_brutal_search(self, country, tech, is_global=False):
        """
        is_global: Si es True, busca en todas las tecnologías y países de la lista maestra.
        """
        results = []
        
        # Definir los términos de búsqueda
        search_country = "Global" if is_global else country
        search_tech = "Energy Infrastructure" if is_global else tech
        
        query = f'"{search_tech}" project {search_country} "MW" CEO contact 2026'
        
        try:
            with DDGS() as ddgs:
                # Si es global, aumentamos el número de resultados para cubrir más terreno
                max_h = 25 if is_global else 12
                hits = list(ddgs.text(query, max_results=max_h))
                
                for i, h in enumerate(hits):
                    risk = self.get_risk_rating(h['body'])
                    # En modo global, intentamos detectar qué tecnología es
                    detected_tech = tech if not is_global else "INFRAESTRUCTURA"
                    for t in self.Tecnologias:
                        if t.lower() in h['title'].lower() or t.lower() in h['body'].lower():
                            detected_tech = t
                            break

                    results.append({
                        "id": f"SC-{i}",
                        "Nombre": h['title'][:80],
                        "Ubicación": search_country.upper(),
                        "Tecnología": detected_tech,
                        "Resumen": h['body'][:500],
                        "Contacto": h['href'],
                        "CEO": "Verificar en link adjunto",
                        "Riesgo": risk,
                        "Fecha_Rastreo": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    })
        except Exception as e:
            print(f"Error de conexión en Scout: {e}")
                
        return results

    def generate_summary_table(self, results):
        """Genera el resumen estadístico por tecnología"""
        summary = {}
        for r in results:
            t = r['Tecnología']
            summary[t] = summary.get(t, 0) + 1
        return summary

scout_engine = ScoutCore()