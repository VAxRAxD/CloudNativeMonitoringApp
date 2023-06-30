import psutil, speedtest, subprocess, os
from flask import Flask, render_template, request, redirect
from database import *

UPLOAD_FOLDER='keys/'

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

# subprocess.run(["./inject.sh 44.202.103.183 ubuntu server.pem"],shell=True)

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
    ip='44.202.103.183'
    cpu_metric=psutil.cpu_percent()
    mem_metric=psutil.virtual_memory().percent
    disk_metric=psutil.disk_usage('/').percent
    # speed=speedtest.Speedtest().download()
    net_metric=50
    # net_metric=speed/(10**7)
    return render_template("dashboard.html",ip=ip,cpu_metric=cpu_metric,mem_metric=mem_metric,disk_metric=disk_metric,net_metric=net_metric)

if __name__ == '__main__':  
    app.run(debug=True)