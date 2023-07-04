import psutil, speedtest, subprocess, os, urllib.request, requests
from flask import Flask, render_template, request, redirect, json,send_file
from datetime import datetime
from database import *
from apscheduler.schedulers.background import BackgroundScheduler

UPLOAD_FOLDER='keys/'
LOGS_FOLDER='logs/'

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['LOGS_FOLDER']=LOGS_FOLDER

NET_METRIC,CPU_METRIC,MEM_METRIC,DISK_METRIC=None,None,None,None

def netUSage():
    global NET_METRIC
    NET_METRIC=round((speedtest.Speedtest().download())/(10**7),2)

def deviceStat():
    global CPU_METRIC, MEM_METRIC, DISK_METRIC
    CPU_METRIC=psutil.cpu_percent()
    MEM_METRIC=psutil.virtual_memory().percent
    DISK_METRIC=psutil.disk_usage('/').percent

def insertLogs():
    global CPU_METRIC, MEM_METRIC, DISK_METRIC, NET_METRIC
    url='http://vaxraxd.tech/reg'
    data={'ip':f"{urllib.request.urlopen('https://ident.me').read().decode('utf8')}",'cpu':CPU_METRIC, 'mem':MEM_METRIC,'disk':DISK_METRIC,'net':NET_METRIC}
    requests.post(url,json=data)

if os.environ.get('SIDE')=='NODE':
    scheduler = BackgroundScheduler()
    network_job = scheduler.add_job(netUSage, 'interval', seconds=8, max_instances=5, id='ntw')
    device_job = scheduler.add_job(deviceStat, 'interval', seconds=1, max_instances=1,id='dvc')
    logs_job=scheduler.add_job(insertLogs, 'interval',seconds=5,max_instances=1,id='log')
    scheduler.start()

@app.route("/",methods=['GET'])
def home():
    servers=viewData()
    return render_template("main.html",servers=servers)

@app.route("/add/",methods=['POST'])
def addServer():
    ipaddr=request.form.get("ipaddr").strip()
    name=request.form.get("name").strip()
    key=request.files["file"]
    filename=ipaddr+"-"+name+"."+key.filename.split(".")[-1]
    key.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    addData(ipaddr,name,filename)
    os.system(f"touch logs/{ipaddr}-{name}")
    os.system(f"fab -i keys/{filename} -H {ipaddr} -u {name} installApp") 
    return redirect("/")

@app.route("/dashboard/",methods=['GET'])
def dashboard():
    ip=urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return render_template("dashboard.html",ip=ip)

@app.route("/logboard/<ip>/",methods=['GET'])
def logboard(ip):
    user=getUser(ip)
    return render_template('logs.html',ip=ip,user=user)

@app.route("/reg/",methods=['POST'])
def registerLogs():
    data=json.loads(request.data)
    ip=data['ip']
    user=getUser(ip)
    time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    time+=" "*5
    cpu=f'CPU UTILIZATION : {data["cpu"]}%'
    cpu+=" "*(27-len(cpu))
    mem=f'MEMORY UTILIZATION : {data["mem"]}%'
    mem+=" "*(31-len(mem))
    disk=f'DISK UTILIZATION : {data["disk"]}%'
    disk+=" "*(29-len(disk))
    if data['net']:
        net=f'NETWORK SPEED : {data["net"]} MBITS/S'
    else:
        net='NETWORK SPEED : - MBITS/S'
    report=time+cpu+mem+disk+net
    os.system(f'echo "{report}">> logs/{ip}-{user}')
    return [{'logs':'success'}]

@app.route("/logs/<ip>/",methods=['GET'])
def logs(ip):
    user=getUser(ip)
    record=list()
    logs=open(f"logs/{ip}-{user}","r")
    for log in logs:
        s=log[:len(log)-1]
        s=s.split('  ')
        s=[data.strip() for data in s if data!=""]
        data=dict()
        data['time']=s[0]
        for i in range(1,len(s)-1):
            k,v=s[i].split(':')
            data[k.split(' ')[0].lower()]=float(v[:len(v)-1].strip())
        k,v=s[len(s)-1].split(':')
        if v.split(' ')[1]!="-":
            data[k.split(' ')[0].lower()]=float(v.split(' ')[1])
        else:
            data[k.split(' ')[0].lower()]="-"
        record.append(data)
    return record

@app.route("/return/<filename>/",methods=['GET'])
def returnLog(filename):
    return send_file(f"logs/{filename}",as_attachment=True,)

@app.route("/metrics/",methods=['GET'])
def metrics():
    return [{'cpu_metric':CPU_METRIC,'mem_metric':MEM_METRIC,'disk_metric':DISK_METRIC,'net_metric':NET_METRIC}]

@app.route("/delete/",methods=['GET','POST'])
def deleteData():
    if request.method=='POST':
        data=json.loads(request.data)
        ip=data['ip']
        user=getUser(ip)
        filename=getFile(ip)
        os.system(f"fab -i keys/{filename} -H {ip} -u {user} terminateApp")
        delData(data['ip'])
        return {"Deletion":"Success"}
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)