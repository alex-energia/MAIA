(
echo import flet as ft
echo def get_content(^):
echo     DATOS = {
echo         "1. INFO BASE": {"Construcción": "01-may-25", "Venta kWh": "$ 323,72", "Financiación": "90%", "Periodo": "25 Años", "MW RTB": "$ 75.000", "Ke": "12,00%", "Factor g": "3,00%", "Min Serv": "1,30"},
echo         "2. INDICADORES ECON": {"WACC Nom": "12,33%", "WACC Real": "9,06%", "TIR Proy": "17,30%", "TIR Inv": "15,73%", "VPN Proy": "$ 24.380 MM", "VPN Inv": "$ 18.064 MM", "B/C": "1,62", "Payback": "9,35 Años"},
echo         "3. RESULTADOS PROY": {"Energía": "45.622 GWh", "Ingresos": "$ 653.952 MM", "EBITDA": "$ 585.400 MM", "CO2": "26.363 Ton", "ROA": "28,15%", "ROE": "54,12%", "Margen": "29,48%", "Caja 25a": "$ 98.719 MM"},
echo         "4. VIABILIDAD": {"Beneficio": "OK", "Flujo Mín": "CUMPLE", "EVA": "POSITIVO", "Salud": "VIABLE", "TIR vs WACC": "CUMPLE", "TIR vs Ke": "CUMPLE", "Sostenibilidad": "ALTA", "Riesgo": "BAJO"},
echo         "5. CRISIS": {"Endeudamiento": "0%", "Carga Fin": "0%", "Cobertura Int": "1,23", "DSCR": "1,67", "Margen Seg": "45%", "Equilibrio": "$ 8.450 MM", "Liquidez": "ALTA", "Solvencia": "OK"},
echo         "6. CAPEX/OPEX": {"CAPEX Total": "$ 90.389 MM", "OPEX Anual": "$ 649 MM", "Equity": "$ 17.472 MM", "Deuda Snr": "$ 72.917 MM", "Costos Adm": "$ 120 MM", "Mantenim": "$ 300 MM", "Seguros": "$ 80 MM", "Otros": "$ 149 MM"},
echo         "7. ESTRUC. DEUDA": {"Ratio D/A": "31,93%", "Kd (1-t)": "7,11%", "Activos": "$ 209.225 MM", "Deuda (D)": "$ 66.819 MM", "Equity (E)": "$ 142.405 MM", "Apalanc": "0,47", "WACC Calc": "12,33%", "Tasa": "11,50%"},
echo         "8. VALORACIÓN": {"FCD": "$ 138.910 MM", "DDM": "$ 118.954 MM", "FCFE": "$ 142.405 MM", "FCFF": "$ 140.226 MM", "Valor Res": "$ 45.000 MM", "Valor Libros": "$ 90.000 MM", "Multiplo": "8.5x", "Per": "12.4"},
echo         "9. BANCARIO": {"DTF": "8,50%", "Spread": "3,00%", "Tasa Fin": "11,50%", "Plazo": "14 Años", "Gracia": "2 Años", "Amortiz": "Francesa", "Póliza": "CUMPLE", "Garantía": "OK"},
echo         "10. MACRO": {"TRM USD": "$ 3.900", "TRM EUR": "$ 4.250", "IPC Est": "4,30%", "Riesgo País": "3,25%", "PIB Est": "2.5%", "Deuda/PIB": "52%", "Tasa Banrep": "10.0%", "Calif": "BB+"}
echo     }
echo     grid = ft.ResponsiveRow(spacing=20, run_spacing=20^)
echo     for tit, items in DATOS.items(^):
echo         rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(k, size=10, color="#B0BEC5"^)^), ft.DataCell(ft.Text(v, weight="bold", color="#66BB6A", size=10^)^)]) for k, v in items.items(^)]
echo         grid.controls.append(ft.Container(content=ft.Column([ft.Text(tit, weight="bold", color="#42A5F5", size=12^), ft.DataTable(columns=[ft.DataColumn(ft.Text(""^)^), ft.DataColumn(ft.Text(""^)^)], rows=rows, heading_row_height=0, data_row_max_height=28^)]), bgcolor="#1A1A1A", padding=15, border_radius=10, col={"sm": 12, "md": 6, "lg": 3}^)^)
echo     return ft.Column([grid], scroll=ft.ScrollMode.ADAPTIVE, expand=True^)
) > datos_proyecto.py