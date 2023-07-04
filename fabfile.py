from fabric.api import *

def installApp():
    run("sudo apt update")
    run("sudo apt install docker.io -y")
    run("sudo chmod 777 /var/run/docker.sock")
    run("docker pull vaxraxd/monitoring:nodes")
    run("docker run -d --name=monitor -p 80:80 vaxraxd/monitoring:nodes")

def terminateApp():
    run("docker kill monitor")
    run("docker rm monitor")
    run("docker rmi vaxraxd/monitoring:nodes")
    