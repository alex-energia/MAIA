from flask import Blueprint, render_template, request, redirect
import sqlite3

# =========================
# IMPORTAR DESGLOSE COSTOS
# =========================
from costos_detallados import desglose_capex, desglose_opex

proyectos_bp = Blueprint("proyectos", __name__)

DB = "maia.db"


# =========================
# CONEXION BASE DE DATOS
# =========================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# CREAR TABLA SI NO EXISTE
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
# LISTA DE PROYECTOS
# =========================

@proyectos_bp.route("/proyectos")
def lista_proyectos():

    conn = get_db()
    proyectos = conn.execute("SELECT * FROM proyectos").fetchall()
    conn.close()

    return render_template("proyectos.html", proyectos=proyectos)


# =========================
# CREAR PROYECTO
# =========================

@proyectos_bp.route("/proyectos/nuevo", methods=["GET","POST"])
def nuevo_proyecto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        capex = float(request.form["capex"])
        opex = float(request.form["opex"])
        ingresos = float(request.form["ingresos"]
)
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


    # =========================
    # CALCULO FLUJOS
    # =========================

    flujos = [-capex]

    for i in range(vida):
        flujos.append(flujo_anual)


    # =========================
    # VAN
    # =========================

    van = 0

    for i,f in enumerate(flujos):
        van += f / ((1+tasa)**i)


    # =========================
    # TIR (aproximacion simple)
    # =========================

    tir = None

    try:

        r = 0.1

        for i in range(100):

            van_temp = 0
            dvan = 0

            for t,f in enumerate(flujos):

                van_temp += f / ((1+r)**t)

                if t > 0:
                    dvan += -t*f/((1+r)**(t+1))

            r = r - van_temp/dvan

        tir = r

    except:
        tir = None


    # =========================
    # PAYBACK
    # =========================

    acumulado = 0
    payback = None

    for i,f in enumerate(flujos):

        acumulado += f

        if acumulado > 0:
            payback = i
            break


    # =========================
    # EVALUACION
    # =========================

    if van > 0:
        evaluacion = "Proyecto rentable"
        recomendacion = "Invertir"
    else:
        evaluacion = "Proyecto no rentable"
        recomendacion = "No invertir"


    # =========================
    # DESGLOSE COSTOS
    # =========================

    capex_detallado = desglose_capex(capex)
    opex_detallado = desglose_opex(opex)


    # =========================
    # RENDER DASHBOARD
    # =========================

    return render_template(
        "proyecto_dashboard.html",
        proyecto=proyecto,
        flujo_anual=round(flujo_anual,2),
        van=round(van,2),
        tir=round(tir,4) if tir else None,
        payback=payback,
        evaluacion=evaluacion,
        recomendacion=recomendacion,
        flujos=flujos,
        capex_detallado=capex_detallado,
        opex_detallado=opex_detallado
    )