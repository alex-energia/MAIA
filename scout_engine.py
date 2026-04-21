# -*- coding: utf-8 -*-
import datetime
from duckduckgo_search import DDGS

class ScoutCore:
    def execute_global_scout(self):
        results = []
        query = 'latest energy infrastructure projects 2026 "CEO" "MW" "investment"'
        try:
            with DDGS() as ddgs:
                search_data = list(ddgs.text(query, max_results=12))
                for i, hit in enumerate(search_data):
                    body = hit['body'].lower()
                    # Clasificación de riesgo con lógica de palabras clave
                    risk_val = "BAJO"
                    if any(x in body for x in ["debt", "protest", "delay", "risk"]): risk_val = "ALTO"
                    elif any(x in body for x in ["planning", "proposal", "early"]): risk_val = "MODERADO"

                    results.append({
                        "id": f"MAIA-INTEL-{datetime.datetime.now().strftime('%M%S')}-{i}",
                        "nombre": hit['title'][:90].upper(),
                        "tecnologia": "RENOVABLE / ALTA PRESIÓN",
                        "ubicacion": "DETECCIÓN GEOGRÁFICA EN FUENTE",
                        "capacidad": "MW ESTIMADOS POR PROYECCIÓN",
                        "riesgo": risk_val,
                        "resumen": self.elaborate_summary(hit['body']),
                        "fuente": hit['href'],
                        "ceo": "DATOS EN FUENTE ORIGINAL",
                        "fecha": datetime.datetime.now().strftime("%d/%m/%Y")
                    })
        except: pass
        return results

    def elaborate_summary(self, text):
        """Genera un resumen más profesional y estructurado"""
        puntos = text.split('.')
        intro = puntos[0] if len(puntos) > 0 else text
        desarrollo = puntos[1] if len(puntos) > 1 else "Análisis técnico pendiente de validación profunda."
        return f"ANÁLISIS ESTRATÉGICO: {intro}. IMPLICACIONES OPERATIVAS: {desarrollo}. ESTADO ACTUAL: Fase de monitoreo 2026 activa."

scout_engine = ScoutCore()