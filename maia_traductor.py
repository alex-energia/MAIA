# ==============================
# MAIA TRADUCTOR PRO v1
# ==============================

from googletrans import Translator

translator = Translator()

def traducir_texto(texto, idioma_destino="es"):
    """
    Traduce automáticamente cualquier idioma al idioma destino.
    Detecta idioma origen automáticamente.
    """

    try:
        resultado = translator.translate(texto, dest=idioma_destino)

        return {
            "texto_original": texto,
            "idioma_origen": resultado.src,
            "idioma_destino": idioma_destino,
            "traduccion": resultado.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }