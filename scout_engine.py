# -*- coding: utf-8 -*-
# scout_engine.py - MAIA DENSITY SHIELD V.5 - FULL DATA EXTRACTION
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def __init__(self):
        # Listas Maestras según requerimiento exacto
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
        
        if is_global:
            query = 'latest energy infrastructure projects "MW" CEO "contact" 2026'
        else:
            c_query = country if (country and country != "BORRAR") else ""
            t_query = tech if (tech and tech != "BORRAR") else "Energy"
            query = f'"{t_query}" project in {c_query} "MW" CEO name "mobile" "address" 2026'
        
        try:
            with DDGS() as ddgs:
                max_hits = 15 if is_global else 12
                search_data = list(ddgs.text(query, max_results=max_hits))
                
                for i, hit in enumerate(search_data):
                    risk = self.get_risk_rating(hit['body'])
                    
                    # Lógica de detección de tecnología para Scout Global
                    detected_tech = tech if not is_global else "INFRAESTRUCTURA"
                    if is_global:
                        for t in self.Tecnologias:
                            if t.lower() in hit['title'].lower() or t.lower() in hit['body'].lower():
                                detected_tech = t
                                break

                    # FICHA CON TODOS LOS CAMPOS SOLICITADOS
                    results.append({
                        "id": f"MAIA-PRJ-{datetime.datetime.now().strftime('%y%m')}-{i}",
                        "Nombre_Proyecto": hit['title'][:90],
                        "Ubicacion_Pais": country.upper() if (country and country != "BORRAR") else "GLOBAL",
                        "Tecnologia_Tipo": detected_tech.upper() if detected_tech else "GENERAL",
                        "Capacidad_Estimada": "Verificar en Documentación (MW)",
                        "Estado_Riesgo": risk,
                        "Resumen_Ejecutivo": hit['body'][:600],
                        "URL_Fuente": hit['href'],
                        # Campos de contacto expandidos según corrección previa
                        "Nombre_CEO": "Análisis de enlace requerido",
                        "Telefono_Contacto": "Disponible en fuente",
                        "Direccion_Sede": "Consultar registro legal en fuente",
                        "Fecha_Rastreo": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    })
        except Exception as e:
            print(f"CRITICAL ENGINE ERROR: {e}")
                
        return results

    def generate_summary_table(self, results):
        summary = {}
        for r in results:
            t = r['Tecnologia_Tipo']
            summary[t] = summary.get(t, 0) + 1
        return summary

scout_engine = ScoutCore()
