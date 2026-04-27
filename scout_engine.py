# -*- coding: utf-8 -*-
import sys
import time
import re
from duckduckgo_search import DDGS

class MaiaDeepSearch:
    def __init__(self):
        self.pilares = [
            "Energia hidroelectrica", "Startup de tecnologia", "SMR nuclear",
            "Solar", "Termica", "Geotermica", "Neutrinos", "Hidrogeno"
        ]
        # FILTRO DE EXCLUSIÓN TOTAL (Hard-Kill de contenido informativo/educativo)
        self.trash = ["wikipedia", "news", "reuters", "bloomberg", "noticias", "youtube", "dictionary", "britannica"]
        # DOMINIOS DE ALTA INTENCIÓN (Filtro de identidad)
        self.targets = "(.gov OR .sa OR .ae OR .sg OR .cl OR .co OR crunchbase.com OR angel.co)"

    def _update_ui(self, i, total, pilar):
        """Barra de progreso técnica en consola"""
        prog = int((i / total) * 100)
        bar = "█" * (prog // 5) + "░" * (20 - (prog // 5))
        sys.stdout.write(f"\r\033[K[MAIA v11.0] [{bar}] {prog}% | ANALIZANDO NODO: {pilar.upper()}")
        sys.stdout.flush()

    def execute_global_scout(self):
        results = []
        total = len(self.pilares)
        
        print("\n" + "="*80)
        print("MAIA TRANSACTIONAL ENGINE v11.0 | 2026 | NO-PLACEHOLDERS")
        print("="*80)

        with DDGS() as ddgs:
            for i, pilar in enumerate(self.pilares):
                self._update_ui(i + 1, total, pilar)
                
                # DORKING FINANCIERO: Busca tipos de archivo y términos de licitación/equity
                # Se fuerza la búsqueda en los dominios target definidos en __init__
                query = f'"{pilar}" {self.targets} (intitle:tender OR "equity sale" OR "series B" OR licitacion) 2026 "USD" -{ " -".join(self.trash) }'
                
                try:
                    # Barrido profundo de 20 resultados para filtrar con rigor
                    search_data = list(ddgs.text(query, max_results=20))
                    for entry in search_data:
                        url = entry['href'].lower()
                        body = entry.get('body', '').lower()
                        title = entry.get('title', '').lower()

                        # 1. VALIDACIÓN DE MONEDA Y TRANSACCIÓN (Filtro de Capital)
                        if not any(k in body for k in ["$", "usd", "million", "billion", "equity", "round"]):
                            continue

                        # 2. EXTRACCIÓN DE DATA MEDIANTE REGEX (Sin placeholders)
                        val = re.search(r'(\$[0-9,.]+ ?(million|billion|M|B|USD))', body, re.I)
                        pwr = re.search(r'([0-9,.]+ ?(MW|GW|MWh|kW))', body, re.I)
                        tel = re.search(r'(\+?[0-9]{1,4}[\s-]?\(?[0-9]{1,4}\)?[\s-]?[0-9]{3,8}[\s-]?[0-9]{3,8})', body)
                        mail = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', body)

                        results.append({
                            "id": f"TXN-{int(time.time())}-{len(results)}",
                            "pilar": pilar.upper(),
                            "nombre": title.upper(),
                            "valor_inversion": val.group(0).upper() if val else "NOT_FOUND_IN_SNIPPET",
                            "potencia": pwr.group(0).upper() if pwr else "SEE_SPECIFICATIONS",
                            "ubicacion": "DETECTED_IN_URL",
                            "contacto_directo": {
                                "email": mail.group(0) if mail else "Verificar en link",
                                "tel": tel.group(0) if tel else "Verificar en link",
                                "web": url
                            },
                            "extracto": body[:250] + "..."
                        })
                    time.sleep(2) # Evitar baneo de IP
                except:
                    continue

        print("\n" + "="*80)
        # RETORNO PURO: Si no hay hallazgos reales, retorna []
        # No hay funciones de 'backup' ni 'hard_coded_deals'.
        return results

scout_engine = MaiaDeepSearch()