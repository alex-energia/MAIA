# -*- coding: utf-8 -*-
import sys
import time
import re
from duckduckgo_search import DDGS

class MaiaTransactionalEngine:
    def __init__(self):
        self.pilares = [
            "Energia hidroelectrica", "Startup de tecnologia", "SMR nuclear",
            "Solar", "Termica", "Geotermica", "Neutrinos", "Hidrogeno"
        ]
        self.whitelist_tlds = [".gov", ".io", ".co", ".sa", ".ae", ".org", ".com"]
        self.hard_kill = ["wikipedia", "reuters", "bloomberg", "noticias", "news", "youtube", "dictionary"]
        self.business_keys = ["tender", "equity", "investment", "shares", "licitacion", "round", "funding"]
        
    def _progress(self, current, total, pilar):
        percent = (current / total) * 100
        bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
        sys.stdout.write(f"\r\033[K[SCANNING v10.0] [{bar}] {int(percent)}% | PILAR: {pilar.upper()}")
        sys.stdout.flush()

    def _regex_extract(self, pattern, text):
        match = re.search(pattern, text, re.I)
        return match.group(0).strip() if match else None

    def execute_transactional_scout(self):
        final_leads = []
        total = len(self.pilares)

        with DDGS() as ddgs:
            for idx, pilar in enumerate(self.pilares):
                self._progress(idx + 1, total, pilar)
                
                # DORKING FINANCIERO: Filtro por tipo de archivo y parámetros de URL transaccional
                dork = f'"{pilar}" (filetype:pdf OR filetype:doc OR "index of") (intitle:tender OR intitle:prospectus OR "investment opportunity") "2026" "USD"'
                
                try:
                    query_results = list(ddgs.text(dork, max_results=15))
                    for entry in query_results:
                        url = entry['href'].lower()
                        body = entry.get('body', '').lower()
                        title = entry.get('title', '').lower()

                        # 1. HARD KILL (Anti-Wiki/News)
                        if any(term in url for term in self.hard_kill):
                            continue

                        # 2. FILTRO DE IDENTIDAD Y DOMINIO
                        valid_domain = any(url.endswith(tld) or f"{tld}/" in url for tld in self.whitelist_tlds)
                        if not valid_domain:
                            continue

                        if ".com" in url or ".org" in url:
                            if not any(k in (body + title) for k in self.business_keys):
                                continue

                        # 3. EXTRACCIÓN DE DATA CRUDA (REGEX)
                        amount = self._regex_extract(r'(\$[0-9,.]+ ?(million|billion|M|B|USD))', body)
                        power = self._regex_extract(r'([0-9,.]+ ?(MW|GW|MWh|kW|GWh))', body)
                        phone = self._regex_extract(r'(\+?[0-9]{1,4}[\s-]?\(?[0-9]{1,4}\)?[\s-]?[0-9]{3,8}[\s-]?[0-9]{3,8})', body)
                        email = self._regex_extract(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', body)

                        if amount or power or email:
                            final_leads.append({
                                "id": f"TXN-{int(time.time())}-{len(final_leads)}",
                                "pilar": pilar.upper(),
                                "entidad": entry['title'].upper(),
                                "valor_usd": amount if amount else "UNDER_AUDIT",
                                "capacidad": power if power else "TECHNICAL_SPECS_IN_FILE",
                                "geolocalizacion": "VERIFY_BY_IP_NODE",
                                "contacto": {
                                    "mail": email if email else "CONTACT_REQUIRED",
                                    "tel": phone if phone else "OFFICE_EXT_PENDING",
                                    "source": url
                                },
                                "metadata": body[:250]
                            })
                    time.sleep(1.8)
                except:
                    continue

        sys.stdout.write("\n[SCAN COMPLETE]\n")
        return final_leads if final_leads else None

# Integración directa
scout_engine = MaiaTransactionalEngine()