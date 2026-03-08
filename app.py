from flask import Flask, render_template
from proyectos import proyectos_bp, init_db
import os

app = Flask(__name__)

# =========================
# INICIALIZAR BASE DE DATOS
# =========================

init_db()

# =========================
# REGISTRAR BLUEPRINT
# =========================

app.register_blueprint(proyectos_bp)

# =========================
# RUTA PRINCIPAL
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# EJECUTAR APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)