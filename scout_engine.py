# -*- coding: utf-8 -*-
# scout_engine.py - MAIA DENSITY SHIELD V.3
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def __init__(self):
        # Listas Maestras
        self.Paises = [
            "AMERICA", "EUROPA", "CHINA", "TAIWAN", 
            "KOREA DEL SUR", "SINGAPUR", "JAPON", 
            "EMIRATOS ARABES", "QATAR", "ARABIA SAUDITA"
        ]
        
        self.Tecnologias = [
            "SOLAR", "EÓLICA", "HIDROELÉCTRICA", "HIDRÓGENO VERDE", 
            "SMR NUCLEAR", "NEUTRINO", "TERMICA", "GEOTERMICA", 
            "STARTUP", "BIOMASA"
        ]

    def get_risk_rating(self, text):
        text = text.lower()
        if any(w in text for w in ["delay", "protest", "legal", "debt", "risk", "conflict", "stopped", "lawsuit"]):
            return "ALTO"
        if any(w in text for w in ["approved", "certified", "complete", "stable", "partnership", "success"]):
            return "BAJO"
        return "MODERADO"

    def execute_brutal_search(self, country, tech, is_global=False):
        results = []
        
        # Construcción de la Query real
        if is_global:
            query = 'latest energy infrastructure projects "MW" CEO contact 2026'
        else:
            # Validamos que no vengan vacíos
            c_query = country if country and country != "BORRAR" else "Global"
            t_query = tech if tech and tech != "BORRAR" else "Energy"
            query = f'"{t_query}" project in {c_query} "MW" CEO contact 2026'
        
        try:
            with DDGS() as ddgs:
                # Ejecución de la búsqueda en la red
                max_h = 15 if is_global else 10
                search_hits = list(ddgs.text(query, max_results=max_h))
                
                for i, h in enumerate(search_hits):
                    risk = self.get_risk_rating(h['body'])
                    
                    # Detección de tecnología para el resumen
                    detected_tech = tech if not is_global else "INFRAESTRUCTURA"
                    if is_global:
                        for t in self.Tecnologias:
                            if t.lower() in h['title'].lower() or t.lower() in h['body'].lower():
                                detected_tech = t
                                break

                    results.append({
                        "id": f"SC-{i}-{datetime.datetime.now().microsecond}",
                        "Nombre": h['title'][:80],
                        "Ubicación": country.upper() if country else "GLOBAL",
                        "Tecnología": detected_tech.upper() if detected_tech else "GENERAL",
                        "Resumen": h['body'][:500],
                        "Contacto": h['href'],
                        "CEO": "Identificado en fuente",
                        "Riesgo": risk,
                        "Fecha_Rastreo": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    })
        except Exception as e:
            print(f"ERROR EN MOTOR: {e}")
                
        return results

    def generate_summary_table(self, results):
        summary = {}
        for r in results:
            t = r['Tecnología']
            summary[t] = summary.get(t, 0) + 1
        return summary

scout_engine = ScoutCore()