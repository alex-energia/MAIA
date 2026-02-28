from flask import Flask, render_template, request, jsonify
from chat_maia import preguntar_maia

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pregunta = data.get("pregunta")
    
    respuesta = preguntar_maia(pregunta)
    
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)