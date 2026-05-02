(
echo import flet as ft
echo import os
echo import time
echo import datos_proyecto
echo def main(page: ft.Page^):
echo     page.title = "SISTEMA MAIA"
echo     page.theme_mode = ft.ThemeMode.DARK
echo     # Forzamos scroll para que se vea todo el modelo
echo     page.scroll = ft.ScrollMode.ADAPTIVE
echo     page.add(datos_proyecto.get_content(^) ^)
echo     page.update(^)
echo if __name__ == "__main__":
echo     # Render asigna el puerto en la variable PORT
echo     port_env = os.getenv("PORT", "8080"^)
echo     print(f"Iniciando MAIA en puerto: {port_env}"^)
echo     # El modo WEB_BROWSER es el unico que Render reconoce como Web Service
echo     ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(port_env^) ^)
) > main.py