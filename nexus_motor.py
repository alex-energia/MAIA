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


# ==============================
# FLUJO DE CAJA
# ==============================

def calcular_flujo_caja(capex, ingresos, opex, horizonte=20):

    flujo = []

    flujo.append(-capex)

    for i in range(horizonte):

        flujo_anual = ingresos - opex

        flujo.append(flujo_anual)

    return flujo


# ==============================
# VAN
# ==============================

def calcular_van(flujo, tasa=0.10):

    van = 0

    for i, f in enumerate(flujo):

        van += f / ((1 + tasa) ** i)

    return van


# ==============================
# PAYBACK
# ==============================

def calcular_payback(flujo):

    acumulado = 0

    for i, f in enumerate(flujo):

        acumulado += f

        if acumulado >= 0:

            return i

    return None


# ==============================
# TIR (aproximada)
# ==============================

def calcular_tir(flujo, intentos=1000):

    tasa = 0.1

    for _ in range(intentos):

        van = 0
        derivada = 0

        for t, f in enumerate(flujo):

            van += f / (1 + tasa) ** t

            if t != 0:

                derivada -= t * f / (1 + tasa) ** (t + 1)

        if derivada == 0:

            return None

        nueva_tasa = tasa - van / derivada

        if abs(nueva_tasa - tasa) < 0.00001:

            return nueva_tasa

        tasa = nueva_tasa

    return tasa


# ==============================
# ANALISIS FINANCIERO COMPLETO
# ==============================

def analisis_financiero(sector, capacidad):

    datos = modelo_financiero(sector, capacidad)

    capex = datos["capex"]

    opex = datos["opex"]

    ingresos = datos["ingresos"]

    flujo = calcular_flujo_caja(capex, ingresos, opex)

    van = calcular_van(flujo)

    tir = calcular_tir(flujo)

    payback = calcular_payback(flujo)

    return {
        "capex": capex,
        "opex": opex,
        "ingresos": ingresos,
        "van": van,
        "tir": tir,
        "payback": payback
    }