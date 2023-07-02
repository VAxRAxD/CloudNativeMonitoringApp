import psutil, speedtest, subprocess, os, urllib.request
from flask import Flask, render_template, request, redirect, json, make_response
from database import *
from apscheduler.schedulers.background import BackgroundScheduler

UPLOAD_FOLDER='keys/'

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

NET_METRIC,CPU_METRIC,MEM_METRIC,DISK_METRIC=2,None,None,None

def netUSage():
    global NET_METRIC
    NET_METRIC=(speedtest.Speedtest().download())/(10**7)

def deviceStat():
    global CPU_METRIC, MEM_METRIC, DISK_METRIC
    CPU_METRIC=psutil.cpu_percent()
    MEM_METRIC=psutil.virtual_memory().percent
    DISK_METRIC=psutil.disk_usage('/').percent

scheduler = BackgroundScheduler()
# network_job = scheduler.add_job(netUSage, 'interval', seconds=8, max_instances=5)
device_job = scheduler.add_job(deviceStat, 'interval', seconds=1, max_instances=2)
scheduler.start()

@app.route("/",methods=['GET'])
def home():
    servers=viewData()
    return render_template("main.html",servers=servers)

@app.route("/add/",methods=['POST'])
def addServer():
    ipaddr=request.form.get("ipaddr")
    name=request.form.get("name")
    key=request.files["file"]
    filename=ipaddr+"-"+name+"."+key.filename.split(".")[-1]
    key.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    addData(ipaddr,name)
    subprocess.run([f"./inject.sh {ipaddr} {name} keys/{filename}"],shell=True) 
    return redirect("/")

@app.route("/dashboard/",methods=['GET'])
def dashboard():
    ip=urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return render_template("dashboard.html",ip=ip)

@app.route("/metrics/",methods=['GET'])
def metrics():
    return [{'cpu_metric':CPU_METRIC,'mem_metric':MEM_METRIC,'disk_metric':DISK_METRIC,'net_metric':NET_METRIC}]

@app.route("/delete/",methods=['POST'])
def deleteData():
    data=json.loads(request.data)
    delData(data['ip'])
    return [{'deletion':'success'}]

if __name__ == '__main__':
    app.run(debug=True)