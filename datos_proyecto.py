(
echo import flet as ft
echo def get_content(^):
echo     DATOS = {
echo         "1. INFO BASE": {"Venta kWh": "$ 323,72", "Financiación": "90%", "Plazo": "25 Años"},
echo         "2. INDICADORES": {"WACC Nom": "12,33%", "TIR Proy": "17,30%", "VPN": "$ 24.380 MM"},
echo         "3. RESULTADOS": {"EBITDA": "$ 585.400 MM", "ROE": "54,12%", "ROA": "28,15%"},
echo         "4. VIABILIDAD": {"EVA": "POSITIVO", "Salud": "VIABLE", "Riesgo": "BAJO"},
echo         "5. CRISIS": {"DSCR": "1,67", "Cobertura": "1,23", "Margen": "45%"},
echo         "6. CAPEX/OPEX": {"CAPEX": "$ 90.389 MM", "OPEX": "$ 649 MM"},
echo         "7. DEUDA": {"Ratio D/A": "31,93%", "Kd": "7,11%", "Apalanc": "0,47"},
echo         "8. VALORACIÓN": {"FCD": "$ 138.910 MM", "FCFE": "$ 142.405 MM"},
echo         "9. BANCARIO": {"DTF": "8,50%", "Tasa Fin": "11,50%", "Gracia": "2 Años"},
echo         "10. MACRO": {"TRM USD": "$ 3.900", "IPC": "4,30%", "Riesgo Pais": "3,25%"}
echo     }
echo     grid = ft.ResponsiveRow(spacing=20, run_spacing=20^)
echo     for tit, items in DATOS.items(^):
echo         rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(k, size=10^)^), ft.DataCell(ft.Text(v, weight="bold", color="green", size=10^)^)]) for k, v in items.items(^)]
echo         grid.controls.append(ft.Container(content=ft.Column([ft.Text(tit, weight="bold", color="blue", size=12^), ft.DataTable(columns=[ft.DataColumn(ft.Text(""^)^), ft.DataColumn(ft.Text(""^)^)], rows=rows, heading_row_height=0^)]), bgcolor="#1A1A1A", padding=15, border_radius=10, col={"sm": 12, "md": 6, "lg": 3}^)^)
echo     return ft.Column([grid], scroll=ft.ScrollMode.ADAPTIVE, expand=True^)
) > datos_proyecto.py