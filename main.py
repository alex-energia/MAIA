import flet as ft
import os
import datos_proyecto
def main(page: ft.Page):
    page.title = "MAIA"
    page.add(datos_proyecto.get_content() )
    page.update()
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080) )
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
