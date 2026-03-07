from flask import Blueprint, render_template, request, redirect, jsonify
import sqlite3
import random
import os
import pdfplumber
import pandas as pd
from docx import Document
from PIL import Image

# =========================
# BLUEPRINT
# =========================

proyectos_bp = Blueprint("proyectos", __name__)

DB = "maia.db"
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================
# CONEXION BASE DE DATOS
# =========================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# CREAR TABLA
# =========================

def init_db():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        capex_inicial REAL,
        opex_anual REAL,
        ingresos_anuales REAL,
        vida_util INTEGER,
        tasa_descuento REAL
    )
    """)

    conn.commit()
    conn.close()


# =========================
# DESGLOSE CAPEX
# =========================

def desglose_capex(capex):

    return [
        {"actividad":"Ingeniería","valor":round(capex*0.15,2)},
        {"actividad":"Equipos","valor":round(capex*0.40,2)},
        {"actividad":"Construcción","valor":round(capex*0.25,2)},
        {"actividad":"Permisos","valor":round(capex*0.10,2)},
        {"actividad":"Contingencia","valor":round(capex*0.10,2)}
    ]


# =========================
# DESGLOSE OPEX
# =========================

def desglose_opex(opex):

    return [
        {"actividad":"Operación","valor":round(opex*0.35,2)},
        {"actividad":"Mantenimiento","valor":round(opex*0.25,2)},
        {"actividad":"Administración","valor":round(opex*0.15,2)},
        {"actividad":"Logística","valor":round(opex*0.15,2)},
        {"actividad":"Regulación","valor":round(opex*0.10,2)}
    ]


# =========================
# MOTOR GENERACION VALOR
# =========================

def generar_valor(capex, ingresos, opex, vida, tasa):

    flujo_operativo = ingresos - opex

    valor_ingresos = ingresos * vida
    valor_costos = opex * vida

    eficiencia_capital = flujo_operativo / capex if capex != 0 else 0

    van = 0

    for i in range(1, vida+1):
        van += flujo_operativo / ((1+tasa)**i)

    van -= capex

    valor = [

        {"driver":"Ingresos operacionales totales","valor":round(valor_ingresos,2)},
        {"driver":"Costos operacionales totales","valor":round(valor_costos,2)},
        {"driver":"Flujo operativo anual","valor":round(flujo_operativo,2)},
        {"driver":"Eficiencia del capital","valor":round(eficiencia_capital,3)},
        {"driver":"Valor presente del proyecto","valor":round(van,2)}

    ]

    return valor


# =========================
# LISTA PROYECTOS
# =========================

@proyectos_bp.route("/proyectos")
def lista_proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT * FROM proyectos"
    ).fetchall()

    conn.close()

    return render_template(
        "proyectos.html",
        proyectos=proyectos
    )


# =========================
# CREAR PROYECTO
# =========================

@proyectos_bp.route("/proyectos/nuevo", methods=["GET","POST"])
def nuevo_proyecto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        capex = float(request.form["capex"])
        opex = float(request.form["opex"])
        ingresos = float(request.form["ingresos"])
        vida = int(request.form["vida"])
        tasa = float(request.form["tasa"])

        conn = get_db()

        conn.execute("""
        INSERT INTO proyectos
        (nombre,capex_inicial,opex_anual,ingresos_anuales,vida_util,tasa_descuento)
        VALUES (?,?,?,?,?,?)
        """,(nombre,capex,opex,ingresos,vida,tasa))

        conn.commit()
        conn.close()

        return redirect("/proyectos")

    return render_template("nuevo_proyecto.html")


# =========================
# DASHBOARD PROYECTO
# =========================

@proyectos_bp.route("/proyectos/<int:proyecto_id>")
def dashboard_proyecto(proyecto_id):

    conn = get_db()

    proyecto = conn.execute(
        "SELECT * FROM proyectos WHERE id=?",
        (proyecto_id,)
    ).fetchone()

    conn.close()

    if not proyecto:
        return "Proyecto no encontrado"

    capex = proyecto["capex_inicial"]
    opex = proyecto["opex_anual"]
    ingresos = proyecto["ingresos_anuales"]
    vida = proyecto["vida_util"]
    tasa = proyecto["tasa_descuento"]

    flujo_anual = ingresos - opex

    flujos = [-capex]

    for i in range(vida):
        flujos.append(flujo_anual)

    van = 0

    for i,f in enumerate(flujos):
        van += f / ((1+tasa)**i)

    return render_template(
        "proyecto_dashboard.html",
        proyecto=proyecto,
        flujo_anual=round(flujo_anual,2),
        van=round(van,2)
    )


# ============================================================
# CHAT MAIA SOBRE PROYECTO
# ============================================================

@proyectos_bp.route("/proyectos/<int:proyecto_id>/chat", methods=["POST"])
def chat_maia_proyecto(proyecto_id):

    pregunta = request.json.get("pregunta","").lower()

    conn = get_db()

    proyecto = conn.execute(
        "SELECT * FROM proyectos WHERE id=?",
        (proyecto_id,)
    ).fetchone()

    conn.close()

    if not proyecto:
        return jsonify({"respuesta":"Proyecto no encontrado"})

    capex = proyecto["capex_inicial"]
    opex = proyecto["opex_anual"]
    ingresos = proyecto["ingresos_anuales"]

    flujo = ingresos - opex

    if "capex" in pregunta:
        return jsonify({"respuesta":f"El CAPEX del proyecto es {capex}"})

    if "opex" in pregunta:
        return jsonify({"respuesta":f"El OPEX anual es {opex}"})

    if "flujo" in pregunta:
        return jsonify({"respuesta":f"El flujo anual es {flujo}"})

    if "rentable" in pregunta:

        if flujo > 0:
            return jsonify({"respuesta":"El proyecto genera flujo positivo"})
        else:
            return jsonify({"respuesta":"El proyecto genera flujo negativo"})

    return jsonify({"respuesta":"Puedo responder preguntas sobre CAPEX, OPEX, flujo y rentabilidad"})


# ============================================================
# SUBIR DOCUMENTOS
# ============================================================

@proyectos_bp.route("/proyectos/<int:proyecto_id>/upload", methods=["POST"])
def subir_documento(proyecto_id):

    archivo = request.files["file"]

    ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)

    archivo.save(ruta)

    return jsonify({"mensaje":"Archivo subido correctamente"})


# ============================================================
# ANALISIS DOCUMENTOS
# ============================================================

def analizar_documento(ruta):

    texto = ""

    if ruta.endswith(".pdf"):

        with pdfplumber.open(ruta) as pdf:

            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""

    elif ruta.endswith(".docx"):

        doc = Document(ruta)

        for p in doc.paragraphs:
            texto += p.text

    elif ruta.endswith(".xlsx"):

        df = pd.read_excel(ruta)

        texto += df.to_string()

    elif ruta.endswith(".jpg") or ruta.endswith(".png"):

        texto = "Imagen cargada correctamente"

    return texto[:5000]