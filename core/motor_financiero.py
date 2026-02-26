# ==========================================
# MOTOR FINANCIERO INSTITUCIONAL - MAIA
# CAPM Dinamico + WACC + Beta Ajustado
# Incluye Hidroelectrica
# ==========================================

class MotorFinanciero:

    def __init__(self):

        # ===============================
        # PARAMETROS DE MERCADO BASE
        # ===============================

        self.risk_free = 0.04          # 4%
        self.market_premium = 0.06     # 6%
        self.impuesto = 0.30           # 30%
        self.costo_deuda = 0.08        # 8%

        self.porcentaje_deuda = 0.70
        self.porcentaje_equity = 0.30

        # ===============================
        # BETAS SECTORIALES
        # ===============================

        self.beta_sector = {
            "solar": 1.10,
            "eolica": 1.05,
            "nuclear": 0.80,
            "geotermica": 0.90,
            "hidroelectrica": 0.85
        }

        # ===============================
        # PRIMA RIESGO PAIS
        # ===============================

        self.prima_riesgo_pais = {
            "colombia": 0.03,
            "mexico": 0.035,
            "brasil": 0.04,
            "chile": 0.025,
            "usa": 0.0
        }

    # ===================================
    # BETA AJUSTADO
    # ===================================

    def calcular_beta_ajustado(self, tecnologia, pais, riesgo_regulatorio):

        beta_base = self.beta_sector.get(tecnologia.lower(), 1.0)
        prima_pais = self.prima_riesgo_pais.get(pais.lower(), 0.02)

        beta_ajustado = beta_base + prima_pais + riesgo_regulatorio

        return beta_ajustado

    # ===================================
    # CAPM DINAMICO
    # ===================================

    def calcular_costo_equity(self, beta):

        return self.risk_free + beta * self.market_premium

    # ===================================
    # WACC DINAMICO
    # ===================================

    def calcular_wacc(self, costo_equity):

        rd_after_tax = self.costo_deuda * (1 - self.impuesto)

        wacc = (
            self.porcentaje_equity * costo_equity +
            self.porcentaje_deuda * rd_after_tax
        )

        return wacc

    # ===================================
    # VAN
    # ===================================

    def calcular_van(self, flujos, tasa):

        van = 0

        for i, flujo in enumerate(flujos):
            van += flujo / ((1 + tasa) ** i)

        return van

    # ===================================
    # TIR
    # ===================================

    def calcular_tir(self, flujos, precision=1e-6, max_iter=1000):

        tasa = 0.10

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