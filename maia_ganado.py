import math

# ==============================
# PARÁMETROS POR RAZA
# ==============================

RAZAS = {
    "brahman": {
        "Wmax": 900,   # Peso adulto promedio kg
        "k": 0.06,     # Tasa crecimiento
        "t0": 24       # Punto inflexión meses
    },
    "angus": {
        "Wmax": 800,
        "k": 0.065,
        "t0": 22
    },
    "holstein": {
        "Wmax": 750,
        "k": 0.07,
        "t0": 20
    },
    "cebu": {
        "Wmax": 850,
        "k": 0.055,
        "t0": 26
    }
}

# ==============================
# FUNCIÓN CURVA LOGÍSTICA
# ==============================

def curva_crecimiento(edad_meses, Wmax, k, t0):
    return Wmax / (1 + math.exp(-k * (edad_meses - t0)))

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def estimar_peso(edad_meses, raza, condicion_corporal=3):
    
    raza = raza.lower()
    
    if raza not in RAZAS:
        return {
            "error": "Raza no soportada"
        }

    params = RAZAS[raza]

    peso_base = curva_crecimiento(
        edad_meses,
        params["Wmax"],
        params["k"],
        params["t0"]
    )

    # Ajuste por condición corporal (escala 1-5)
    ajuste = (condicion_corporal - 3) * 0.05
    factor_visual = 1 + ajuste

    peso_estimado = peso_base * factor_visual

    intervalo = peso_estimado * 0.12

    return {
        "peso_estimado": round(peso_estimado, 1),
        "intervalo_confianza": round(intervalo, 1),
        "rango_inferior": round(peso_estimado - intervalo, 1),
        "rango_superior": round(peso_estimado + intervalo, 1)
    }


# ==============================
# PRUEBA LOCAL
# ==============================

if __name__ == "__main__":
    resultado = estimar_peso(edad_meses=18, raza="brahman", condicion_corporal=3)
    print(resultado)