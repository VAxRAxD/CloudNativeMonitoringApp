from kubernetes import client,config

# aws eks update-kubeconfig --name cloud-native-cluster
config.load_kube_config()

api_client=client.ApiClient()

#Deployment Configure
container = client.V1Container(
    name="server-monitoring",
    image="",
    ports=[client.V1ContainerPort(container_port=8000)]
)
template = client.V1PodTemplateSpec(
    metadata=client.V1ObjectMeta(labels={"app": "server-monitoring"}),
    spec=client.V1PodSpec(containers=[container]),
)
spec = client.V1DeploymentSpec(
    replicas=1, template=template, selector={"matchLabels":{"app": "server-monitoring"}})

deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="server-monitor-deployment"),
    spec=spec,
)

#Create Deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

#Servive Configure
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="server-monitoring-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "server-monitoring"},
        ports=[client.V1ServicePort(port=8000)]
    )
)

#Create Service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)