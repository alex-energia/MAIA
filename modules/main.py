from modules.energia import AnalizadorEnergia

analizador = AnalizadorEnergia()

datos = {
    "tecnologia": "solar",
    "inversion": 20000000,
    "capacidad_mw": 10,
    "precio_kwh": 0.08,
    "factor_planta": 0.25,
    "opex_anual": 500000,
    "tasa_descuento": 0.10,
    "anos": 20
}

resultado = analizador.analizar_proyecto(datos)

print("===== ANALISIS PROYECTO =====")
print("Tecnologia:", resultado["tecnologia"])
print("Energia anual (MWh):", round(resultado["energia_anual_mwh"], 2))
print("Ingresos anuales:", round(resultado["ingresos_anuales"], 2))
print("Flujo anual:", round(resultado["flujo_anual"], 2))
print("VAN:", round(resultado["VAN"], 2))
print("TIR:", round(resultado["TIR"], 4))

print("\n===== ANALISIS DE SENSIBILIDAD PRECIO =====")

sensibilidad = analizador.analisis_sensibilidad_precio(datos)

for escenario, valores in sensibilidad.items():
    print("\nEscenario:", escenario)
    print("Precio kWh:", round(valores["precio_kwh"], 4))
    print("VAN:", round(valores["VAN"], 2))
    print("TIR:", round(valores["TIR"], 4))