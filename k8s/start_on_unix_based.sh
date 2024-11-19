#!/bin/bash

# Print with colors
print_cyan() { printf "\033[0;36m🚀 %s\033[0m\n" "$1"; }
print_yellow() { printf "\033[0;33m%s\033[0m\n" "$1"; }
print_red() { printf "\033[0;31m❌ %s\033[0m\n" "$1"; }
print_green() { printf "\033[0;32m✅ %s\033[0m\n" "$1"; }
print_gray() { printf "\033[0;37m%s\033[0m\n" "$1"; }

print_cyan "Starting Snow Peak application setup..."

# Check prerequisites
if ! command -v kubectl &> /dev/null; then
    print_red "kubectl not found"
    exit 1
fi

if ! command -v minikube &> /dev/null; then
    print_red "minikube not found"
    exit 1
fi

# Start minikube if not running
if [ "$(minikube status --format '{{.Host}}')" != "Running" ]; then
    print_yellow "🔄 Starting Minikube..."
    minikube start
fi

# Create ConfigMaps
print_yellow "📦 Creating ConfigMaps..."
kubectl delete configmap keycloak-realms-config --ignore-not-found
kubectl delete configmap rabbitmq-plugins-config --ignore-not-found
kubectl delete configmap nginx-config --ignore-not-found

kubectl create configmap keycloak-realms-config --from-file=./keycloak/realms/
kubectl create configmap rabbitmq-plugins-config --from-file=enabled_plugins=./rabbitmq_enabled_plugins
kubectl create configmap nginx-config --from-file=nginx.conf=./client/nginx.conf

# Apply Kubernetes manifests
print_yellow "🎮 Applying Kubernetes manifests..."
kubectl apply -f ./k8s/manifest_prod.yaml

# Wait for pod function
wait_for_pod() {
    pod_prefix=$1
    print_gray "Waiting for $pod_prefix..."
    attempts=0
    while [ $attempts -lt 20 ]; do
        if kubectl get pods | grep "^$pod_prefix" | grep -q "Running"; then
            print_green "$pod_prefix is ready"
            return 0
        fi
        attempts=$((attempts + 1))
        sleep 2
    done
    print_red "Timeout waiting for $pod_prefix"
    return 1
}

# Wait for critical services
services=("db" "keycloak-postgres" "keycloak" "rabbitmq" "ski-lift-1" "ski-lift-2" "ski-lift-3" "backend" "frontend")
for service in "${services[@]}"; do
    wait_for_pod "$service"
done

# Start minikube tunnel in background
print_yellow "🚇 Starting minikube tunnel..."
minikube tunnel &
tunnel_pid=$!

# Trap to kill the tunnel process on script exit
trap 'kill $tunnel_pid 2>/dev/null' EXIT

print_green "✅ Setup completed! Services are available at:"
print_cyan "📊 RabbitMQ Management: http://localhost:15672"
print_cyan "🌐 Frontend: http://localhost:80"
print_cyan "🔒 Keycloak: http://localhost:9090"
print_yellow "⚠️  Keep this window open to maintain tunnel connection"

# Wait for user interrupt
wait $tunnel_pid
