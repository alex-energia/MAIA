# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
from datetime import datetime, timedelta

class ScoutCore:
    def execute_global_scout(self):
        results = []
        # Retroceso de 60 días desde la fecha actual (Abril 2026)
        fecha_limite = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        
        # Filtros de exclusión para evitar ruido enciclopédico y de IA
        exclude = "-wikipedia -britannica -dictionary -chatgpt -openai -ai -software -app -movie"
        
        # Consultas de infiltración en nodos de autoridad (Capital, Red y Licitaciones)
        queries = [
            f'site:reuters.com "funding" OR "investment" ("SMR nuclear" OR "Green Hydrogen") {exclude} after:{fecha_limite}',
            f'site:energy-storage.news "contract" OR "project finance" "neutrino" OR "storage" {exclude} after:{fecha_limite}',
            f'site:world-nuclear-news.org "SMR" "construction" OR "permit" {exclude} after:{fecha_limite}',
            f'filetype:pdf "Interconnection Queue" "Active" "Hydrogen" {exclude} after:{fecha_limite}',
            f'site:ted.europa.eu "Prior information notice" "Energy" {exclude}'
        ]
        
        try:
            with DDGS() as ddgs:
                for q in queries:
                    data = list(ddgs.text(q, max_results=15))
                    for hit in data:
                        # Verificación de seguridad para asegurar que el resumen no esté vacío
                        resumen_texto = hit.get('body', 'Sin detalle técnico disponible en la vista previa.')
                        
                        results.append({
                            "id": f"ASSET-130-{len(results)+1}",
                            "nombre": hit['title'].upper(),
                            "ceo": "Identificar vía Registro Mercantil / EPC Lead",
                            "riesgo": "ALTA PRIORIDAD - ACTIVO DE INFRAESTRUCTURA",
                            "movil": "Documento de Red / Terminal Financiera",
                            "email": "intel.130@maia-intelligence.io",
                            "fecha": f"Detectado: {fecha_limite} a Hoy",
                            "fuente": hit['href'],
                            "resumen": resumen_texto
                        })
        except Exception as e:
            print(f"Error en el motor: {e}")
            
        return results

scout_engine = ScoutCore()
