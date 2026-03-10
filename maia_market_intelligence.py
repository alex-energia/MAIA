import requests
import datetime

OPORTUNIDADES = []

PAISES_OBJETIVO = [
    "Colombia",
    "Ecuador",
    "Peru",
    "Panama",
    "Paraguay",
    "Venezuela",
    "Chile",
    "Brasil",
    "Argentina",
    "Mexico"
]

TECNOLOGIAS = [
    "PCH",
    "small hydro",
    "hydropower",
    "solar project",
    "wind farm",
    "battery storage",
    "nuclear project",
    "SMR reactor"
]

def buscar_oportunidades():

    resultados = []

    fecha = datetime.date.today()

    for pais in PAISES_OBJETIVO:
        for tecnologia in TECNOLOGIAS:

            query = f"{tecnologia} investment opportunity {pais}"

            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=5&apiKey=demo"

            try:

                r = requests.get(url)
                data = r.json()

                if "articles" in data:

                    for art in data["articles"]:

                        oportunidad = {
                            "titulo": art["title"],
                            "fuente": art["source"]["name"],
                            "pais": pais,
                            "tecnologia": tecnologia,
                            "fecha": art["publishedAt"],
                            "url": art["url"]
                        }

                        resultados.append(oportunidad)

            except:
                pass

    return resultados


def detectar_activos_tempranos():

    oportunidades = buscar_oportunidades()

    activos_tempranos = []

    for o in oportunidades:

        texto = o["titulo"].lower()

        if any(x in texto for x in [
            "seeking investors",
            "investment opportunity",
            "project financing",
            "project development"
        ]):

            activos_tempranos.append(o)

    return activos_tempranos