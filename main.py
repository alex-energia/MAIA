(
echo import flet as ft
echo import os
echo import datos_proyecto
echo def main(page: ft.Page^):
echo     page.title = "MAIA"
echo     page.add(datos_proyecto.get_content(^) ^)
echo     page.update(^)
echo if __name__ == "__main__":
echo     port = int(os.getenv("PORT", 8080^) ^)
echo     ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port^)
) > main.py
