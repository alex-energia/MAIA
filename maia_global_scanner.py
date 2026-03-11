import requests
import datetime
import urllib.parse

# =========================
# REGIONES
# =========================

REGIONES = [
"latin america",
"north america",
"europe",
"asia",
"africa",
"middle east"
]

# =========================
# TIPOS DE NEGOCIO
# =========================

KEYWORDS = [

"hydropower project for sale",
"hydropower project partial sale",
"hydropower project investment opportunity",
"energy project equity sale",
"energy project seeking investor",

"small modular reactor project",
"SMR nuclear project investment",
"nuclear energy project partner",

"renewable energy project for sale",
"energy infrastructure investment",

"PPP energy project",
"energy project concession"

]

# =========================
# GLOBAL SCANNER
# =========================

def escanear_mercado_global():

    resultados = []

    for region in REGIONES:

        for keyword in KEYWORDS:

            query = f"{keyword} {region}"

            try:

                query_encoded = urllib.parse.quote(query)

                url = f"https://api.duckduckgo.com/?q={query_encoded}&format=json"

                r = requests.get(url, timeout=5)

                texto = query.lower()

                tipo_activo = "energia"

                if "hydro" in texto:
                    tipo_activo = "hidroelectrica"

                if "smr" in texto or "nuclear" in texto:
                    tipo_activo = "nuclear_smr"

                tipo_negocio = "general"

                if "sale" in texto:
                    tipo_negocio = "venta_total"

                if "partial" in texto:
                    tipo_negocio = "venta_parcial"

                if "investment" in texto:
                    tipo_negocio = "entrada_inversionista"

                if "partner" in texto:
                    tipo_negocio = "busqueda_socio"

                resultados.append({

                    "titulo": query,
                    "region": region,
                    "tipo_activo": tipo_activo,
                    "tipo_negocio": tipo_negocio,
                    "potencia": "1+ MW",
                    "fecha": str(datetime.date.today()),
                    "fuente": f"https://duckduckgo.com/?q={query_encoded}"

                })

            except:

                continue

    return resultados