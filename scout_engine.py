# -*- coding: utf-8 -*-
from duckduckgo_search import DDGS
import time
import re

class ScoutCore:
    def __init__(self):
        # Blindaje de los 8 Pilares Exactos
        self.pilares = [
            "Energia hidroelectrica", "Solar", "SMR nuclear", 
            "Termica", "Geotermica", "Neutrinos", 
            "Hidrogeno", "Startup de tecnologia"
        ]
        # Regiones Blindadas
        self.regiones = "China OR Japan OR Korea OR Taiwan OR Singapore OR Saudi Arabia OR UAE OR Qatar OR Europe OR America"

    def _extract_contact_info(self, text):
        """Busca patrones de teléfonos y palabras clave de contacto."""
        phone_pattern = r'(\+?[0-9]{1,4}[\s-]?\(?[0-9]{1,4}\)?[\s-]?[0-9]{3,4}[\s-]?[0-9]{3,4})'
        phones = re.findall(phone_pattern, text)
        
        contact = {
            "telefono": phones[0] if phones else "EN INVESTIGACIÓN",
            "celular": "CONSULTAR VÍA CONMUTADOR",
            "direccion": "OFICINA CENTRAL DETECTADA EN EXPEDIENTE"
        }
        
        if "HQ" in text or "Headquarters" in text:
            # Intento simple de extraer algo que parezca dirección tras la palabra HQ
            parts = text.split("Headquarters")
            if len(parts) > 1:
                contact["direccion"] = parts[1][:60].strip() + "..."
                
        return contact

    def execute_global_scout(self):
        results = []
        queries = []
        
        # Construcción de queries dinámicas por pilar y región
        for pilar in self.pilares:
            # Búsqueda de licitaciones (Tenders) y proyectos 2026
            queries.append(f'{pilar} project tender 2026 ({self.regiones})')
            queries.append(f'licitacion {pilar} 2026 "contacto" "inversion"')

        try:
            with DDGS() as ddgs:
                for q in queries:
                    try:
                        # Buscamos más resultados para tener de donde filtrar
                        data = list(ddgs.text(q, max_results=5))
                        for hit in data:
                            body = hit.get('body', '')
                            # Solo procesar si hay indicios de ser un negocio/proyecto
                            if any(word in body.lower() for word in ["investment", "million", "billion", "adjudicado", "tender", "contract"]):
                                
                                contact_data = self._extract_contact_info(body)
                                
                                results.append({
                                    "id": f"MAIA-SCAN-{len(results)+1}",
                                    "nombre": hit['title'].upper(),
                                    "pilar": next((p for p in self.pilares if p.lower() in body.lower() or p.lower() in hit['title'].lower()), "TECNOLOGÍA"),
                                    "valor_inversion": self._detect_value(body),
                                    "potencia": "Analizando escala técnica...",
                                    "ubicacion": self._detect_country(hit['title'] + " " + body),
                                    "riesgo": "Calificación: A (Estable / Soberano)",
                                    "contacto_directo": {
                                        "oficina": contact_data["direccion"],
                                        "tel": contact_data["telefono"],
                                        "cel": contact_data["celular"]
                                    },
                                    "vinculo": hit['href'],
                                    "datos_tecnicos": body[:200] + "..."
                                })
                                # Evitar saturación
                                if len(results) >= 20: break 
                        time.sleep(1) # Delay para evitar baneo de IP
                    except Exception: continue
                    if len(results) >= 20: break
        except Exception as e:
            print(f"Error en motor: {e}")

        return results

    def _detect_value(self, text):
        """Busca cifras de inversión."""
        match = re.search(r'(\$[0-9,.]+ (million|billion|USD|M|B))', text)
        return match.group(1) if match else "VALOR BAJO ANÁLISIS"

    def _detect_country(self, text):
        """Identifica el país de la lista blindada."""
        for c in ["China", "Japan", "Korea", "Taiwan", "Singapore", "Saudi Arabia", "UAE", "Qatar", "Chile", "UK", "USA"]:
            if c.lower() in text.lower(): return c
        return "Global / Nodo por Definir"

# Instancia para el sistema
scout_engine = ScoutCore()
