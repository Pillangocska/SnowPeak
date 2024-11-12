# list all pods:
kubectl get pods
# start resources:
kubectl apply -f resources.yaml
# view all resources:
kubectl get all
# get logs for pod:
kubectl logs <pod-name>
# shell into container:
kubectl exec -it <pod-name> -- /bin/bash
# delete resources
kubectl delete -f <filename>.yaml
