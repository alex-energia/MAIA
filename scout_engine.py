# -*- coding: utf-8 -*-
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def __init__(self):
        self.Paises = ["AMERICA", "EUROPA", "CHINA", "TAIWAN", "KOREA DEL SUR", "SINGAPUR", "JAPON", "EMIRATOS ARABES", "QATAR", "ARABIA SAUDITA"]
        self.Tecnologias = ["SOLAR", "EÓLICA", "HIDROELÉCTRICA", "HIDRÓGENO VERDE", "SMR NUCLEAR", "NEUTRINO", "TERMICA", "GEOTERMICA", "STARTUP", "BIOMASA"]

    def execute_brutal_search(self, country, tech, is_global=False):
        results = []
        c_val = country if (country and country != "BORRAR") else ""
        t_val = tech if (tech and tech != "BORRAR") else "Energy"
        query = f'latest energy projects 2026 "CEO" "contact"' if is_global else f'"{t_val}" project in {c_val} "MW" CEO name mobile address 2026'
        
        try:
            with DDGS() as ddgs:
                search_data = list(ddgs.text(query, max_results=10))
                for i, hit in enumerate(search_data):
                    results.append({
                        "id": f"MAIA-{datetime.datetime.now().strftime('%M%S')}-{i}",
                        "Nombre_Proyecto": hit['title'][:90],
                        "Ubicacion_Pais": c_val.upper() if c_val else "GLOBAL",
                        "Tecnologia_Tipo": t_val.upper(),
                        "Estado_Riesgo": "ANALIZANDO",
                        "Resumen_Ejecutivo": hit['body'][:500],
                        "URL_Fuente": hit['href'],
                        "Nombre_CEO": "Consultar Fuente",
                        "Telefono_Contacto": "Ver en sitio",
                        "Direccion_Sede": "Sede Central",
                        "Fecha_Rastreo": datetime.datetime.now().strftime("%d/%m/%Y")
                    })
        except: pass
        return results

scout_engine = ScoutCore()
