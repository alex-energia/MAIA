import requests
import datetime


PAISES_OBJETIVO = [
"colombia",
"ecuador",
"peru",
"panama",
"paraguay",
"venezuela"
]


KEYWORDS = [
"small hydro",
"hydropower project",
"pch hydro",
"hydropower investment",
"hydropower for sale",
"smr nuclear project",
"energy project investment"
]


def buscar_oportunidades():

    oportunidades = []

    for pais in PAISES_OBJETIVO:

        for k in KEYWORDS:

            query = f"{k} {pais}"

            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=5&apiKey=demo"

            try:

                r = requests.get(url,timeout=5)

                data = r.json()

                for art in data.get("articles",[]):

                    oportunidades.append({

                        "titulo": art["title"],
                        "pais": pais,
                        "tecnologia": "energia",
                        "potencia_mw": "N/D",
                        "empresa": art["source"]["name"],
                        "contacto": art["url"],
                        "fecha": art["publishedAt"]

                    })

            except:
                pass


    return oportunidades



def detectar_activos_tempranos():

    oportunidades = buscar_oportunidades()

    deals = []

    for o in oportunidades:

        texto = o["titulo"].lower()

        if any(x in texto for x in [

        "for sale",
        "investment",
        "seeking investors",
        "capital",
        "partnership"

        ]):

            deals.append(o)


    return deals