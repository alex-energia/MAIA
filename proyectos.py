from flask import Blueprint, render_template, request, redirect
import sqlite3
import random

# =========================
# BLUEPRINT
# =========================

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


    acumulado = 0
    payback = None

    for i,f in enumerate(flujos):

        acumulado += f

        if acumulado > 0:

            payback = i
            break


    if van > 0:

        evaluacion = "Proyecto rentable"
        recomendacion = "Invertir"

    else:

        evaluacion = "Proyecto no rentable"
        recomendacion = "No invertir"


    capex_detallado = desglose_capex(capex)
    opex_detallado = desglose_opex(opex)


    valor_generado = generar_valor(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )


    indicadores_financieros = motor_financiero_avanzado(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )


    sensibilidad = analisis_sensibilidad(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )


    riesgo = simulacion_montecarlo(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )


    # NUEVO
    escenarios_financiacion = escenarios_apalancamiento(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )


    energia = motor_energia_maia(
        capex,
        opex,
        vida,
        tasa
    )


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
        opex_detallado=opex_detallado,
        valor_generado=valor_generado,
        indicadores_financieros=indicadores_financieros,
        sensibilidad=sensibilidad,
        riesgo=riesgo,
        escenarios_financiacion=escenarios_financiacion,
        energia=energia
    )


# ============================================================
# ESCENARIOS APALANCAMIENTO
# ============================================================

def escenarios_apalancamiento(capex, ingresos, opex, vida, tasa):

    escenarios = [

        {"nombre":"70% deuda / 30% equity","deuda":0.7},
        {"nombre":"80% deuda / 20% equity","deuda":0.8},
        {"nombre":"100% equity","deuda":0.0}

    ]

    resultados = []

    for e in escenarios:

        deuda = capex * e["deuda"]
        equity = capex - deuda

        flujo = ingresos - opex

        van = 0

        for i in range(1,vida+1):
            van += flujo/((1+tasa)**i)

        van -= capex

        roe = flujo/equity if equity != 0 else 0

        resultados.append({

            "escenario":e["nombre"],
            "deuda":round(deuda,2),
            "equity":round(equity,2),
            "van":round(van,2),
            "roe":round(roe,4)

        })

    return resultados


# ============================================================
# PRECIO MINIMO KWH
# ============================================================

def precio_minimo_kwh(capex, opex, produccion_kwh, vida, tasa):

    precio = 0.01

    while precio < 1:

        ingresos = produccion_kwh * precio
        flujo = ingresos - opex

        van = 0

        for i in range(1,vida+1):
            van += flujo/((1+tasa)**i)

        van -= capex

        if van >= 0:
            return round(precio,4)

        precio += 0.001

    return None


# ============================================================
# LCOE
# ============================================================

def calcular_lcoe(capex, opex, produccion_kwh, vida, tasa):

    costo_total = capex
    energia_total = 0

    for i in range(1,vida+1):

        costo_total += opex/((1+tasa)**i)
        energia_total += produccion_kwh/((1+tasa)**i)

    if energia_total == 0:
        return None

    return round(costo_total/energia_total,4)


# ============================================================
# MOTOR ENERGIA MAIA
# ============================================================

def motor_energia_maia(capex, opex, vida, tasa):

    produccion_anual_kwh = 1000000

    precio_minimo = precio_minimo_kwh(
        capex,
        opex,
        produccion_anual_kwh,
        vida,
        tasa
    )

    lcoe = calcular_lcoe(
        capex,
        opex,
        produccion_anual_kwh,
        vida,
        tasa
    )

    return {

        "produccion_anual_kwh":produccion_anual_kwh,
        "precio_minimo_kwh":precio_minimo,
        "lcoe":lcoe

    }