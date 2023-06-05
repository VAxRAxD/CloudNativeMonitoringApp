import psutil,uvicorn,json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app=FastAPI()
template=Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def main(request: Request):
    cpu_metric=psutil.cpu_percent()
    mem_metric=psutil.virtual_memory().percent
    message=None
    if cpu_metric > 80 or mem_metric > 80:
        message = "High CPU or Memory Detected, scale up!!!"
    return template.TemplateResponse("main.html",{"request":request,"message":message,"cpu_metric":cpu_metric,"mem_metric":mem_metric})