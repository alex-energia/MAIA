# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import datetime

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # FECHA: Retroceso de 60 días (Desde Feb 2026)
        # FOCO: Documentos de ingeniería y financieros (.pdf, .xlsx)
        queries = [
            'filetype:pdf "Interconnection Queue" "Status: Active" "Hydrogen"',
            'filetype:pdf "SMR" "Feasibility Study" "Grant Award" 2026',
            'site:ted.europa.eu "Prior information notice" "SMR" OR "Hydrogen"',
            '"Neutrino energy" "Investment Teaser" filetype:pdf'
        ]
        
        exclude = "-chat -gpt -ai -openai -movie -film -wikipedia"

        try:
            with DDGS() as ddgs:
                for q in queries:
                    full_q = f"{q} {exclude} after:2026-02-20"
                    data = list(ddgs.text(full_q, max_results=25))
                    for hit in data:
                        results.append({
                            "id": f"NODE-110-{len(results)+1}",
                            "nombre": hit['title'].upper(),
                            "tipo": "ACTIVO DE INFRAESTRUCTURA REAL",
                            "estado": "DETECTADO EN REGISTRO TÉCNICO",
                            "fuente": hit['href'],
                            "resumen": hit['body'][:250] + "..."
                        })
        except: pass
        return results

scout_engine = ScoutCore()