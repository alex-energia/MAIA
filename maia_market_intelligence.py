import requests
import datetime
import urllib.parse


# =========================
# PAISES OBJETIVO
# =========================

PAISES = [
    "colombia",
    "ecuador",
    "peru",
    "panama",
    "paraguay",
    "venezuela"
]


# =========================
# PALABRAS CLAVE
# =========================

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
# GLOBAL ENERGY SCANNER
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

                texto = query.lower()

                # -------------------------
                # CLASIFICACION ACTIVO
                # -------------------------

                tipo_activo = "energia"
                fase = "desarrollo"
                potencia = "1+ MW"
                tipo_oportunidad = "general"

                if "hydro" in texto or "hydropower" in texto:
                    tipo_activo = "hidroelectrica"

                if "smr" in texto or "nuclear" in texto:
                    tipo_activo = "nuclear_smr"

                if "sale" in texto or "for sale" in texto or "venta" in texto:
                    tipo_oportunidad = "activo_en_venta"

                if "investment" in texto or "investor" in texto:
                    tipo_oportunidad = "buscando_inversion"

                oportunidades.append({

                    "titulo": query,
                    "pais": pais,
                    "tipo_activo": tipo_activo,
                    "fase": fase,
                    "tipo_oportunidad": tipo_oportunidad,
                    "potencia_mw": potencia,
                    "empresa": "fuente web",
                    "contacto": f"https://duckduckgo.com/?q={query_encoded}",
                    "fecha": str(datetime.date.today())

                })

            except Exception:

                continue

    return oportunidades


# =========================
# MAIA DEAL INTELLIGENCE
# =========================

def detectar_activos_tempranos():

    oportunidades = buscar_oportunidades()

    deals = []

    for o in oportunidades:

        texto = o["titulo"].lower()

        prioridad = "normal"
        tipo_negocio = "exploracion"
        tipo_activo = o["tipo_activo"]

        # -------------------------
        # CLASIFICACION NEGOCIO
        # -------------------------

        if any(x in texto for x in ["sale", "for sale", "venta"]):

            prioridad = "alta"
            tipo_negocio = "adquisicion_proyecto"

        if any(x in texto for x in ["investment", "investor", "capital"]):

            prioridad = "media"
            tipo_negocio = "entrada_inversionista"

        if "partner" in texto:

            prioridad = "media"
            tipo_negocio = "busqueda_socio"

        if "smr" in texto or "nuclear" in texto:

            prioridad = "estrategica"
            tipo_negocio = "infraestructura_estrategica"

        # -------------------------
        # FILTRO FINAL
        # -------------------------

        if prioridad != "normal":

            o["prioridad"] = prioridad
            o["tipo_negocio"] = tipo_negocio
            o["tipo_activo"] = tipo_activo

            deals.append(o)

    return deals