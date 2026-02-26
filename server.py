from flask import Flask, request, jsonify
from core.evaluador_integral import EvaluadorIntegral
from chat_maia import preguntar_maia
import os

app = Flask(__name__)
evaluador = EvaluadorIntegral()

# ===============================
# INTERFAZ PRINCIPAL (Evaluador)
# ===============================
@app.route("/")
def home():
    return """
    <h1>MAIA - Evaluación Integral</h1>
    <form method="post" action="/maia">
        <label>Tecnología:</label><br>
        <input type="text" name="tecnologia"><br><br>

        <label>Capacidad (MW):</label><br>
        <input type="number" name="capacidad"><br><br>

        <label>País:</label><br>
        <input type="text" name="pais"><br><br>

        <label>Riesgo:</label><br>
        <input type="number" step="0.01" name="riesgo"><br><br>

        <button type="submit">Evaluar</button>
    </form>

    <br><br>
    <a href="/chat">Ir al Chat Inteligente MAIA</a>
    """

# ===============================
# PROCESAMIENTO EVALUADOR
# ===============================
@app.route("/maia", methods=["POST"])
def maia():
    if request.is_json:
        data = request.get_json()
        tecnologia = data.get("tecnologia")
        capacidad = data.get("capacidad")
        pais = data.get("pais")
        riesgo = data.get("riesgo")
    else:
        tecnologia = request.form.get("tecnologia")
        capacidad = request.form.get("capacidad")
        pais = request.form.get("pais")
        riesgo = request.form.get("riesgo")

    try:
        riesgo = float(riesgo)
    except (TypeError, ValueError):
        return "Error: riesgo inválido."

    resultado = evaluador.evaluar(tecnologia, capacidad, pais, riesgo)

    resultado_html = "<h2>Resultado Evaluación</h2><ul>"
    for clave, valor in resultado.items():
        resultado_html += f"<li><strong>{clave}:</strong> {valor}</li>"
    resultado_html += "</ul><br><a href='/'>Volver</a>"

    return resultado_html


# ===============================
# CHAT INTELIGENTE MAIA (SIN VOZ)
# ===============================
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return """
        <h2>Chat con MAIA</h2>
        <form method="post">
            <label>Escribe tu pregunta:</label><br><br>
            <textarea name="pregunta" rows="6" cols="70"></textarea><br><br>
            <button type="submit">Preguntar</button>
        </form>
        <br><a href="/">Volver</a>
        """

    if request.is_json:
        data = request.get_json()
        pregunta = data.get("pregunta")
    else:
        pregunta = request.form.get("pregunta")

    if not pregunta:
        return "No se recibió ninguna pregunta."

    respuesta = preguntar_maia(pregunta)

    return f"""
    <h2>Respuesta MAIA</h2>
    <div style='white-space: pre-wrap; font-family: Arial;'>
        {respuesta}
    </div>
    <br><br>
    <a href="/chat">Hacer otra pregunta</a>
    <br><a href="/">Volver</a>
    """


# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)