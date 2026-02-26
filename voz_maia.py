import os
from TTS.api import TTS

# Cargar modelo XTTS v2
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

def hablar(texto):
    archivo = "respuesta_maia.wav"

    tts.tts_to_file(
        text=texto,
        language="es",
        speaker_wav="voz_latina.wav",
        file_path=archivo
    )

    os.startfile(archivo)

if __name__ == "__main__":
    print("Maia lista. Escribe y presiona Enter.")
    while True:
        texto = input("Tu: ")
        if texto.lower() in ["salir", "exit", "quit"]:
            break
        hablar(texto)