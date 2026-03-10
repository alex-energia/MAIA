import requests
import datetime
import urllib.parse


PAISES = [
"colombia",
"ecuador",
"peru",
"panama",
"paraguay",
"venezuela"
]


KEYWORDS = [

"hydropower project for sale",
"small hydro project investment",
"hydropower plant seeking investors",
"small hydro power plant 1 mw investment",
"hydropower project latin america",
"energy infrastructure investment",
"smr nuclear project investment",
"small modular reactor project"

]


# =========================
# BUSCAR OPORTUNIDADES
# =========================

def buscar_oportunidades():

    oportunidades = []

    for pais in PAISES:

        for keyword in KEYWORDS:

            query = f"{keyword} {pais}"

            try:

                query_encoded = urllib.parse.quote(query)

                url = f"https://api.duckduckgo.com/?q={query_encoded}&format=json&no_redirect=1&no_html=1"

                r = requests.get(url, timeout=5)

                data = r.json()

                oportunidades.append({

                    "titulo": query,
                    "pais": pais,
                    "tecnologia": "energia",
                    "potencia_mw": "1+",
                    "empresa": "fuente web",
                    "contacto": f"https://duckduckgo.com/?q={query_encoded}",
                    "fecha": str(datetime.date.today())

                })

            except Exception:

                continue

    return oportunidades



# =========================
# DETECTAR ACTIVOS TEMPRANOS
# =========================

def detectar_activos_tempranos():

    oportunidades = buscar_oportunidades()

    deals = []

    for o in oportunidades:

        texto = o["titulo"].lower()

        prioridad = "normal"
        tipo_activo = "energia"


        # hidroeléctricas
        if any(x in texto for x in ["hydro", "hydropower", "small hydro"]):

            tipo_activo = "hidroelectrica"


        # nuclear SMR
        if any(x in texto for x in ["smr", "small modular reactor", "nuclear"]):

            tipo_activo = "nuclear_smr"
            prioridad = "estrategica"


        # activos en venta
        if any(x in texto for x in ["sale", "for sale", "venta"]):

            prioridad = "alta"


        # buscando inversionistas
        if any(x in texto for x in ["investment", "investor", "capital", "partner"]):

            if prioridad != "alta":
                prioridad = "media"


        if prioridad != "normal":

            o["prioridad"] = prioridad
            o["tipo_activo"] = tipo_activo

            deals.append(o)


    return deals