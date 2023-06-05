from kubernetes import client,config

# aws eks update-kubeconfig --name cloud-native-cluster
config.load_kube_config()

api_client=client.ApiClient()

#Deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="server-monitoring"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "server-monitoring"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "server-monitoring"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="server-monitoring-container",
                        image="031677989988.dkr.ecr.us-east-1.amazonaws.com/server_monitoring:latest",
                        ports=[client.V1ContainerPort(container_port=8000)]
                    )
                ]
            )
        )
    )
)

#Create Deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

#Servive
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