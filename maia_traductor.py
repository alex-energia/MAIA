from deep_translator import GoogleTranslator

def traducir_texto(texto, idioma_destino="es"):
    try:
        traduccion = GoogleTranslator(source="auto", target=idioma_destino).translate(texto)

        return {
            "texto_original": texto,
            "idioma_destino": idioma_destino,
            "traduccion": traduccion
        }

    except Exception as e:
        return {
            "error": str(e)
        }