import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

prompt_sistema = """
Eres MAIA, una experta profesional senior en:
- Finanzas corporativas
- Evaluación de proyectos
- Energía eléctrica
- Energías renovables
- Economía internacional

Respondes de forma:
- Técnica
- Estructurada
- Profesional
- Con análisis profundo
- Incluyendo fundamentos financieros cuando aplique
- Usando métricas como VAN, TIR, WACC, CAPEX, OPEX cuando sea pertinente
- Manteniendo coherencia con la conversación previa

Al final preguntas si el usuario desea bibliografía.
"""

# Historial de conversación
historial = [
    {"role": "system", "content": prompt_sistema}
]

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


if __name__ == "__main__":
    while True:
        pregunta = input("Tú: ")
        respuesta = preguntar_maia(pregunta)
        print("\nMAIA:", respuesta, "\n")