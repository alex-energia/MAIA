from flask import Flask, render_template, request, jsonify
from chat_maia import preguntar_maia
from maia_ganado import estimar_peso
from maia_plantas import diagnosticar_planta
from maia_traductor import traducir_texto

app = Flask(__name__)

# ==============================
# RUTA PRINCIPAL
# ==============================

@app.route("/")
def home():
    return render_template("index.html")

# ==============================
# CHAT NORMAL
# ==============================

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pregunta = data.get("pregunta")
    respuesta = preguntar_maia(pregunta)
    return jsonify({"respuesta": respuesta})

# ==============================
# MAIA GANADO
# ==============================

@app.route("/calcular_ganado", methods=["POST"])
def calcular_ganado():
    data = request.get_json()
    edad = data.get("edad")
    raza = data.get("raza")

    resultado = estimar_peso(
        edad_meses=edad,
        raza=raza
    )

    return jsonify(resultado)

# ==============================
# MAIA PLANTAS
# ==============================

@app.route("/diagnostico_plantas", methods=["POST"])
def diagnostico_plantas():
    resultado = diagnosticar_planta()
    return jsonify(resultado)

# ==============================
# MAIA TRADUCTOR
# ==============================

@app.route("/traducir", methods=["POST"])
def traducir():
    data = request.get_json()
    texto = data.get("texto")
    idioma_destino = data.get("idioma_destino")

    resultado = traducir_texto(texto, idioma_destino)
    return jsonify(resultado)

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)