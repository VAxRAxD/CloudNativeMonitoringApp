import psutil,uvicorn
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def main():
    cpu_metric=psutil.cpu_percent()
    mem_metric=psutil.virtual_memory().percent
    if cpu_metric > 80 or mem_metric > 80:
        Message = "High CPU or Memory Detected, scale up!!!"
    return {"cpu_percent":cpu_metric,"memory_percent":mem_metric}