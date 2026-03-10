import requests
import datetime

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


def buscar_oportunidades():

    oportunidades = []

    for pais in PAISES:

        for keyword in KEYWORDS:

            query = f"{keyword} {pais}"

            try:

                url = f"https://duckduckgo.com/?q={query}&format=json"

                r = requests.get(url, timeout=5)

                oportunidades.append({

                    "titulo": query,
                    "pais": pais,
                    "tecnologia": "energia",
                    "potencia_mw": "1+",
                    "empresa": "fuente web",
                    "contacto": url,
                    "fecha": str(datetime.date.today())

                })

            except:

                continue

    return oportunidades



def detectar_activos_tempranos():

    oportunidades = buscar_oportunidades()

    deals = []

    for o in oportunidades:

        texto = o["titulo"].lower()

        if any(x in texto for x in [

        "sale",
        "investment",
        "investor",
        "capital",
        "partner"

        ]):

            deals.append(o)

    return deals