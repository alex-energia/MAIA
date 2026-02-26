class AnalizadorEnergia:

    def analizar_proyecto(self, datos):

        tecnologia = datos.get("tecnologia", "generico")
        inversion = datos.get("inversion", 0)
        capacidad = datos.get("capacidad_mw", 0)
        precio = datos.get("precio_kwh", 0)
        factor = datos.get("factor_planta", 0)
        opex_anual = datos.get("opex_anual", 0)
        tasa_descuento = datos.get("tasa_descuento", 0.10)
        anos = datos.get("anos", 20)

        energia_anual_mwh = capacidad * 8760 * factor
        ingresos = energia_anual_mwh * 1000 * precio
        flujo_anual = ingresos - opex_anual

        flujos = [-inversion] + [flujo_anual] * anos

        van = self.calcular_van(flujos, tasa_descuento)
        tir = self.calcular_tir(flujos)

        return {
            "tecnologia": tecnologia,
            "energia_anual_mwh": energia_anual_mwh,
            "ingresos_anuales": ingresos,
            "flujo_anual": flujo_anual,
            "VAN": van,
            "TIR": tir
        }

    def calcular_van(self, flujos, tasa):
        van = 0
        for i, flujo in enumerate(flujos):
            van += flujo / ((1 + tasa) ** i)
        return van

    def calcular_tir(self, flujos, precision=1e-6, max_iter=1000):

        tasa = 0.1

        for _ in range(max_iter):
            van = 0
            derivada = 0

            for i, flujo in enumerate(flujos):
                van += flujo / ((1 + tasa) ** i)
                if i != 0:
                    derivada -= i * flujo / ((1 + tasa) ** (i + 1))

            if derivada == 0:
                return None

            nueva_tasa = tasa - van / derivada

            if abs(nueva_tasa - tasa) < precision:
                return nueva_tasa

            tasa = nueva_tasa

        return tasa

    def analisis_sensibilidad_precio(self, datos, variacion=0.2):

        precio_base = datos["precio_kwh"]

        escenarios = {
            "pesimista": precio_base * (1 - variacion),
            "base": precio_base,
            "optimista": precio_base * (1 + variacion)
        }

        resultados = {}

        for nombre, precio in escenarios.items():
            datos_mod = datos.copy()
            datos_mod["precio_kwh"] = precio
            resultado = self.analizar_proyecto(datos_mod)

            resultados[nombre] = {
                "precio_kwh": precio,
                "VAN": resultado["VAN"],
                "TIR": resultado["TIR"]
            }

        return resultados


    