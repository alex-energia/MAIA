def generar_valor(capex, ingresos, opex, vida, tasa):

    flujo_operativo = ingresos - opex

    valor_ingresos = ingresos * vida
    valor_costos = opex * vida

    eficiencia_capital = flujo_operativo / capex if capex != 0 else 0


    # VAN simplificado
    van = 0

    for i in range(1, vida+1):
        van += flujo_operativo / ((1+tasa)**i)

    van -= capex


    valor = [

        {
        "driver":"Ingresos operacionales totales",
        "valor":round(valor_ingresos,2)
        },

        {
        "driver":"Costos operacionales totales",
        "valor":round(valor_costos,2)
        },

        {
        "driver":"Flujo operativo anual",
        "valor":round(flujo_operativo,2)
        },

        {
        "driver":"Eficiencia del capital",
        "valor":round(eficiencia_capital,3)
        },

        {
        "driver":"Valor presente del proyecto",
        "valor":round(van,2)
        }

    ]

    return valor