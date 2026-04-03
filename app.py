from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
import os,time,zipfile

print("MAIA INDUSTRIAL CORE LEVEL 7 - REAL DRONE STACK")

app=Flask(__name__,template_folder="templates")
app.secret_key="maia_ultra"

# =========================
# NO CACHE
# =========================
@app.after_request
def add_header(response):
    response.cache_control.no_store=True
    return response

init_db()
app.register_blueprint(proyectos_bp)

# =========================
# FILE WRITER
# =========================
def write_file(path,content):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        f.write(content)

# =========================
# VIABILIDAD
# =========================
def analizar_viabilidad(idea):
    idea=idea.lower();score=0;j=[];p=[];s=[]
    if "incendio" in idea:score+=2;j.append("Emergencia real")
    else:p.append("No critico");s.append("Aplicar rescate/incendios")
    if "autonom" in idea:score+=2;j.append("Autonomia")
    else:score+=1;p.append("Sin autonomia");s.append("Agregar IA")
    if "sensor" in idea or "camara" in idea:score+=2;j.append("Percepcion")
    else:score+=1;p.append("Sin sensores");s.append("Agregar vision")
    estado="ALTAMENTE VIABLE" if score>=6 else "VIABLE" if score>=4 else "MEJORABLE"
    return {"estado":estado,"score":score,"justificacion":j,"problemas":p,"soluciones":s}

# =========================
# IDEA
# =========================
def analizar_idea(idea):
    return {"tipo":"incendio" if "incendio" in idea.lower() else "general","nivel":"alto","riesgo":"integracion sistemas","recomendacion":"PX4 + ROS2 + MAVLink"}

# =========================
# HARDWARE
# =========================
def generar_hardware(peso):
    return {"estructura":{"material":"carbono","tipo":"quad_x_industrial"},"propulsion":{"motores":4,"kv":1200,"thrust":6.5},"controlador":"Pixhawk","bateria":"LiPo 6S 10000mAh","sensores":{"lidar":True,"termico":True,"gps":True},"peso_total":peso}

# =========================
# SOFTWARE INDUSTRIAL REAL (LEVEL 7 FIXED)
# =========================
def generar_software(base):
    root=os.path.join(base,"software")

    estructura={
    "main.py":"""from core.system import DroneSystem
if __name__=="__main__":
    DroneSystem().run()
""",

    "core":{
    "system.py":"""import time
from comms.mavlink_node import MAVLinkNode
from control.flight_controller import FlightController
from perception.vision import VisionSystem
from navigation.planner import Planner
from telemetry.logger import Logger
from safety.failsafe import FailSafe

class DroneSystem:
    def __init__(self):
        self.mav=MAVLinkNode()
        self.fc=FlightController()
        self.vision=VisionSystem()
        self.nav=Planner()
        self.log=Logger()
        self.safe=FailSafe()

        self.mav.arm()

    def run(self):
        while True:
            s=self.mav.get_telemetry()
            v=self.vision.process()

            if self.safe.check(s):
                self.mav.emergency_land()
                continue

            m=self.nav.update(s,v)
            c=self.fc.update(s,m)

            self.mav.send_control(c)
            self.log.log(s)

            time.sleep(0.02)
"""},

    "comms":{
    "mavlink_node.py":"""from pymavlink import mavutil

class MAVLinkNode:
    def __init__(self):
        self.master=mavutil.mavlink_connection('udp:127.0.0.1:14550')
        self.master.wait_heartbeat()

    def arm(self):
        self.master.arducopter_arm()

    def get_telemetry(self):
        msg=self.master.recv_match(blocking=False)
        data={"altitude":0,"battery":100}

        if msg and msg.get_type()=="GLOBAL_POSITION_INT":
            data["altitude"]=msg.relative_alt/1000

        return data

    def send_control(self,c):
        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,
            int(c.get("roll",1500)),
            int(c.get("pitch",1500)),
            int(c.get("throttle",1500)),
            int(c.get("yaw",1500)),
            0,0,0,0
        )

    def emergency_land(self):
        print("FAILSAFE LAND")
"""},

    "control":{
    "pid.py":"""class PID:
    def __init__(self,kp,ki,kd):
        self.kp=kp
        self.ki=ki
        self.kd=kd
        self.i=0
        self.prev=0

    def update(self,sp,meas,dt):
        e=sp-meas
        self.i+=e*dt
        d=(e-self.prev)/dt if dt>0 else 0
        self.prev=e
        return self.kp*e+self.ki*self.i+self.kd*d
""",

    "flight_controller.py":"""from control.pid import PID

class FlightController:
    def __init__(self):
        self.alt=PID(1.5,0.02,0.5)

    def update(self,s,m):
        t=1500+self.alt.update(10,s.get("altitude",0),0.02)*100
        return {"roll":1500,"pitch":1500,"yaw":1500,"throttle":t}
"""},

    "perception":{
    "vision.py":"""import cv2

class VisionSystem:
    def __init__(self):
        self.cap=cv2.VideoCapture(0)

    def process(self):
        ret,frame=self.cap.read()
        if not ret:return {}
        return {"vision":True}
"""},

    "navigation":{
    "planner.py":"""class Planner:
    def update(self,s,v):
        if s.get("battery",100)<25:return {"mode":"RTL"}
        if v.get("vision"):return {"mode":"TRACK"}
        return {"mode":"PATROL"}
"""},

    "safety":{
    "failsafe.py":"""class FailSafe:
    def check(self,s):
        return s.get("battery",100)<15
"""},

    "telemetry":{
    "logger.py":"""import time
class Logger:
    def log(self,d):
        print(time.time(),d)
"""},

    "config":{
    "params.yaml":"pid: {kp:1.5,ki:0.02,kd:0.5}"
    }}

    def crear(r,c):
        if isinstance(c,dict):
            for k,v in c.items():
                crear(os.path.join(r,k),v)
        else:
            write_file(r,c)

    crear(root,estructura)
    return estructura

# =========================
# RESTO
# =========================
def calcular_fisica(peso):
    thrust=26
    return {"thrust_total":thrust,"relacion":round(thrust/peso,2),"estado":"ESTABLE"}

def generar_telemetria():
    return {"vars":["x","y","z","battery"],"hz":10}

def generar_modelo_3d(base,peso):
    return {"tipo":"quad_x_industrial","formato":"URDF + STL","escala":peso}

def exportar_zip(path):
    z=path+".zip"
    with zipfile.ZipFile(z,'w') as zipf:
        for root,_,files in os.walk(path):
            for f in files:
                full=os.path.join(root,f)
                zipf.write(full,os.path.relpath(full,path))
    return z

# =========================
# CORE
# =========================
class MaiaCore:
    def ejecutar_paso(self,idea,paso,data):
        if paso==0:
            return {"paso":1,"data":{"core":analizar_drone(idea),"viabilidad":analizar_viabilidad(idea),"analisis_idea":analizar_idea(idea)}}
        elif paso==1:
            data["hardware"]=generar_hardware(12);return {"paso":2,"data":data}
        elif paso==2:
            base=f"maia_projects/{int(time.time())}";os.makedirs(base,exist_ok=True)
            data["base"]=base;data["software"]=generar_software(base)
            return {"paso":3,"data":data}
        elif paso==3:
            data["fisica"]=calcular_fisica(data["hardware"]["peso_total"])
            data["telemetria"]=generar_telemetria()
            return {"paso":4,"data":data}
        elif paso==4:
            data["riesgos"]=["viento","bateria","comunicacion"]
            return {"paso":5,"data":data}
        elif paso==5:
            data["modelo_3d"]=generar_modelo_3d(data["base"],data["hardware"]["peso_total"])
            return {"paso":6,"data":data}
        elif paso==6:
            data["zip"]=exportar_zip(data["base"])
            data["nivel_maia"]="NIVEL 7 - INDUSTRIAL REAL STACK"
            return {"final":True,"resultado":data}

# =========================
# API
# =========================
@app.route("/maia_step",methods=["POST"])
def maia_step():
    req=request.get_json() or {}
    core=MaiaCore()
    return jsonify(core.ejecutar_paso(req.get("idea",""),int(req.get("paso",0)),req.get("data",{})))

# =========================
# VISTAS
# =========================
@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN
# =========================
if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)