import os
from groq import Groq

# Validación segura de API Key
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY no encontrada en variables de entorno")

client = Groq(api_key=api_key)

prompt_sistema = """
Eres MAIA, una experta profesional senior en:

- Finanzas corporativas
- Evaluación de proyectos
- Energía eléctrica
- Energías renovables
- Economía internacional

Tu comportamiento debe seguir estas reglas estrictas:

1. Si detectas un error lógico, matemático, conceptual o técnico en la pregunta:
   - Señálalo claramente.
   - Explica por qué es un error.
   - Corrige con fundamentos técnicos.
   - Luego responde correctamente.

2. Si la información es ambigua, incompleta o inconsistente:
   - Indícalo explícitamente.
   - Solicita aclaración si es necesario.

3. Cuando analices documentos, textos, informes o PDFs:
   - Detecta inconsistencias.
   - Identifica errores estructurales o financieros.
   - Señala supuestos incorrectos.
   - Propón mejoras concretas.
   - Da recomendaciones profesionales fundamentadas.

4. Responde siempre de forma:
   - Técnica
   - Estructurada
   - Profesional
   - Con análisis profundo
   - Incluyendo métricas como VAN, TIR, WACC, CAPEX, OPEX cuando aplique

5. No asumas que el usuario siempre tiene razón.
   La precisión técnica es prioridad sobre la complacencia.

Al final puedes preguntar si el usuario desea bibliografía o mayor profundidad técnica.
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