# ==============================
# NEXUS MOTOR FINANCIERO
# ==============================

def calcular_capex(sector, capacidad):

    costos = {
        "Energia Solar": 900000,
        "Hidroelectrico": 2000000,
        "Eolico": 1500000,
        "Nuclear": 6000000,
        "Agricola": 2000,
        "Mineria": 50000,
        "Infraestructura": 3000000,
        "Inmobiliario": 1200
    }

    costo_unitario = costos.get(sector, 100000)

    return capacidad * costo_unitario


# ==============================
# OPEX
# ==============================

def calcular_opex(capex):

    return capex * 0.05


# ==============================
# INGRESOS ESTIMADOS
# ==============================

def calcular_ingresos(sector, capacidad):

    precios = {
        "Energia Solar": 70,
        "Hidroelectrico": 65,
        "Eolico": 75,
        "Nuclear": 90,
        "Agricola": 1200,
        "Mineria": 200,
        "Infraestructura": 150000,
        "Inmobiliario": 800
    }

    precio = precios.get(sector, 100)

    return capacidad * precio * 1000


# ==============================
# MODELO COMPLETO
# ==============================

def modelo_financiero(sector, capacidad):

    capex = calcular_capex(sector, capacidad)

    opex = calcular_opex(capex)

    ingresos = calcular_ingresos(sector, capacidad)

    return {
        "capex": capex,
        "opex": opex,
        "ingresos": ingresos
    }