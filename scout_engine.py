# -*- coding: utf-8 -*-
# scout_engine.py - MAIA DENSITY SHIELD V.2
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def __init__(self):
        # Listas Maestras solicitadas por el usuario
        self.Paises = [
            "AMERICA", 
            "EUROPA", 
            "CHINA", 
            "TAIWAN", 
            "KOREA DEL SUR", 
            "SINGAPUR", 
            "JAPON", 
            "EMIRATOS ARABES", 
            "QATAR", 
            "ARABIA SAUDITA"
        ]
        
        self.Tecnologias = [
            "SOLAR", 
            "EÓLICA", 
            "HIDROELÉCTRICA", 
            "HIDRÓGENO VERDE", 
            "SMR NUCLEAR", 
            "NEUTRINO", 
            "TERMICA", 
            "GEOTERMICA", 
            "STARTUP", 
            "BIOMASA"
        ]

    def get_risk_rating(self, text):
        """Analiza el riesgo basado en semántica de red real"""
        text = text.lower()
        if any(w in text for w in ["delay", "protest", "legal", "debt", "risk", "conflict", "stopped", "lawsuit"]):
            return "ALTO"
        if any(w in text for w in ["approved", "certified", "complete", "stable", "partnership", "success", "signed"]):
            return "BAJO"
        return "MODERADO"

    def execute_brutal_search(self, country, tech, is_global=False):
        """
        Ejecuta la búsqueda real en la red.
        Si is_global es True, busca tendencias generales de infraestructura.
        """
        results = []
        
        # Construcción de la Query de búsqueda real
        if is_global:
            query = 'latest energy infrastructure projects "MW" CEO contact 2026'
            search_country = "GLOBAL"
            search_tech = "MULTIPLE"
        else:
            # Si el usuario no seleccionó algo válido, evitamos error
            c_query = country if country else ""
            t_query = tech if tech else "energy"
            query = f'"{t_query}" project in {c_query} "MW" CEO contact 2026'
            search_country = country.upper() if country else "NO ESPECIFICADO"
            search_tech = tech.upper() if tech else "GENERAL"
        
        try:
            with DDGS() as ddgs:
                # Limitamos a 15 resultados para mantener la velocidad
                max_results = 20 if is_global else 12
                hits = list(ddgs.text(query, max_results=max_results))
                
                for i, h in enumerate(hits):
                    risk = self.get_risk_rating(h['body'])
                    
                    # Intentar identificar la tecnología si es búsqueda global
                    current_tech = search_tech
                    if is_global:
                        for t in self.Tecnologias:
                            if t.lower() in h['title'].lower() or t.lower() in h['body'].lower():
                                current_tech = t
                                break

                    results.append({
                        "id": f"SC-{i}-{datetime.datetime.now().microsecond}",
                        "Nombre": h['title'][:85],
                        "Ubicación": search_country,
                        "Tecnología": current_tech,
                        "Resumen": h['body'][:500],
                        "Contacto": h['href'],
                        "CEO": "Identificado en enlace externo",
                        "Riesgo": risk,
                        "Fecha_Rastreo": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    })
        except Exception as e:
            print(f"ERROR CRÍTICO EN SCOUT: {e}")
                
        return results

    def generate_summary_table(self, results):
        """Genera el cuadro de resumen estadístico solicitado"""
        summary = {}
        for r in results:
            t = r['Tecnología']
            summary[t] = summary.get(t, 0) + 1
        return summary

scout_engine = ScoutCore()