# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
from datetime import datetime, timedelta

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Fecha de búsqueda: Últimos 60 días para detectar movimientos recientes
        fecha_limite = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        
        # Filtros de exclusión de ruido mediático
        exclude = "-news -reuters -prnewswire -globenewswire -wikipedia -media -press"
        
        # Consultas de CAPA TÉCNICA (Patentes y Permisos)
        queries = [
            f'site:patents.google.com "neutrino energy" OR "SMR nuclear" after:2025-12-31',
            f'filetype:pdf "Environmental Impact Assessment" "Hydrogen" "2026"',
            f'site:iaea.org "SMR" "Preliminary Safety Analysis Report"',
            f'site:epo.org "neutrino" "energy conversion" "patent"',
            f'filetype:pdf "Technical Specifications" "Green Hydrogen" "2026"'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in queries:
                    data = list(ddgs.text(q, max_results=12))
                    for hit in data:
                        results.append({
                            "id": f"TECH-150-{len(results)+1}",
                            "nombre": hit['title'].upper(),
                            "ceo": "Consultar Inventor / Titular de la Patente",
                            "riesgo": "ACTIVO TÉCNICO REGISTRADO (CAPA RAÍZ)",
                            "movil": "Registro de Propiedad Intelectual / Ambiental",
                            "email": "blueprint.150@maia-intelligence.io",
                            "fecha": "Documento Técnico 2026",
                            "fuente": hit['href'],
                            "resumen": hit.get('body', 'Documento de alta densidad técnica detectado en repositorio oficial.')
                        })
        except: pass
        return results

scout_engine = ScoutCore()