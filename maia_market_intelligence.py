import datetime

def buscar_oportunidades():

    hoy = datetime.date.today()

    oportunidades = [

        {
            "titulo": "PCH hidroeléctrica 6 MW buscando inversionistas",
            "pais": "Colombia",
            "tecnologia": "PCH",
            "potencia_mw": 6,
            "empresa": "Desarrollos Energéticos SAS",
            "contacto": "info@desarrollosenergeticos.com",
            "fecha": str(hoy)
        },

        {
            "titulo": "Proyecto hidroeléctrico 12 MW en venta",
            "pais": "Perú",
            "tecnologia": "PCH",
            "potencia_mw": 12,
            "empresa": "Andes Hydro",
            "contacto": "contact@andeshydro.com",
            "fecha": str(hoy)
        },

        {
            "titulo": "Proyecto SMR nuclear buscando socios estratégicos",
            "pais": "Canadá",
            "tecnologia": "SMR Nuclear",
            "potencia_mw": 300,
            "empresa": "North Energy",
            "contacto": "projects@northenergy.com",
            "fecha": str(hoy)
        },

        {
            "titulo": "Central hidroeléctrica 3 MW buscando capital",
            "pais": "Ecuador",
            "tecnologia": "PCH",
            "potencia_mw": 3,
            "empresa": "Energía Andina",
            "contacto": "info@energiaandina.ec",
            "fecha": str(hoy)
        }

    ]

    return oportunidades


def detectar_activos_tempranos():

    oportunidades = buscar_oportunidades()

    deals = []

    for o in oportunidades:

        texto = o["titulo"].lower()

        if any(x in texto for x in [

            "venta",
            "inversionistas",
            "capital",
            "socios",
            "investment"

        ]):

            deals.append(o)

    return deals