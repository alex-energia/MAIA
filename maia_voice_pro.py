import os
import whisper
import torch
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from groq import Groq
from TTS.api import TTS

# ===== CONFIG =====
SAMPLE_RATE = 16000
DURATION = 5  # segundos de grabación por pregunta

# ===== MODELOS =====
print("Cargando Whisper...")
modelo_whisper = whisper.load_model("base")

print("Cargando modelo de voz...")
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC", progress_bar=False)

print("Conectando MAIA...")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

prompt_sistema = """
Eres MAIA, experta senior en finanzas, energía y evaluación de proyectos.
Respondes de forma estructurada, técnica y profesional.
Mantienes coherencia con la conversación previa.
"""

historial = [{"role": "system", "content": prompt_sistema}]

# ===== FUNCIONES =====

def grabar_audio():
    print("Habla ahora...")
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    wav.write("input.wav", SAMPLE_RATE, audio)
    print("Procesando audio...")

def transcribir():
    resultado = modelo_whisper.transcribe("input.wav", language="es")
    return resultado["text"]

def preguntar_maia(pregunta):
    historial.append({"role": "user", "content": pregunta})

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=historial,
        temperature=0.3
    )

    contenido = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": contenido})
    return contenido

def hablar(texto):
    tts.tts_to_file(text=texto, file_path="respuesta.wav")
    os.system("start respuesta.wav")

# ===== LOOP PRINCIPAL =====

print("\nMAIA Voice Pro iniciada.\n")

while True:
    grabar_audio()
    pregunta = transcribir()
    print("Tú:", pregunta)

    if pregunta.strip() == "":
        print("No detecté voz.")
        continue

    respuesta = preguntar_maia(pregunta)
    print("\nMAIA:", respuesta)

    hablar(respuesta)