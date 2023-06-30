import psutil, speedtest, subprocess
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import *

app=FastAPI()
template=Jinja2Templates(directory="templates")

@app.get("/")
def home(request:Request):
    # subprocess.run(["./inject.sh 44.202.103.183 ubuntu server.pem"],shell=True)
    return {"Hello":"World"}

@app.get("/dashboard/",response_class=HTMLResponse)
def dashboard(request: Request):
    ip='44.202.103.183'
    cpu_metric=psutil.cpu_percent()
    mem_metric=psutil.virtual_memory().percent
    disk_metric=psutil.disk_usage('/').percent
    # speed=speedtest.Speedtest().download()
    net_metric=50
    # net_metric=speed/(10**7)
    return template.TemplateResponse("dashboard.html",{"request":request,"ip":ip,"cpu_metric":cpu_metric,"mem_metric":mem_metric,"disk_metric":disk_metric,"net_metric":net_metric})