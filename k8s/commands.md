# k8s components
## ConfigMap
ConfigMaps store configuration data as key-value pairs
They separate configuration from the application code
## Deployment
Deployments manage the lifecycle of pods (containers)
They ensure the desired number of pods are running
Handle updates and rollbacks
## Service
Services provide networking and load balancing for pods
They give pods a stable network identity
Enable communication between different parts of your application
- ClusterIP: Internal access only
- NodePort: Exposes port on each node
- LoadBalancer: Exposes service externally
- ExternalName: Maps service to external DNS
# PersistentVolumeClaim - PVC
PVCs request storage resources
Ensure data persists even if pods are restarted
Similar to Docker volumes but more abstract

# list all pods:
kubectl get pods
# view details of pod
kubectl describe pod <pod-name>
# start resources:
kubectl apply -f resources.yaml
# view all resources:
kubectl get all
# get logs for pod:
kubectl logs <pod-name>
kubectl logs -l app=keycloak
# shell into container:
kubectl exec -it <pod-name> -- /bin/bash
# delete resources
kubectl delete -f <filename>.yaml
# list all configmaps
kubectl get configmaps
# view details of configmap
kubectl describe configmap <configm-name>
# get URLs for all exposed services
minikube service list
# get URL for a specific service
minikube service keycloak --url
# get minikube ip
minikube ip
# see dashboard:
minikube dashboard
# stop minikube
minikube stop


# configs
kubectl create configmap keycloak-realms-config --from-file=./keycloak/realms/
kubectl create configmap rabbitmq-plugins-config --from-file=enabled_plugins=./rabbitmq_enabled_plugins
kubectl create configmap nginx-config --from-file=nginx.conf=./client/nginx.conf
# if we want to update:
kubectl delete configmap keycloak-realms-config
kubectl create configmap keycloak-realms-config --from-file=./keycloak/realms/
