import psutil
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app=FastAPI()
template=Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def main(request: Request):
    cpu_metric=psutil.cpu_percent()
    mem_metric=psutil.virtual_memory().percent
    disk_metric=psutil.disk_usage('/').percent
    nic_info=psutil.net_if_stats()
    net_metric=0
    for entry in nic_info:
        net_metric=max(net_metric,nic_info[entry][2])
    return template.TemplateResponse("main.html",{"request":request,"cpu_metric":cpu_metric,"mem_metric":mem_metric,"disk_metric":disk_metric,"net_metric":net_metric/10000})